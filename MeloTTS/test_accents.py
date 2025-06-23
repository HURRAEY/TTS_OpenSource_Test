from melo.api import TTS
import soundfile as sf
import numpy as np
import os

# 테스트할 영어 문장들
test_sentences = [
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
    "Oh, that's just upstairs noise.",
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
    "What a laugh."
]

# 영어 액센트 옵션들
accent_options = {
    'EN-US': 'EN-US',      # 미국식 영어
    'EN-BR': 'EN-BR',      # 영국식 영어  
    'EN-INDIA': 'EN_INDIA', # 인도식 영어
    'EN-AU': 'EN-AU',      # 호주식 영어
    'EN-Default': 'EN-Default'  # 기본 영어
}

# 출력 디렉토리 생성
output_dir = "accent_test_output"
os.makedirs(output_dir, exist_ok=True)

print("🎤 MeloTTS 영어 액센트 테스트 시작...")

# 각 액센트별로 TTS 인스턴스 생성 및 테스트
for accent_name, accent_code in accent_options.items():
    print(f"\n🔊 {accent_name} 액센트 테스트 중...")
    
    try:
        # TTS 인스턴스 생성
        tts = TTS(language=accent_code, device='auto')
        
        # 액센트별 디렉토리 생성
        accent_dir = os.path.join(output_dir, accent_name)
        os.makedirs(accent_dir, exist_ok=True)
        
        # 각 문장을 해당 액센트로 생성
        for idx, sentence in enumerate(test_sentences, 1):
            output_path = os.path.join(accent_dir, f"line_{idx:03d}.wav")
            
            try:
                tts.tts_to_file(
                    text=sentence,
                    speaker_id=0,
                    output_path=output_path,
                    speed=1.0,
                    noise_scale=0.6,
                    quiet=True,
                )
                print(f"  ✓ {idx:03d}: {sentence[:50]}...")
            except Exception as e:
                print(f"  ✗ {idx:03d}: 오류 - {e}")
        
        print(f"✅ {accent_name} 완료 → {accent_dir}")
        
    except Exception as e:
        print(f"❌ {accent_name} 로드 실패: {e}")

print(f"\n🎉 모든 액센트 테스트 완료!")
print(f"📁 결과 파일 위치: {output_dir}")
print("\n📋 액센트별 특징:")
print("• EN-US: 미국식 영어 (표준 미국 발음)")
print("• EN-BR: 영국식 영어 (영국식 억양과 발음)")
print("• EN-INDIA: 인도식 영어 (인도식 억양)")
print("• EN-AU: 호주식 영어 (호주식 억양)")
print("• EN-Default: 기본 영어 (일반적인 영어)") 