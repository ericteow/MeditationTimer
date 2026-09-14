#!/usr/bin/env python3
"""
Generate 5 Yinqing bell sounds across 3 distinctly graded dynamics:
- small  (小声 / Soft):   Body RMS ~ -30.5 dBFS, Peak ~ -18.5 dBFS (gentle, quiet, whisper strike)
- medium (中声 / Medium): Body RMS ~ -20.4 dBFS, Peak ~ -8.0 dBFS  (+10 dB louder, balanced presence)
- loud   (大声 / Loud):   Body RMS ~ -11.4 dBFS, Peak ~ -0.9 dBFS  (+9 dB louder, full powerful ringing)

Total: 5 types * 3 dynamics = 15 tracks.
Encodes to high-quality MP3 (192kbps) using ffmpeg.
"""

import os
import wave
import subprocess
import numpy as np

SAMPLE_RATE = 48000

# Dynamics config: (volume_suffix, target_body_rms, strike_factor, en_label, zh_label)
DYNAMICS = [
    ("small", 0.030, 0.25, "Soft", "小声"),
    ("medium", 0.095, 0.55, "Medium", "中声"),
    ("loud", 0.270, 1.00, "Loud", "大声"),
]

def create_metallic_strike(strike_type="metal", intensity=1.0, sample_rate=SAMPLE_RATE):
    """
    Simulates strike impact transient.
    """
    duration = 0.035
    total_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, total_samples, endpoint=False)
    noise = np.random.normal(0, 1, total_samples)

    if strike_type == "metal":
        decay = 180 + 120 * intensity
        env = np.exp(-t * decay)
        clink = (np.sin(2 * np.pi * 5800 * t) * (0.25 + 0.35 * intensity) + 
                 np.sin(2 * np.pi * 8400 * t) * (0.15 + 0.35 * intensity) + 
                 noise * (0.10 + 0.20 * intensity)) * env
        return clink * (0.12 + 0.25 * intensity)
    else:  # soft / warm striker
        decay = 120 + 80 * intensity
        env = np.exp(-t * decay)
        clink = (np.sin(2 * np.pi * 3200 * t) * (0.35 + 0.30 * intensity) + 
                 noise * (0.08 + 0.12 * intensity)) * env
        return clink * (0.10 + 0.18 * intensity)

def synthesize_yinqing_single_strike(base_freq, duration, modes_config, strike_type="metal", intensity=1.0, pan_center=0.0):
    total_samples = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, total_samples, endpoint=False)
    
    left = np.zeros(total_samples, dtype=np.float64)
    right = np.zeros(total_samples, dtype=np.float64)
    
    for (ratio, amp, decay_sec, pan_off, beat_hz, beat_depth) in modes_config:
        freq = base_freq * ratio
        # Non-linear excitation: higher partials excite more strongly when struck harder
        harmonic_scale = 1.0 if ratio <= 1.05 else (0.45 + 0.55 * intensity)
        env = np.exp(-t / max(0.05, decay_sec) * 3.8)
        
        if beat_hz > 0:
            mod = 1.0 - beat_depth * 0.5 * (1.0 - np.cos(2 * np.pi * beat_hz * t))
        else:
            mod = 1.0
            
        phase = np.random.uniform(0, 2 * np.pi)
        wave_comp = np.sin(2 * np.pi * freq * t + phase) * env * mod * amp * harmonic_scale
        
        pan = np.clip(pan_center + pan_off, -1.0, 1.0)
        angle = (pan + 1.0) * (np.pi / 4)
        left += wave_comp * np.cos(angle)
        right += wave_comp * np.sin(angle)
        
    strike = create_metallic_strike(strike_type=strike_type, intensity=intensity)
    strike_len = min(len(strike), total_samples)
    strike_pan = np.clip(pan_center, -1.0, 1.0)
    angle_s = (strike_pan + 1.0) * (np.pi / 4)
    left[:strike_len] += strike[:strike_len] * np.cos(angle_s)
    right[:strike_len] += strike[:strike_len] * np.sin(angle_s)
    
    fade_len = int(0.5 * SAMPLE_RATE)
    fade_out = np.linspace(1.0, 0.0, fade_len)
    left[-fade_len:] *= fade_out
    right[-fade_len:] *= fade_out
    
    return left, right

# 1. 经典禅门引磬 (1080Hz)
def gen_1_classic_bronze(intensity=1.0):
    base_freq = 1080.0
    duration = 9.0
    modes = [
        (1.000, 0.85, 8.2, -0.05, 1.8, 0.25),
        (1.002, 0.75, 7.8,  0.05, 1.8, 0.25),
        (2.740, 0.35, 4.2, -0.15, 2.4, 0.20),
        (5.380, 0.18, 2.0,  0.18, 3.2, 0.15),
        (8.920, 0.08, 0.9, -0.22, 0.0, 0.0),
        (13.20, 0.03, 0.4,  0.22, 0.0, 0.0),
    ]
    return synthesize_yinqing_single_strike(base_freq, duration, modes, strike_type="metal", intensity=intensity)

# 2. 破空晶莹高磬 (1728Hz)
def gen_2_crystalline_high(intensity=1.0):
    base_freq = 1728.0
    duration = 7.5
    modes = [
        (1.000, 0.90, 6.8, -0.04, 2.2, 0.20),
        (1.0015, 0.80, 6.5,  0.04, 2.2, 0.20),
        (2.755, 0.28, 3.2, -0.12, 3.0, 0.15),
        (5.420, 0.12, 1.4,  0.15, 0.0, 0.0),
        (8.850, 0.05, 0.6, -0.20, 0.0, 0.0),
    ]
    return synthesize_yinqing_single_strike(base_freq, duration, modes, strike_type="metal", intensity=intensity)

# 3. 温润紫铜引磬 (852Hz)
def gen_3_warm_soft(intensity=1.0):
    base_freq = 852.0
    duration = 10.0
    modes = [
        (1.000, 0.95, 9.2, -0.05, 1.4, 0.30),
        (1.002, 0.82, 8.8,  0.05, 1.4, 0.30),
        (2.710, 0.30, 4.8, -0.12, 2.0, 0.20),
        (5.310, 0.14, 2.5,  0.14, 2.8, 0.15),
        (8.750, 0.04, 1.1, -0.18, 0.0, 0.0),
    ]
    return synthesize_yinqing_single_strike(base_freq, duration, modes, strike_type="soft", intensity=intensity)

# 4. 禅堂仪轨连击磬 (Double Strike - 叮~叮~~)
def gen_4_double_strike(intensity=1.0):
    base_freq = 1180.0
    duration = 10.5
    modes = [
        (1.000, 0.85, 8.5, -0.05, 1.6, 0.25),
        (1.002, 0.75, 8.0,  0.05, 1.6, 0.25),
        (2.745, 0.32, 4.5, -0.14, 2.2, 0.20),
        (5.390, 0.16, 2.2,  0.16, 0.0, 0.0),
        (8.880, 0.06, 1.0, -0.20, 0.0, 0.0),
    ]
    
    # Strike 1: 轻击
    l1, r1 = synthesize_yinqing_single_strike(base_freq, duration, modes, strike_type="metal", intensity=intensity*0.7, pan_center=-0.1)
    # Strike 2: 主击 (t=0.68s)
    strike_2_time = 0.68
    l2, r2 = synthesize_yinqing_single_strike(base_freq, duration - strike_2_time, modes, strike_type="metal", intensity=intensity, pan_center=0.1)
    
    strike_2_sample = int(strike_2_time * SAMPLE_RATE)
    total_samples = int(duration * SAMPLE_RATE)
    mix_l = np.zeros(total_samples, dtype=np.float64)
    mix_r = np.zeros(total_samples, dtype=np.float64)
    
    mix_l += l1 * 0.65
    mix_r += r1 * 0.65
    
    len2 = len(l2)
    mix_l[strike_2_sample:strike_2_sample + len2] += l2 * 1.0
    mix_r[strike_2_sample:strike_2_sample + len2] += r2 * 1.0
    
    return mix_l, mix_r

# 5. 空灵治愈谐波引磬 (528Hz)
def gen_5_harmonic_528(intensity=1.0):
    duration = 11.0
    modes = [
        (528.0,  0.65, 10.2, -0.05, 1.0, 0.25),
        (528.8,  0.55, 9.8,   0.05, 1.0, 0.25),
        (1056.0, 0.85, 8.5,  -0.10, 1.8, 0.25),
        (1057.2, 0.70, 8.0,   0.10, 1.8, 0.25),
        (1584.0, 0.35, 5.5,   0.15, 2.5, 0.20),
        (2880.0, 0.15, 2.8,  -0.20, 0.0, 0.0),
        (4750.0, 0.05, 1.2,   0.20, 0.0, 0.0),
    ]
    total_samples = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, total_samples, endpoint=False)
    left = np.zeros(total_samples, dtype=np.float64)
    right = np.zeros(total_samples, dtype=np.float64)
    
    for (freq, amp, decay_sec, pan, beat_hz, beat_depth) in modes:
        harmonic_scale = 1.0 if freq <= 600.0 else (0.45 + 0.55 * intensity)
        env = np.exp(-t / decay_sec * 3.6)
        if beat_hz > 0:
            mod = 1.0 - beat_depth * 0.5 * (1.0 - np.cos(2 * np.pi * beat_hz * t))
        else:
            mod = 1.0
        phase = np.random.uniform(0, 2 * np.pi)
        wave_comp = np.sin(2 * np.pi * freq * t + phase) * env * mod * amp * harmonic_scale
        angle = (pan + 1.0) * (np.pi / 4)
        left += wave_comp * np.cos(angle)
        right += wave_comp * np.sin(angle)
        
    strike = create_metallic_strike(strike_type="soft", intensity=intensity)
    strike_len = min(len(strike), total_samples)
    left[:strike_len] += strike[:strike_len] * 0.6
    right[:strike_len] += strike[:strike_len] * 0.6
    
    fade_len = int(0.8 * SAMPLE_RATE)
    fade_out = np.linspace(1.0, 0.0, fade_len)
    left[-fade_len:] *= fade_out
    right[-fade_len:] *= fade_out
    
    return left, right

GENERATORS = [
    ("yinqing_01_classic_bronze", gen_1_classic_bronze),
    ("yinqing_02_crystalline_high", gen_2_crystalline_high),
    ("yinqing_03_warm_soft", gen_3_warm_soft),
    ("yinqing_04_double_strike", gen_4_double_strike),
    ("yinqing_05_harmonic_528", gen_5_harmonic_528),
]

def soft_limit(stereo, max_peak=0.92):
    """
    Smooth limiter that gently compresses only peaks above 0.70 without clipping or distorting.
    """
    peak = np.max(np.abs(stereo))
    if peak > max_peak:
        threshold = 0.70
        mask = np.abs(stereo) > threshold
        excess = (np.abs(stereo) - threshold) / (peak - threshold)
        compressed = threshold + (max_peak - threshold) * np.tanh(excess * 1.6)
        out = stereo.copy()
        out[mask] = np.sign(stereo[mask]) * compressed[mask]
        return out
    return stereo

def write_wav_file(wav_path, stereo_float):
    int16_data = np.clip(stereo_float * 32767.0, -32768, 32767).astype(np.int16)
    with wave.open(wav_path, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(int16_data.tobytes())

def save_and_convert(wav_path, mp3_path, stereo_signal):
    write_wav_file(wav_path, stereo_signal)
    
    # ffmpeg convert to 192k mp3
    cmd = [
        "ffmpeg", "-y", "-i", wav_path,
        "-codec:a", "libmp3lame", "-b:a", "192k", mp3_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if os.path.exists(wav_path):
        os.remove(wav_path)

def main():
    sounds_dir = os.path.join(os.path.dirname(__file__), "sounds")
    os.makedirs(sounds_dir, exist_ok=True)
    
    print("🔔 开始为5款引磬重构3种声调（精准声学响度分级，小声/中声/大声差距明显）...")
    
    for base_name, gen_func in GENERATORS:
        print(f"\n正在处理: {base_name}")
        for dyn_suffix, target_body_rms, strike_factor, en_label, zh_label in DYNAMICS:
            l, r = gen_func(intensity=strike_factor)
            stereo = np.column_stack([l, r])
            
            # Measure sustain body RMS (0.1s to 2.5s)
            body = stereo[int(0.10 * SAMPLE_RATE):int(2.5 * SAMPLE_RATE)]
            cur_body_rms = np.sqrt(np.mean(body**2))
            
            # Scale directly by target Body RMS
            gain = target_body_rms / max(1e-6, cur_body_rms)
            scaled = stereo * gain
            
            # Soft limit transient to max 0.92 (-0.7 dBFS)
            limited = soft_limit(scaled, max_peak=0.92)
            
            wav_path = os.path.join(sounds_dir, f"{base_name}_{dyn_suffix}.wav")
            mp3_path = os.path.join(sounds_dir, f"{base_name}_{dyn_suffix}.mp3")
            save_and_convert(wav_path, mp3_path, limited)
            
            peak = np.max(np.abs(limited))
            b = limited[int(0.10 * SAMPLE_RATE):int(2.5 * SAMPLE_RATE)]
            measured_body_rms = np.sqrt(np.mean(b**2))
            print(f"  ✓ {dyn_suffix:<6} ({zh_label}): Peak={peak:.3f} ({20*np.log10(peak):>5.1f} dBFS) | Body RMS={measured_body_rms:.3f} ({20*np.log10(measured_body_rms):>5.1f} dBFS)")

    print("\n🎉 全部 15 首引磬音频（小声、中声、大声）重新生成与转码完毕！")

if __name__ == "__main__":
    main()
