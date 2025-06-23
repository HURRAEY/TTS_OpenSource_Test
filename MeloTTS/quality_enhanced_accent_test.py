from melo.api import TTS
import os

# 테스트할 샘플 문장
sample_sentences = [
    "Hello, this is a test of English accent quality.",
    "The weather is beautiful today.",
    "I love this amazing technology.",
    "Thank you very much for your attention.",
    "Have a wonderful day ahead!"
]

# 국가별 영어 억양(speaker_id)
accent_speakers = {
    'EN-Default': '기본',
    'EN-US': '미국',
    'EN-BR': '영국',
    'EN_INDIA': '인도',
    'EN-AU': '호주',
}

# 음질 향상을 위한 파라미터 조합들
quality_settings = {
    'standard': {
        'noise_scale': 0.6,
        'noise_scale_w': 0.8,
        'sdp_ratio': 0.2,
        'speed': 1.0
    },
    'high_quality': {
        'noise_scale': 0.4,  # 더 낮은 노이즈 = 더 깔끔한 음성
        'noise_scale_w': 0.6,  # 더 낮은 노이즈 = 더 안정적인 음성
        'sdp_ratio': 0.1,  # 더 낮은 SDP = 더 자연스러운 음성
        'speed': 1.0
    },
    'ultra_quality': {
        'noise_scale': 0.2,  # 매우 낮은 노이즈
        'noise_scale_w': 0.4,  # 매우 낮은 노이즈
        'sdp_ratio': 0.05,  # 매우 낮은 SDP
        'speed': 0.9  # 약간 느리게 = 더 명확한 발음
    },
    'balanced': {
        'noise_scale': 0.5,
        'noise_scale_w': 0.7,
        'sdp_ratio': 0.15,
        'speed': 1.0
    }
}

output_dir = "quality_enhanced_accent_test"
os.makedirs(output_dir, exist_ok=True)

print("🎤 음질 향상된 국가별 영어 억양 테스트 시작...")
print("📝 테스트 문장:")
for i, sentence in enumerate(sample_sentences, 1):
    print(f"  {i:2d}. {sentence}")

# TTS 인스턴스 생성 (영어)
tts = TTS(language='EN', device='auto')
speaker_ids = tts.hps.data.spk2id

# 각 액센트별로 다양한 품질 설정으로 테스트
for speaker, desc in accent_speakers.items():
    print(f"\n🔊 {desc}({speaker}) 억양 테스트 중...")
    spk_id = speaker_ids[speaker]
    
    for quality_name, params in quality_settings.items():
        print(f"  📊 {quality_name} 품질 설정 적용 중...")
        accent_dir = os.path.join(output_dir, f"{speaker}_{quality_name}")
        os.makedirs(accent_dir, exist_ok=True)
        
        for idx, sentence in enumerate(sample_sentences, 1):
            output_path = os.path.join(accent_dir, f"sample_{idx:02d}.wav")
            try:
                print(f"    생성 중: {sentence[:30]}...")
                tts.tts_to_file(
                    text=sentence,
                    speaker_id=spk_id,
                    output_path=output_path,
                    speed=params['speed'],
                    noise_scale=params['noise_scale'],
                    noise_scale_w=params['noise_scale_w'],
                    sdp_ratio=params['sdp_ratio'],
                    quiet=True,
                )
                print(f"    ✅ 완료: {output_path}")
            except Exception as e:
                print(f"    ❌ 오류: {e}")
        
        # 파일 크기 확인
        wav_files = [f for f in os.listdir(accent_dir) if f.endswith('.wav')]
        total_size = sum(os.path.getsize(os.path.join(accent_dir, f)) for f in wav_files)
        print(f"    📊 {quality_name}: {len(wav_files)}개 파일, 총 {total_size:,} bytes")

print(f"\n🎉 모든 음질 향상 테스트 완료!")
print(f"📁 결과 파일 위치: {output_dir}")

# 최종 분석
print(f"\n📈 최종 품질 설정 분석:")
for quality_name, params in quality_settings.items():
    print(f"  {quality_name}:")
    print(f"    - noise_scale: {params['noise_scale']}")
    print(f"    - noise_scale_w: {params['noise_scale_w']}")
    print(f"    - sdp_ratio: {params['sdp_ratio']}")
    print(f"    - speed: {params['speed']}")
    print(f"    - 예상 효과: {'고품질' if quality_name == 'ultra_quality' else '균형' if quality_name == 'balanced' else '표준' if quality_name == 'standard' else '향상된 품질'}")

print(f"\n💡 권장사항:")
print(f"  - 최고 품질: ultra_quality 설정")
print(f"  - 균형잡힌 선택: balanced 설정")
print(f"  - 빠른 처리: standard 설정") 