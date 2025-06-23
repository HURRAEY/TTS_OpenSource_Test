from melo.api import TTS
import soundfile as sf
import numpy as np
import os

# 테스트할 샘플 문장
sample_sentences = [
    "Hello, this is a test of English accent.",
    "How are you today?",
    "The weather is beautiful.",
    "I love this technology.",
    "Thank you very much."
]

# 국가별 영어 억양(speaker_id)
accent_speakers = {
    'EN-Default': '기본',
    'EN-US': '미국',
    'EN-BR': '영국',
    'EN_INDIA': '인도',
    'EN-AU': '호주',
}

output_dir = "accent_test_output_country"
os.makedirs(output_dir, exist_ok=True)

print("🎤 국가별 영어 억양 테스트 시작...")
print("📝 테스트 문장:")
for i, sentence in enumerate(sample_sentences, 1):
    print(f"  {i:2d}. {sentence}")

# TTS 인스턴스 생성 (영어)
tts = TTS(language='EN', device='auto')
speaker_ids = tts.hps.data.spk2id

for speaker, desc in accent_speakers.items():
    print(f"\n🔊 {desc}({speaker}) 억양 테스트 중...")
    spk_id = speaker_ids[speaker]
    accent_dir = os.path.join(output_dir, speaker)
    os.makedirs(accent_dir, exist_ok=True)
    for idx, sentence in enumerate(sample_sentences, 1):
        output_path = os.path.join(accent_dir, f"sample_{idx:02d}.wav")
        try:
            print(f"  생성 중: {sentence}")
            tts.tts_to_file(
                text=sentence,
                speaker_id=spk_id,
                output_path=output_path,
                speed=1.0,
                noise_scale=0.6,
                quiet=True,
            )
            print(f"  ✅ 완료: {output_path}")
        except Exception as e:
            print(f"  ❌ 오류: {e}")
    print(f"✅ {desc}({speaker}) 완료 → {accent_dir}")

print(f"\n🎉 모든 국가별 영어 억양 테스트 완료!")
print(f"📁 결과 파일 위치: {output_dir}")

# 파일 크기 확인
print(f"\n📊 생성된 파일 확인:")
for speaker in accent_speakers.keys():
    speaker_dir = os.path.join(output_dir, speaker)
    if os.path.exists(speaker_dir):
        wav_files = [f for f in os.listdir(speaker_dir) if f.endswith('.wav')]
        total_size = sum(os.path.getsize(os.path.join(speaker_dir, f)) for f in wav_files)
        print(f"  {speaker}: {len(wav_files)}개 파일, 총 {total_size:,} bytes")

print(f"\n🎯 테스트 완료! 각 버전의 음질을 비교해보세요.")
print(f"📝 샘플 문장: 'Hello, this is a test.'") 