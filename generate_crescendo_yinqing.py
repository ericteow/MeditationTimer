#!/usr/bin/env python3
"""
Generate 3-strike crescendo Yinqing (引磬三击：由轻至重 / 小声到大声)
Classic Zen ritual cadence:
Strike 1: Soft (轻扣微鸣，凝神摄心) ~30% volume, warm attack
Strike 2: Medium (次扣渐扬，正念凝聚) ~65% volume, clear metallic
Strike 3: Strong (重扣宏鸣，空灵入定) ~100% volume, full resonance & long tail
"""

import numpy as np
from scipy.io import wavfile
import os

SAMPLE_RATE = 48000

def create_metallic_strike(intensity=1.0, sample_rate=SAMPLE_RATE):
    """
    Simulates strike transient. 
    intensity: 0.0 to 1.0. 
    Lower intensity = softer contact, less harsh high-frequency noise.
    Higher intensity = crisp metallic transient with rich high clink.
    """
    duration = 0.035
    total_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, total_samples, endpoint=False)
    
    decay_rate = 140 + 120 * intensity
    env = np.exp(-t * decay_rate)
    noise = np.random.normal(0, 1, total_samples)
    
    # As intensity increases, higher partials in the strike emerge
    clink = (np.sin(2 * np.pi * 3200 * t) * (0.8 - 0.2 * intensity) +
             np.sin(2 * np.pi * 5800 * t) * (0.3 + 0.4 * intensity) +
             np.sin(2 * np.pi * 8400 * t) * (0.1 + 0.4 * intensity) +
             noise * (0.15 + 0.25 * intensity)) * env
             
    return clink * (0.2 + 0.25 * intensity)

def render_single_strike(base_freq, duration, intensity, pan_center=0.0):
    total_samples = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, total_samples, endpoint=False)
    
    left = np.zeros(total_samples, dtype=np.float64)
    right = np.zeros(total_samples, dtype=np.float64)
    
    # Dynamic modal ratios: stronger strike excites higher partials more strongly (non-linear acoustic response)
    modes = [
        # (ratio, base_amp, decay_sec, pan_offset, beat_hz, beat_depth)
        (1.000, 0.85, 8.5, -0.04, 1.8, 0.25),
        (1.002, 0.75, 8.0,  0.04, 1.8, 0.25),
        (2.740, 0.35 * (0.7 + 0.5 * intensity), 4.5, -0.12, 2.4, 0.20),
        (5.380, 0.18 * (0.4 + 0.8 * intensity), 2.2,  0.15, 3.2, 0.15),
        (8.920, 0.08 * (0.2 + 1.0 * intensity), 1.0, -0.18, 0.0, 0.0),
        (13.20, 0.03 * (0.1 + 1.2 * intensity), 0.5,  0.20, 0.0, 0.0),
    ]
    
    for (ratio, amp, decay_sec, pan_off, beat_hz, beat_depth) in modes:
        freq = base_freq * ratio
        env = np.exp(-t / max(0.05, decay_sec) * 3.8)
        if beat_hz > 0:
            mod = 1.0 - beat_depth * 0.5 * (1.0 - np.cos(2 * np.pi * beat_hz * t))
        else:
            mod = 1.0
        phase = np.random.uniform(0, 2 * np.pi)
        # Scale amplitude by intensity
        wave = np.sin(2 * np.pi * freq * t + phase) * env * mod * amp * intensity
        
        pan = np.clip(pan_center + pan_off, -1.0, 1.0)
        angle = (pan + 1.0) * (np.pi / 4)
        left += wave * np.cos(angle)
        right += wave * np.sin(angle)
        
    strike = create_metallic_strike(intensity=intensity)
    slen = min(len(strike), total_samples)
    s_angle = (np.clip(pan_center, -1.0, 1.0) + 1.0) * (np.pi / 4)
    left[:slen] += strike[:slen] * np.cos(s_angle)
    right[:slen] += strike[:slen] * np.sin(s_angle)
    
    return left, right

def generate_yinqing_3_strikes(base_freq=1080.0, strike_times=[0.0, 2.5, 5.5], intensities=[0.30, 0.65, 1.0], total_duration=16.0):
    """
    strike_times: [t1, t2, t3] in seconds
    intensities: [i1, i2, i3] scale factors
    total_duration: length of the entire piece
    """
    total_samples = int(total_duration * SAMPLE_RATE)
    full_left = np.zeros(total_samples, dtype=np.float64)
    full_right = np.zeros(total_samples, dtype=np.float64)
    
    pans = [-0.08, 0.0, 0.08] # Subtle spatial movement from left to center to wide
    
    for idx, (st, inten, p) in enumerate(zip(strike_times, intensities, pans)):
        dur = total_duration - st
        l, r = render_single_strike(base_freq, dur, intensity=inten, pan_center=p)
        start_sample = int(st * SAMPLE_RATE)
        end_sample = start_sample + len(l)
        full_left[start_sample:end_sample] += l
        full_right[start_sample:end_sample] += r
        
    # Smooth fade out
    fade_len = int(1.0 * SAMPLE_RATE)
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
    print(f"✅ 生成成功: {filename} ({len(left)/sample_rate:.1f}s)")

if __name__ == "__main__":
    sounds_dir = os.path.join(os.path.dirname(__file__), "sounds")
    os.makedirs(sounds_dir, exist_ok=True)
    
    print("🔔 开始合成引磬三击（小声到大声）...")
    
    # 1. 经典禅堂三击 (正统黄铜引磬 1080Hz，节拍庄重沉静)
    # 第1声 0.0s (轻度 ~0.30)，第2声 2.5s (中度 ~0.65)，第3声 5.5s (重度 ~1.00，余音延绵至16s)
    l1, r1 = generate_yinqing_3_strikes(base_freq=1080.0, strike_times=[0.0, 2.5, 5.5], intensities=[0.30, 0.65, 1.0], total_duration=16.0)
    save_wav(os.path.join(sounds_dir, "yinqing_3strikes_crescendo_classic.wav"), l1, r1)
    
    # 2. 紧凑清越三击 (1200Hz，间隔更紧凑，适合短时静心/快速开静)
    # 第1声 0.0s, 第2声 1.6s, 第3声 3.6s, 余音至12s
    l2, r2 = generate_yinqing_3_strikes(base_freq=1200.0, strike_times=[0.0, 1.6, 3.6], intensities=[0.28, 0.60, 1.0], total_duration=13.0)
    save_wav(os.path.join(sounds_dir, "yinqing_3strikes_crescendo_crisp.wav"), l2, r2)

    # 3. 温润紫铜三击 (852Hz 柔和深静，渐强不喧哗，舒缓平和)
    l3, r3 = generate_yinqing_3_strikes(base_freq=852.0, strike_times=[0.0, 2.6, 5.8], intensities=[0.32, 0.68, 1.0], total_duration=16.5)
    save_wav(os.path.join(sounds_dir, "yinqing_3strikes_crescendo_warm.wav"), l3, r3)

    print("🎉 引磬渐强三击全部生成完成！")
