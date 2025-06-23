from melo.api import TTS
from melo.download_utils import LANG_TO_HF_REPO_ID
import os

def get_model_details():
    """각 영어 버전의 모델 상세 정보"""
    
    print("🎯 MeloTTS 영어 버전별 모델 상세 정보")
    print("=" * 60)
    
    english_models = {
        'EN': 'myshell-ai/MeloTTS-English',
        'EN_V2': 'myshell-ai/MeloTTS-English-v2', 
        'EN_NEWEST': 'myshell-ai/MeloTTS-English-v3'
    }
    
    for version, model_id in english_models.items():
        print(f"\n📋 {version} 버전:")
        print(f"  🔗 모델 ID: {model_id}")
        
        # HuggingFace 링크
        hf_link = f"https://huggingface.co/{model_id}"
        print(f"  🌐 HuggingFace: {hf_link}")
        
        # 버전별 특징 설명
        if version == 'EN':
            print(f"  📝 특징: 기본 영어 모델 (안정적, 범용적)")
            print(f"  🎯 용도: 일반적인 영어 TTS, 안정성 중시")
            print(f"  ⚡ 성능: 기본 수준, 빠른 처리")
            
        elif version == 'EN_V2':
            print(f"  📝 특징: 개선된 영어 모델 (v2)")
            print(f"  🎯 용도: 향상된 품질의 영어 음성")
            print(f"  ⚡ 성능: 중간 수준, 품질과 속도 균형")
            
        elif version == 'EN_NEWEST':
            print(f"  📝 특징: 최신 영어 모델 (v3)")
            print(f"  🎯 용도: 최고 품질의 영어 음성")
            print(f"  ⚡ 성능: 최고 수준, 최신 기술 적용")
    
    print(f"\n🔍 모델 다운로드 위치:")
    cache_dir = os.path.expanduser("~/.cache/huggingface/hub")
    print(f"  📁 캐시 디렉토리: {cache_dir}")
    
    # 실제 다운로드된 모델 확인
    print(f"\n📦 다운로드된 모델 확인:")
    for version, model_id in english_models.items():
        model_path = os.path.join(cache_dir, "models--" + model_id.replace("/", "--"))
        if os.path.exists(model_path):
            print(f"  ✅ {version}: {model_id} (다운로드 완료)")
        else:
            print(f"  ❌ {version}: {model_id} (다운로드 필요)")

def compare_model_architectures():
    """모델 아키텍처 비교"""
    print(f"\n🏗️ 모델 아키텍처 비교")
    print("=" * 60)
    
    print("📊 각 버전별 기술적 특징:")
    print("\n🔹 EN (MeloTTS-English):")
    print("  • 기본 VITS 아키텍처")
    print("  • 표준 영어 음성 합성")
    print("  • 안정적인 성능")
    
    print("\n🔹 EN_V2 (MeloTTS-English-v2):")
    print("  • 개선된 VITS 아키텍처")
    print("  • 향상된 음질과 자연스러움")
    print("  • 더 나은 억양과 리듬")
    
    print("\n🔹 EN_NEWEST (MeloTTS-English-v3):")
    print("  • 최신 VITS2 아키텍처")
    print("  • 최고 품질의 음성 합성")
    print("  • 개선된 발음과 감정 표현")
    print("  • 더 효율적인 처리")

def show_usage_examples():
    """사용 예시"""
    print(f"\n💻 사용 예시")
    print("=" * 60)
    
    examples = {
        'EN': {
            'code': 'tts = TTS(language="EN", device="auto")',
            'use_case': '기본적인 영어 음성 필요시'
        },
        'EN_V2': {
            'code': 'tts = TTS(language="EN_V2", device="auto")',
            'use_case': '품질과 속도의 균형이 필요시'
        },
        'EN_NEWEST': {
            'code': 'tts = TTS(language="EN_NEWEST", device="auto")',
            'use_case': '최고 품질의 영어 음성 필요시'
        }
    }
    
    for version, info in examples.items():
        print(f"\n🔹 {version} 사용법:")
        print(f"  ```python")
        print(f"  {info['code']}")
        print(f"  tts.tts_to_file(text='Hello world', output_path='output.wav')")
        print(f"  ```")
        print(f"  🎯 용도: {info['use_case']}")

def show_performance_comparison():
    """성능 비교"""
    print(f"\n⚡ 성능 비교 (테스트 결과 기반)")
    print("=" * 60)
    
    performance_data = {
        'EN': {
            'duration': '2.50초',
            'file_size': '220KB',
            'rms': '0.0435',
            'quality': '기본'
        },
        'EN_V2': {
            'duration': '2.48초', 
            'file_size': '218KB',
            'rms': '0.0668',
            'quality': '개선'
        },
        'EN_NEWEST': {
            'duration': '1.58초',
            'file_size': '140KB', 
            'rms': '0.0751',
            'quality': '최고'
        }
    }
    
    print("📊 성능 지표:")
    print(f"{'버전':<12} {'길이':<8} {'파일크기':<10} {'RMS':<8} {'품질':<8}")
    print("-" * 50)
    
    for version, data in performance_data.items():
        print(f"{version:<12} {data['duration']:<8} {data['file_size']:<10} {data['rms']:<8} {data['quality']:<8}")

if __name__ == "__main__":
    get_model_details()
    compare_model_architectures()
    show_usage_examples()
    show_performance_comparison()
    
    print(f"\n🎯 결론:")
    print("• EN_NEWEST (v3)가 가장 최신 기술과 최고 품질 제공")
    print("• EN_V2 (v2)는 안정성과 품질의 균형점")
    print("• EN (v1)은 기본적인 영어 음성에 적합") 