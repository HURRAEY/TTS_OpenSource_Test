import os
import torch
import soundfile as sf
from transformers import AutoTokenizer

# ─────────────────────────────────────────────────────────────
# 환경 설정
# GPU 사용 가능하면 float16 으로, 아니면 float32 로 모델 로드
# ─────────────────────────────────────────────────────────────
DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float16 if torch.cuda.is_available() else torch.float32

OUTPUT_DIR = "tts_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────────
# ① Parler-TTS (영어)
# ─────────────────────────────────────────────────────────────
EN_MODEL_ID = "parler-tts/parler-tts-mini-v1"
from parler_tts import ParlerTTSForConditionalGeneration  # 지연 import

en_tokenizer = AutoTokenizer.from_pretrained(EN_MODEL_ID)
en_model = ParlerTTSForConditionalGeneration.from_pretrained(
    EN_MODEL_ID, torch_dtype=DTYPE
).to(DEVICE)

def parler_tts(text: str, idx: int):
    """Parler-TTS 로 단일 문장을 음성으로 변환하여 저장"""
    description = (
        "A neutral speaker delivers the line with a clear voice, moderate speed, very clear audio."
    )
    input_ids = en_tokenizer(description, return_tensors="pt").input_ids.to(DEVICE)
    prompt_ids = en_tokenizer(text, return_tensors="pt").input_ids.to(DEVICE)

    with torch.no_grad():
        wav = en_model.generate(input_ids=input_ids, prompt_input_ids=prompt_ids)

    wav = wav.cpu().numpy().squeeze()
    path = os.path.join(OUTPUT_DIR, f"en_{idx:03d}.wav")
    sf.write(path, wav, en_model.config.sampling_rate)
    return path

# ─────────────────────────────────────────────────────────────
# ③ 스크립트 입력 (영어 / 일본어)
# ─────────────────────────────────────────────────────────────
ENGLISH_LINES = [
    "So, this is home for you.",
    "Yes.",
    "But, why are the sink and bed in the same space?",
    "What?",
    "Aha! This must be the staff's break room.",
    "It's not a break room.",
    "Then what is it?",
    "It's a studio.",
    "A studio.",
    "Got it. I've seen the first room. Show me the second one.",
    "This is all of it.",
    "This is the whole house?",
    "Yes.",
    "Then, where's the pool?",
    "There's no pool.",
    "No pool in the house?",
    "No.",
    "What a laugh.",
    "By the way, is the TV on?",
    "I don't have a TV.",
    "But I hear voices.",
    "Oh, that's noise from the upstairs neighbor.",
    "Oh, this is that upstairs noise.",
    "What a laugh.",
    "Okay.",
    "Oh, what's this, though?",
    "I prepared some Korean snacks for us.",
    "I know Korean snacks.",
    "How do you know?",
    "My uncle always eats them at the market during elections.",
    "Oh, I see.",
    "Oh, right.",
    "This.",
    "What's this?",
    "A housewarming gift.",
    "It's okay, honey.",
    "Drive around comfortably.",
    "Well, the thing is…",
    "There's no parking space here.",
    "No parking space?",
    "What a laugh.",
]

# 일본어 대사 리스트 제거
JAPANESE_LINES = []

# ─────────────────────────────────────────────────────────────
# ④ 생성 루프
# ─────────────────────────────────────────────────────────────
print(f"[INFO] Generating {len(ENGLISH_LINES)} English lines …")
for i, line in enumerate(ENGLISH_LINES, 1):
    out_path = parler_tts(line, i)
    print(f"  ↳ {out_path}")

if JAPANESE_LINES:
    print(f"[INFO] Generating {len(JAPANESE_LINES)} Japanese lines … (currently disabled)")

print("[DONE] All English files are saved under", OUTPUT_DIR) 