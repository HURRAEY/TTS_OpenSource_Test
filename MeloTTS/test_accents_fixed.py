from melo.api import TTS
import soundfile as sf
import numpy as np
import os

# 테스트할 영어 문장들 (짧은 문장들로 테스트)
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

# MeloTTS에서 실제 지원되는 영어 버전들
english_versions = {
    'EN': 'EN (기본 영어)',      # 기본 영어
    'EN_V2': 'EN_V2 (영어 v2)',  # 영어 v2 버전
    'EN_NEWEST': 'EN_NEWEST (영어 최신)'  # 영어 최신 버전
}

# 출력 디렉토리 생성
output_dir = "accent_test_output_fixed"
os.makedirs(output_dir, exist_ok=True)

print("🎤 MeloTTS 영어 버전 테스트 시작...")
print("📋 테스트할 영어 버전들:")
for code, desc in english_versions.items():
    print(f"  • {code}: {desc}")

# 각 영어 버전별로 TTS 인스턴스 생성 및 테스트
for version_code, version_desc in english_versions.items():
    print(f"\n🔊 {version_desc} 테스트 중...")
    
    try:
        # TTS 인스턴스 생성
        tts = TTS(language=version_code, device='auto')
        
        # 버전별 디렉토리 생성
        version_dir = os.path.join(output_dir, version_code)
        os.makedirs(version_dir, exist_ok=True)
        
        # 각 문장을 해당 버전으로 생성
        for idx, sentence in enumerate(test_sentences, 1):
            output_path = os.path.join(version_dir, f"line_{idx:03d}.wav")
            
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
        
        print(f"✅ {version_desc} 완료 → {version_dir}")
        
    except Exception as e:
        print(f"❌ {version_desc} 로드 실패: {e}")

print(f"\n🎉 모든 영어 버전 테스트 완료!")
print(f"📁 결과 파일 위치: {output_dir}")
print("\n📋 영어 버전별 특징:")
print("• EN: 기본 영어 모델 (안정적)")
print("• EN_V2: 영어 v2 모델 (개선된 품질)")
print("• EN_NEWEST: 영어 최신 모델 (최고 품질)")

# 추가로 다른 언어들과 비교 테스트
print(f"\n🌍 다른 언어들과 비교 테스트...")
comparison_languages = {
    'KR': '한국어',
    'JP': '일본어', 
    'FR': '프랑스어',
    'ES': '스페인어',
    'ZH': '중국어'
}

for lang_code, lang_name in comparison_languages.items():
    print(f"\n🔊 {lang_name} 테스트 중...")
    
    try:
        tts = TTS(language=lang_code, device='auto')
        lang_dir = os.path.join(output_dir, f"comparison_{lang_code}")
        os.makedirs(lang_dir, exist_ok=True)
        
        # 각 언어별로 첫 번째 영어 문장을 테스트
        test_sentence = "Hello, this is a test sentence."
        output_path = os.path.join(lang_dir, "test_english.wav")
        
        try:
            tts.tts_to_file(
                text=test_sentence,
                speaker_id=0,
                output_path=output_path,
                speed=1.0,
                noise_scale=0.6,
                quiet=True,
            )
            print(f"  ✓ {lang_name}: 영어 문장 처리 성공")
        except Exception as e:
            print(f"  ✗ {lang_name}: 오류 - {e}")
            
    except Exception as e:
        print(f"❌ {lang_name} 로드 실패: {e}")

print(f"\n🎯 테스트 완료! 각 버전의 음질을 비교해보세요.") 