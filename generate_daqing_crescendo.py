#!/usr/bin/env python3
"""
Generate 3-Strike Crescendo (由轻至重 · 小声到大声) for all 5 types of Buddhist Daqing (大磬/大罄):
Cadence:
- Strike 1: 0.0s (轻推 ~32% 力度) - 润物无声、微波泛起
- Strike 2: 3.0s (中推 ~68% 力度) - 气韵凝聚、声浪推叠
- Strike 3: 6.8s (重推 ~100% 满力度) - 宏鸣入定、驻波长存，尾韵延绵至22s
"""

import numpy as np
from scipy.io import wavfile
import os

SAMPLE_RATE = 48000

def create_felt_mallet_strike(intensity=1.0, softness=0.85, duration=0.06, sample_rate=SAMPLE_RATE):
    total_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, total_samples, endpoint=False)
    
    decay_rate = 60 + 40 * (1.0 - softness)
    env = np.exp(-t * decay_rate)
    noise = np.random.normal(0, 1, total_samples)
    
    thud_freq = 60.0 + 30.0 * (1.0 - softness)
    thud = np.sin(2 * np.pi * thud_freq * t) * env
    friction = noise * env * (0.08 * (1.0 - softness) + 0.02)
    
    return (thud * 0.7 + friction) * intensity

def render_single_daqing_strike(base_freq, duration, modes_config, intensity=1.0, softness=0.85, pan_center=0.0):
    total_samples = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, total_samples, endpoint=False)
    
    left = np.zeros(total_samples, dtype=np.float64)
    right = np.zeros(total_samples, dtype=np.float64)
    
    for (ratio, base_amp, decay_sec, pan_off, beat_hz, beat_depth) in modes_config:
        freq = base_freq * ratio
        env = np.exp(-t / max(0.5, decay_sec) * 3.2)
        
        if beat_hz > 0:
            mod = 1.0 - beat_depth * 0.5 * (1.0 - np.cos(2 * np.pi * beat_hz * t))
        else:
            mod = 1.0
            
        # Non-linear overtone excitation: higher intensity excites higher modes slightly more
        if ratio > 2.0:
            mode_intensity = intensity ** 1.15
        else:
            mode_intensity = intensity
            
        phase = np.random.uniform(0, 2 * np.pi)
        wave = np.sin(2 * np.pi * freq * t + phase) * env * mod * base_amp * mode_intensity
        
        pan = np.clip(pan_center + pan_off, -1.0, 1.0)
        angle = (pan + 1.0) * (np.pi / 4)
        left += wave * np.cos(angle)
        right += wave * np.sin(angle)
        
    attack_len = int(0.025 * SAMPLE_RATE)
    att_env = np.sin(np.linspace(0, np.pi/2, attack_len)) ** 2
    left[:attack_len] *= att_env
    right[:attack_len] *= att_env
    
    strike = create_felt_mallet_strike(intensity=intensity, softness=softness)
    slen = min(len(strike), total_samples)
    s_angle = (np.clip(pan_center, -1.0, 1.0) + 1.0) * (np.pi / 4)
    left[:slen] += strike[:slen] * np.cos(s_angle)
    right[:slen] += strike[:slen] * np.sin(s_angle)
    
    return left, right

def generate_daqing_3_strikes(base_freq, modes_config, softness=0.85, 
                              strike_times=[0.0, 3.0, 6.8], 
                              intensities=[0.32, 0.68, 1.0], 
                              total_duration=22.0):
    total_samples = int(total_duration * SAMPLE_RATE)
    full_left = np.zeros(total_samples, dtype=np.float64)
    full_right = np.zeros(total_samples, dtype=np.float64)
    
    pans = [-0.10, 0.0, 0.10]
    
    for st, inten, p in zip(strike_times, intensities, pans):
        dur = total_duration - st
        l, r = render_single_daqing_strike(base_freq, dur, modes_config, 
                                           intensity=inten, softness=softness, pan_center=p)
        start_idx = int(st * SAMPLE_RATE)
        end_idx = start_idx + len(l)
        full_left[start_idx:end_idx] += l
        full_right[start_idx:end_idx] += r
        
    # Smooth tail fade
    fade_len = int(1.5 * SAMPLE_RATE)
    fade_out = np.linspace(1.0, 0.0, fade_len)
    full_left[-fade_len:] *= fade_out
    full_right[-fade_len:] *= fade_out
    
    return full_left, full_right

def save_wav(filename, left, right, sample_rate=SAMPLE_RATE):
    stereo = np.column_stack([left, right])
    peak = np.max(np.abs(stereo))
    if peak > 0:
        target_peak = 0.89  # -1.0 dBFS
        stereo = stereo * (target_peak / peak)
    int16_data = (stereo * 32767.0).astype(np.int16)
    wavfile.write(filename, sample_rate, int16_data)
    print(f"✅ 大磬三击已生成: {filename} ({len(left)/sample_rate:.1f}s)")

def main():
    sounds_dir = os.path.join(os.path.dirname(__file__), "sounds")
    os.makedirs(sounds_dir, exist_ok=True)
    
    print("🥣 开始合成五种大磬三声（小声到大声 · 渐强三推）...")
    
    # 1. 禅林古铜大磬三击 (108 Hz)
    modes_1 = [
        (0.51, 0.35, 18.0, 0.0, 0.3, 0.20),
        (1.000, 0.88, 19.0, -0.06, 0.38, 0.30),
        (1.0035, 0.78, 18.2, 0.06, 0.38, 0.30),
        (2.760, 0.42, 13.0, -0.15, 0.8, 0.22),
        (2.768, 0.35, 12.5, 0.15, 0.8, 0.22),
        (5.380, 0.20, 7.5, -0.22, 1.4, 0.18),
        (8.850, 0.08, 4.0, 0.25, 0.0, 0.0),
    ]
    l1, r1 = generate_daqing_3_strikes(108.0, modes_1, softness=0.82, total_duration=22.0)
    save_wav(os.path.join(sounds_dir, "daqing_3strikes_01_ancient_bronze.wav"), l1, r1)
    
    # 2. 清修白铜玉磬三击 (216 Hz)
    modes_2 = [
        (1.000, 0.90, 16.5, -0.05, 0.5, 0.25),
        (1.002, 0.82, 16.0,  0.05, 0.5, 0.25),
        (2.745, 0.48, 12.0, -0.12, 1.2, 0.20),
        (2.752, 0.40, 11.5,  0.12, 1.2, 0.20),
        (5.350, 0.25, 7.0,   0.18, 2.0, 0.15),
        (8.750, 0.10, 4.2,  -0.20, 0.0, 0.0),
    ]
    l2, r2 = generate_daqing_3_strikes(216.0, modes_2, softness=0.70, total_duration=20.0)
    save_wav(os.path.join(sounds_dir, "daqing_3strikes_02_pure_resonant.wav"), l2, r2)
    
    # 3. 藏密黑金颂钵大磬三击 (136.1 Hz OM)
    modes_3 = [
        (1.000, 0.92, 20.0, -0.08, 0.28, 0.35),
        (1.0025, 0.85, 19.5, 0.08, 0.28, 0.35),
        (2.780, 0.45, 15.0, -0.16, 0.65, 0.25),
        (2.786, 0.38, 14.5, 0.16, 0.65, 0.25),
        (5.420, 0.22, 9.0,   0.22, 1.1, 0.20),
        (8.950, 0.09, 5.0,  -0.25, 0.0, 0.0),
    ]
    l3, r3 = generate_daqing_3_strikes(136.1, modes_3, softness=0.95, total_duration=24.0)
    save_wav(os.path.join(sounds_dir, "daqing_3strikes_03_tibetan_om.wav"), l3, r3)
    
    # 4. 索尔菲吉奥174Hz安神大磬三击 (174 Hz)
    modes_4 = [
        (0.50,  0.40, 17.0,  0.0,  0.2, 0.15),
        (1.000, 0.95, 18.0, -0.04, 0.35, 0.25),
        (1.0018, 0.88, 17.5, 0.04, 0.35, 0.25),
        (2.710, 0.32, 11.0, -0.12, 0.7, 0.18),
        (5.280, 0.12, 5.5,   0.14, 0.0, 0.0),
    ]
    l4, r4 = generate_daqing_3_strikes(174.0, modes_4, softness=1.0, total_duration=22.0)
    save_wav(os.path.join(sounds_dir, "daqing_3strikes_04_grounding_174.wav"), l4, r4)
    
    # 5. 空灵深潭大磬三击 (120 Hz)
    modes_5 = [
        (1.000, 0.88, 18.5, -0.06, 0.45, 0.28),
        (1.003, 0.78, 18.0,  0.06, 0.45, 0.28),
        (2.750, 0.42, 13.0, -0.15, 0.9, 0.20),
        (5.360, 0.20, 7.5,   0.18, 1.5, 0.15),
        (8.800, 0.07, 3.8,  -0.22, 0.0, 0.0),
    ]
    l5, r5 = generate_daqing_3_strikes(120.0, modes_5, softness=0.88, total_duration=23.0)
    save_wav(os.path.join(sounds_dir, "daqing_3strikes_05_deep_pool.wav"), l5, r5)
    
    print("\n🎉 五种大磬三声（渐强三击）全部合成完成！")

if __name__ == "__main__":
    main()
