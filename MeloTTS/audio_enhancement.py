import librosa
import soundfile as sf
import numpy as np
import os
from scipy import signal
from scipy.signal import butter, filtfilt

def enhance_audio_quality(audio_path, output_path, enhancement_type='standard'):
    """
    오디오 품질 향상 함수
    
    Args:
        audio_path: 입력 오디오 파일 경로
        output_path: 출력 오디오 파일 경로
        enhancement_type: 향상 타입 ('standard', 'high', 'ultra')
    """
    
    # 오디오 로드
    audio, sr = librosa.load(audio_path, sr=None)
    
    if enhancement_type == 'standard':
        # 기본 향상
        enhanced_audio = apply_basic_enhancement(audio, sr)
    elif enhancement_type == 'high':
        # 고급 향상
        enhanced_audio = apply_advanced_enhancement(audio, sr)
    elif enhancement_type == 'ultra':
        # 최고급 향상
        enhanced_audio = apply_ultra_enhancement(audio, sr)
    else:
        enhanced_audio = audio
    
    # 파일 저장
    sf.write(output_path, enhanced_audio, sr)
    return enhanced_audio

def apply_basic_enhancement(audio, sr):
    """기본 음질 향상"""
    # 노이즈 감소
    audio = reduce_noise(audio, sr)
    # 볼륨 정규화
    audio = normalize_volume(audio)
    return audio

def apply_advanced_enhancement(audio, sr):
    """고급 음질 향상"""
    # 기본 향상 적용
    audio = apply_basic_enhancement(audio, sr)
    # 주파수 보정
    audio = frequency_correction(audio, sr)
    # 리버브 감소
    audio = reduce_reverb(audio, sr)
    return audio

def apply_ultra_enhancement(audio, sr):
    """최고급 음질 향상"""
    # 고급 향상 적용
    audio = apply_advanced_enhancement(audio, sr)
    # 스펙트럼 보정
    audio = spectral_correction(audio, sr)
    # 클리핑 방지
    audio = prevent_clipping(audio)
    return audio

def reduce_noise(audio, sr):
    """노이즈 감소"""
    # 고주파 노이즈 필터링
    nyquist = sr / 2
    cutoff = 8000  # 8kHz 이상 제거
    b, a = butter(4, cutoff / nyquist, btype='low')
    filtered = filtfilt(b, a, audio)
    return filtered

def normalize_volume(audio):
    """볼륨 정규화"""
    # RMS 정규화
    rms = np.sqrt(np.mean(audio**2))
    target_rms = 0.1
    if rms > 0:
        audio = audio * (target_rms / rms)
    return audio

def frequency_correction(audio, sr):
    """주파수 보정"""
    # 스펙트럼 서브트랙션으로 노이즈 제거
    stft = librosa.stft(audio)
    magnitude = np.abs(stft)
    phase = np.angle(stft)
    
    # 노이즈 스펙트럼 추정 (첫 0.1초)
    noise_frames = int(0.1 * sr / 512)
    noise_spectrum = np.mean(magnitude[:, :noise_frames], axis=1)
    
    # 스펙트럼 서브트랙션
    enhanced_magnitude = magnitude - noise_spectrum[:, np.newaxis]
    enhanced_magnitude = np.maximum(enhanced_magnitude, 0)
    
    # ISTFT로 복원
    enhanced_stft = enhanced_magnitude * np.exp(1j * phase)
    enhanced_audio = librosa.istft(enhanced_stft)
    
    return enhanced_audio

def reduce_reverb(audio, sr):
    """리버브 감소"""
    # 간단한 에코 캔슬레이션
    delay_samples = int(0.05 * sr)  # 50ms 딜레이
    decay = 0.3
    
    # 딜레이된 신호 생성
    delayed = np.zeros_like(audio)
    delayed[delay_samples:] = audio[:-delay_samples] * decay
    
    # 원본에서 딜레이된 신호 제거
    enhanced = audio - delayed
    
    return enhanced

def spectral_correction(audio, sr):
    """스펙트럼 보정"""
    # 멜 스펙트로그램 계산
    mel_spec = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=128)
    
    # 스펙트럼 정규화
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
    
    # 스펙트럼 서브트랙션
    mel_spec_enhanced = mel_spec_db - np.mean(mel_spec_db, axis=1, keepdims=True)
    
    # 다시 파워로 변환
    mel_spec_enhanced = librosa.db_to_power(mel_spec_enhanced)
    
    # ISTFT로 복원 (근사)
    enhanced_audio = librosa.feature.inverse.mel_to_audio(
        mel_spec_enhanced, sr=sr, n_iter=32
    )
    
    return enhanced_audio

def prevent_clipping(audio):
    """클리핑 방지"""
    # 소프트 클리핑
    threshold = 0.95
    audio = np.tanh(audio / threshold) * threshold
    return audio

def batch_enhance_audio(input_dir, output_dir, enhancement_type='standard'):
    """배치 오디오 향상"""
    os.makedirs(output_dir, exist_ok=True)
    
    wav_files = [f for f in os.listdir(input_dir) if f.endswith('.wav')]
    
    for wav_file in wav_files:
        input_path = os.path.join(input_dir, wav_file)
        output_path = os.path.join(output_dir, f"enhanced_{wav_file}")
        
        try:
            enhance_audio_quality(input_path, output_path, enhancement_type)
            print(f"✅ 향상 완료: {wav_file}")
        except Exception as e:
            print(f"❌ 오류: {wav_file} - {e}")

if __name__ == "__main__":
    # 예시 사용법
    print("🎵 오디오 품질 향상 도구")
    print("사용법: batch_enhance_audio('입력폴더', '출력폴더', 'enhancement_type')")
    print("enhancement_type: 'standard', 'high', 'ultra'") 