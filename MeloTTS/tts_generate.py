from melo.api import TTS
import importlib, sys
import argparse, re
import soundfile as sf
import numpy as np
import os
import torch, librosa
from melo.mel_processing import spectrogram_torch
from melo import utils

# ---- Patch: alias `MeCab` as `mecab` for g2pkk (Korean) ----
try:
    import MeCab as _MeCab
    sys.modules.setdefault('mecab', _MeCab)
except ImportError:
    pass

# -----------------------------
# 0. CLI 인자 파싱
# -----------------------------
parser = argparse.ArgumentParser(description="Multi-lang TTS generator for OpenVoice/MeloTTS")
parser.add_argument("--script", type=str, default="script.txt", help="대본 파일 경로 (UTF-8)")
parser.add_argument("--languages", type=str, default="JA,EN,KR", help="합성할 언어 코드 콤마 구분 (예: JA,EN)")
parser.add_argument("--speaker", type=str, default=None, help="특정 화자명(한글/영문)만 선택해 합성. 미지정 시 전체 화자")
parser.add_argument("--ref_wav", type=str, default=None, help="음색 클로닝용 참조 WAV 파일 경로 (mono/16k~48kHz)" )
args = parser.parse_args()

# 확인용
selected_langs = [l.strip().upper() for l in args.languages.split(',') if l.strip()]

# -----------------------------
# 1. Prepare TTS instances per language (CPU by default)
# -----------------------------
# 이전 코드 블록 유지하면서, 선택된 언어만 생성하도록 수정
lang_map = {  # 사용자가 입력하는 코드와 MeloTTS 내부 코드 매핑
    'JA': 'JP',
    'JP': 'JP',
    'EN': 'EN',
    'KR': 'KR',
}

tts_instances = {}
for user_code in selected_langs:
    if user_code not in lang_map:
        print(f"[WARN] 지원되지 않는 언어 코드 무시: {user_code}")
        continue
    internal_code = lang_map[user_code]
    try:
        tts_instances[user_code] = TTS(language=internal_code, device='auto')
    except Exception as e:
        print(f"[WARN] {user_code} TTS 인스턴스 로드 실패: {e}")

# -----------------------------
# 2. 대본 파싱 (화자 필터)
# -----------------------------
sentences = {code: [] for code in tts_instances}

def is_speaker_line(line: str) -> bool:
    """한글/영문으로만 이루어지고 공백이 없는 라인을 화자 이름으로 간주."""
    return bool(re.fullmatch(r"[\uAC00-\uD7A3A-Za-z]+", line))

script_path = args.script
if not os.path.exists(script_path):
    print(f"[ERROR] 스크립트 파일이 존재하지 않습니다: {script_path}")
    exit(1)

with open(script_path, encoding='utf-8') as f:
    current_speaker = None
    buffer = []  # 화자 한 턴의 문장들

    def flush_buffer():
        """현재 buffer(JA/EN/KR) -> sentences 에 누적"""
        if not buffer:
            return
        if args.speaker and current_speaker != args.speaker:
            return  # 화자 필터링
        # 언어 순서가 JA, EN, KR 로 들어왔다고 가정하되, 부족하면 패스
        for idx, code in enumerate(['JA', 'EN', 'KR']):
            if code in sentences and idx < len(buffer):
                sentences[code].append(buffer[idx])
        buffer.clear()

    for raw in f:
        line = raw.rstrip('\n').strip()
        if not line:
            continue
        if is_speaker_line(line):
            # 화자가 변경되면 이전 buffer flush
            flush_buffer()
            current_speaker = line
            continue
        buffer.append(line)

    # 파일 끝 flush
    flush_buffer()

# -----------------------------
# 3. 합성할 문장이 없는 경우 경고
# -----------------------------
if not any(sentences.values()):
    print("[WARN] 합성할 문장이 없습니다. 스크립트 형식 또는 화자/언어 선택을 확인하세요.")
    exit(0)

# -----------------------------
# 4. Output directory
# -----------------------------
OUTPUT_DIR = "wav_out"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# 4. (Optional) Reference audio embedding 추출
# -----------------------------
g_global = None
if args.ref_wav:
    # 처음 선택된 언어의 hps로 mel 스펙트로그램 파라미터 사용
    first_tts = None
    if tts_instances:
        first_tts = next(iter(tts_instances.values()))
    if first_tts is None:
        print("[ERROR] TTS 인스턴스가 없어 ref_wav 임베딩을 만들 수 없습니다.")
    else:
        hps = first_tts.hps
        wav, _ = librosa.load(args.ref_wav, sr=hps.data.sampling_rate, mono=True)
        wav_tensor = torch.FloatTensor(wav).unsqueeze(0).to(first_tts.device)
        win_len = getattr(hps.data, 'win_length', hps.data.filter_length)
        with torch.no_grad():
            spec = spectrogram_torch(
                wav_tensor,
                hps.data.filter_length,
                hps.data.sampling_rate,
                hps.data.hop_length,
                win_len,
                center=False,
            )
            g_global = first_tts.model.ref_enc(spec.transpose(1, 2)).unsqueeze(-1)
        print(f"[+] reference embedding 추출 완료: {args.ref_wav}")

# -----------------------------
# 5. Generate TTS files
# -----------------------------
for lang_code, tts in tts_instances.items():
    if not sentences[lang_code]:
        continue
    print(f"\n[+] Synthesising {lang_code} sentences ({len(sentences[lang_code])} lines)...")
    for idx, sentence in enumerate(sentences[lang_code], 1):
        out_path = os.path.join(OUTPUT_DIR, f"{lang_code}_{idx:03d}.wav")
        try:
            if g_global is None:
                # 기본 음색
                tts.tts_to_file(
                    text=sentence,
                    speaker_id=0,
                    output_path=out_path,
                    speed=1.0,
                    noise_scale=0.6,
                    quiet=True,
                )
            else:
                # 음색 클로닝: 내부 infer 호출 커스텀
                # 참고로 tts_to_file 구현을 부분 복사하여 g 파라미터 주입
                texts = tts.split_sentences_into_pieces(sentence, tts.language, quiet=True)
                audio_segments = []
                for t_piece in texts:
                    bert, ja_bert, phones, tones, lang_ids = \
                        utils.get_text_for_tts_infer(t_piece, tts.language, tts.hps, tts.device, tts.symbol_to_id)
                    with torch.no_grad():
                        x_tst = phones.to(tts.device).unsqueeze(0)
                        tones_t = tones.to(tts.device).unsqueeze(0)
                        lang_ids_t = lang_ids.to(tts.device).unsqueeze(0)
                        bert_t = bert.to(tts.device).unsqueeze(0)
                        ja_bert_t = ja_bert.to(tts.device).unsqueeze(0)
                        x_tst_lengths = torch.LongTensor([phones.size(0)]).to(tts.device)
                        audio_piece, *_ = tts.model.infer(
                            x_tst,
                            x_tst_lengths,
                            torch.LongTensor([0]).to(tts.device),
                            tones_t,
                            lang_ids_t,
                            bert_t,
                            ja_bert_t,
                            sdp_ratio=0.2,
                            noise_scale=0.6,
                            noise_scale_w=0.8,
                            length_scale=1.0,
                            g=g_global,
                        )
                        audio_piece = audio_piece[0, 0].data.cpu().float().numpy()
                    audio_segments += audio_piece.tolist()
                    audio_segments += [0] * int((tts.hps.data.sampling_rate * 0.05))
                audio_np = np.array(audio_segments).astype(np.float32)
                sf.write(out_path, audio_np, tts.hps.data.sampling_rate)
            print(f"  • {out_path}")
        except Exception as e:
            print(f"  [FAIL] {lang_code} {idx:03d}: {e}")

print("\n[✓] TTS generation finished. 'wav_out' 폴더를 확인하세요.") 