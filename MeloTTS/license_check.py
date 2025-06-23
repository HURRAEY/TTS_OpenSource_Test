import requests
import json
from melo.download_utils import LANG_TO_HF_REPO_ID

def check_huggingface_license(model_id):
    """HuggingFace에서 모델의 라이선스 정보 확인"""
    try:
        url = f"https://huggingface.co/api/models/{model_id}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('license', 'Unknown')
        else:
            return "API 접근 실패"
    except Exception as e:
        return f"오류: {e}"

def analyze_licenses():
    """모든 모델의 라이선스 분석"""
    print("🔍 MeloTTS 라이선스 분석")
    print("=" * 60)
    
    print("📋 소프트웨어 라이선스 (MeloTTS 코드):")
    print("✅ MIT License - 상업적 이용 가능")
    print("  • 자유로운 사용, 수정, 배포 가능")
    print("  • 상업적 이용 제한 없음")
    print("  • 저작권 표시만 요구")
    
    print(f"\n📋 모델별 라이선스 확인:")
    print("-" * 60)
    
    for lang_code, model_id in LANG_TO_HF_REPO_ID.items():
        license_info = check_huggingface_license(model_id)
        print(f"{lang_code:<12}: {license_info}")
    
    print(f"\n⚠️  중요 고려사항:")
    print("1. 소프트웨어 (MeloTTS 코드): MIT License - 상업적 이용 가능")
    print("2. 모델 가중치: 각 모델별로 개별 라이선스 확인 필요")
    print("3. 훈련 데이터: 원본 데이터의 라이선스 확인 필요")
    print("4. 음성 샘플: 생성된 음성의 저작권 고려 필요")

def commercial_usage_guidelines():
    """상업적 이용 가이드라인"""
    print(f"\n💼 상업적 이용 가이드라인")
    print("=" * 60)
    
    print("✅ 일반적으로 허용되는 용도:")
    print("  • 상업용 애플리케이션 개발")
    print("  • 유료 서비스 제공")
    print("  • 제품에 TTS 기능 통합")
    print("  • 음성 콘텐츠 생성 및 판매")
    
    print(f"\n⚠️  주의사항:")
    print("  • 저작권 표시 유지 (MIT License 요구사항)")
    print("  • 모델별 라이선스 조건 확인")
    print("  • 생성된 음성의 저작권 고려")
    print("  • 개인정보 보호법 준수")
    
    print(f"\n🔗 확인 방법:")
    print("  1. 각 모델의 HuggingFace 페이지 방문")
    print("  2. 'License' 섹션 확인")
    print("  3. 필요시 MyShell.ai에 문의")

def check_specific_models():
    """주요 모델들의 라이선스 상세 확인"""
    print(f"\n🎯 주요 영어 모델 라이선스 상세 확인")
    print("=" * 60)
    
    english_models = {
        'EN': 'myshell-ai/MeloTTS-English',
        'EN_V2': 'myshell-ai/MeloTTS-English-v2',
        'EN_NEWEST': 'myshell-ai/MeloTTS-English-v3'
    }
    
    for version, model_id in english_models.items():
        print(f"\n📋 {version} ({model_id}):")
        license_info = check_huggingface_license(model_id)
        print(f"  라이선스: {license_info}")
        
        # 일반적인 라이선스 해석
        if 'mit' in license_info.lower():
            print(f"  ✅ 상업적 이용 가능")
        elif 'apache' in license_info.lower():
            print(f"  ✅ 상업적 이용 가능")
        elif 'cc' in license_info.lower():
            print(f"  ⚠️  Creative Commons - 조건 확인 필요")
        elif 'unknown' in license_info.lower():
            print(f"  ⚠️  라이선스 정보 불명확 - 직접 확인 필요")
        else:
            print(f"  ⚠️  기타 라이선스 - 조건 확인 필요")

if __name__ == "__main__":
    analyze_licenses()
    commercial_usage_guidelines()
    check_specific_models()
    
    print(f"\n🎯 결론:")
    print("• MeloTTS 소프트웨어: MIT License로 상업적 이용 가능")
    print("• 모델 가중치: 각 모델별 라이선스 확인 필요")
    print("• 권장사항: 실제 상업적 이용 전 MyShell.ai에 문의") 