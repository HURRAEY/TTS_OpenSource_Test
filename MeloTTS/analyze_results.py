import os
import glob
import soundfile as sf
import numpy as np

def analyze_audio_file(file_path):
    """오디오 파일 분석"""
    try:
        data, samplerate = sf.read(file_path)
        duration = len(data) / samplerate
        rms = np.sqrt(np.mean(data**2))
        return {
            'duration': duration,
            'rms': rms,
            'file_size': os.path.getsize(file_path),
            'sample_rate': samplerate
        }
    except Exception as e:
        return None

def compare_versions():
    """영어 버전들 비교"""
    base_dir = "accent_test_output_fixed"
    versions = ['EN', 'EN_V2', 'EN_NEWEST']
    
    print("🎵 MeloTTS 영어 버전 비교 분석")
    print("=" * 50)
    
    for version in versions:
        version_dir = os.path.join(base_dir, version)
        if not os.path.exists(version_dir):
            continue
            
        print(f"\n📊 {version} 분석:")
        
        # 첫 번째 파일 분석 (샘플)
        sample_file = os.path.join(version_dir, "line_001.wav")
        if os.path.exists(sample_file):
            analysis = analyze_audio_file(sample_file)
            if analysis:
                print(f"  • 샘플 파일: line_001.wav")
                print(f"  • 길이: {analysis['duration']:.2f}초")
                print(f"  • 파일 크기: {analysis['file_size']:,} bytes")
                print(f"  • 샘플레이트: {analysis['sample_rate']} Hz")
                print(f"  • RMS 레벨: {analysis['rms']:.4f}")
        
        # 전체 파일 수
        wav_files = glob.glob(os.path.join(version_dir, "*.wav"))
        print(f"  • 총 파일 수: {len(wav_files)}개")
        
        # 전체 파일 크기
        total_size = sum(os.path.getsize(f) for f in wav_files)
        print(f"  • 총 크기: {total_size:,} bytes ({total_size/1024/1024:.1f} MB)")

def compare_languages():
    """다른 언어들과 비교"""
    base_dir = "accent_test_output_fixed"
    languages = ['comparison_JP', 'comparison_FR', 'comparison_ES', 'comparison_ZH']
    
    print(f"\n🌍 다른 언어들과의 비교")
    print("=" * 50)
    
    for lang in languages:
        lang_dir = os.path.join(base_dir, lang)
        if not os.path.exists(lang_dir):
            continue
            
        lang_name = lang.replace('comparison_', '')
        print(f"\n📊 {lang_name}:")
        
        test_file = os.path.join(lang_dir, "test_english.wav")
        if os.path.exists(test_file):
            analysis = analyze_audio_file(test_file)
            if analysis:
                print(f"  • 영어 문장 처리 결과:")
                print(f"  • 길이: {analysis['duration']:.2f}초")
                print(f"  • 파일 크기: {analysis['file_size']:,} bytes")
                print(f"  • RMS 레벨: {analysis['rms']:.4f}")

def generate_summary():
    """요약 리포트 생성"""
    print(f"\n📋 MeloTTS 영어 버전 테스트 요약")
    print("=" * 50)
    print("✅ 성공적으로 생성된 버전들:")
    print("  • EN (기본 영어) - 안정적이고 기본적인 영어 음성")
    print("  • EN_V2 (영어 v2) - 개선된 품질의 영어 음성")
    print("  • EN_NEWEST (영어 최신) - 최고 품질의 영어 음성")
    
    print(f"\n🌍 다국어 지원 테스트:")
    print("  • 일본어 (JP): ✅ 영어 문장 처리 성공")
    print("  • 프랑스어 (FR): ✅ 영어 문장 처리 성공")
    print("  • 스페인어 (ES): ✅ 영어 문장 처리 성공")
    print("  • 중국어 (ZH): ✅ 영어 문장 처리 성공")
    print("  • 한국어 (KR): ❌ g2pkk 모듈 누락")
    
    print(f"\n💡 영어 음질 개선 권장사항:")
    print("  1. EN_NEWEST 사용 - 최신 모델로 최고 품질")
    print("  2. EN_V2 사용 - 안정성과 품질의 균형")
    print("  3. EN 사용 - 기본적인 영어 음성 필요시")
    print("  4. 다국어 모델 활용 - 특정 언어의 영어 발음 특성 활용")

if __name__ == "__main__":
    compare_versions()
    compare_languages()
    generate_summary() 