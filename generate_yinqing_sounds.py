#!/usr/bin/env python3
"""
Yinqing (引磬/引罄) Sound Generator
Synthesizes 5 distinct types of traditional and therapeutic Buddhist Yinqing bells:
1. 经典禅门引磬 (Classic Bronze Zen Yinqing): 1080Hz 纯正清越、法音庄严
2. 破空晶莹高磬 (Crystalline High Yinqing): 1728Hz 极清极亮、破除昏沉、点亮觉知
3. 温润紫铜引磬 (Warm Soft Yinqing): 852Hz 柔和深静、温润圆融、抚平躁动
4. 禅堂仪轨连击磬 (Double-Strike Ritual Yinqing): 叮-叮 连击余响、仪式开静
5. 528Hz空灵治愈引磬 (Ethereal 528/1056Hz Harmonic Yinqing): 转化奇迹律动、丰富空灵泛音
"""

import numpy as np
from scipy.io import wavfile
import os

SAMPLE_RATE = 48000

def create_metallic_strike(strike_type="metal", sample_rate=SAMPLE_RATE):
    """
    Simulates the microscopic impact of a striker hitting the rim of the bell.
    'metal': crisp metal striker click
    'soft': wrapped/softer striker
    """
    duration = 0.04
    total_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, total_samples, endpoint=False)
    
    # Sharp impulse + high frequency contact noise
    noise = np.random.normal(0, 1, total_samples)
    if strike_type == "metal":
        # Fast exponential decay (15ms)
        env = np.exp(-t * 220)
        # Metallic clink high resonance (e.g. 5.8kHz and 8.2kHz)
        clink = (np.sin(2 * np.pi * 5800 * t) * 0.5 + 
                 np.sin(2 * np.pi * 8400 * t) * 0.4 + 
                 noise * 0.3) * env
        return clink * 0.35
    else: # soft / warm
        env = np.exp(-t * 140)
        clink = (np.sin(2 * np.pi * 3200 * t) * 0.6 + noise * 0.2) * env
        return clink * 0.25

def synthesize_yinqing_single_strike(base_freq, duration, modes_config, strike_type="metal", pan_center=0.0):
    """
    Synthesizes a single Yinqing bell chime with physical modal distribution.
    modes_config: list of (freq_ratio, amp, decay_sec, pan_offset, beat_hz, beat_depth)
    """
    total_samples = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, total_samples, endpoint=False)
    
    left = np.zeros(total_samples, dtype=np.float64)
    right = np.zeros(total_samples, dtype=np.float64)
    
    for (ratio, amp, decay_sec, pan_off, beat_hz, beat_depth) in modes_config:
        freq = base_freq * ratio
        # Mode decay envelope: e^(-t / decay * 4.0)
        env = np.exp(-t / max(0.05, decay_sec) * 3.8)
        
        # Subtle acoustic beating between asymmetrical bell contours
        if beat_hz > 0:
            mod = 1.0 - beat_depth * 0.5 * (1.0 - np.cos(2 * np.pi * beat_hz * t))
        else:
            mod = 1.0
            
        phase = np.random.uniform(0, 2 * np.pi)
        wave = np.sin(2 * np.pi * freq * t + phase) * env * mod * amp
        
        # Panning
        pan = np.clip(pan_center + pan_off, -1.0, 1.0)
        angle = (pan + 1.0) * (np.pi / 4)
        left += wave * np.cos(angle)
        right += wave * np.sin(angle)
        
    # Add metallic strike at beginning
    strike = create_metallic_strike(strike_type=strike_type)
    strike_len = min(len(strike), total_samples)
    strike_pan = np.clip(pan_center, -1.0, 1.0)
    angle_s = (strike_pan + 1.0) * (np.pi / 4)
    left[:strike_len] += strike[:strike_len] * np.cos(angle_s)
    right[:strike_len] += strike[:strike_len] * np.sin(angle_s)
    
    # Smooth fadeout to zero
    fade_len = int(0.5 * SAMPLE_RATE)
    fade_out = np.linspace(1.0, 0.0, fade_len)
    left[-fade_len:] *= fade_out
    right[-fade_len:] *= fade_out
    
    return left, right

def generate_yinqing_1_classic_bronze():
    """1. 经典禅门引磬 (1080 Hz) - 正统寺院清越磬声，余韵庄严"""
    base_freq = 1080.0
    duration = 9.0
    modes = [
        # (ratio, amp, decay_sec, pan_offset, beat_hz, beat_depth)
        (1.000, 0.85, 8.2, -0.05, 1.8, 0.25),
        (1.002, 0.75, 7.8,  0.05, 1.8, 0.25), # 微双音干涉
        (2.740, 0.35, 4.2, -0.15, 2.4, 0.20), # 二阶模态
        (5.380, 0.18, 2.0,  0.18, 3.2, 0.15), # 三阶模态
        (8.920, 0.08, 0.9, -0.22, 0.0, 0.0),  # 高阶亮音
        (13.20, 0.03, 0.4,  0.22, 0.0, 0.0),
    ]
    return synthesize_yinqing_single_strike(base_freq, duration, modes, strike_type="metal")

def generate_yinqing_2_crystalline_high():
    """2. 破空晶莹高磬 (1728 Hz) - 高亢通透，极清极亮，提神止息破昏沉"""
    base_freq = 1728.0
    duration = 7.5
    modes = [
        (1.000, 0.90, 6.8, -0.04, 2.2, 0.20),
        (1.0015, 0.80, 6.5,  0.04, 2.2, 0.20),
        (2.755, 0.28, 3.2, -0.12, 3.0, 0.15),
        (5.420, 0.12, 1.4,  0.15, 0.0, 0.0),
        (8.850, 0.05, 0.6, -0.20, 0.0, 0.0),
    ]
    return synthesize_yinqing_single_strike(base_freq, duration, modes, strike_type="metal")

def generate_yinqing_3_warm_soft():
    """3. 温润紫铜引磬 (852 Hz) - 柔润厚实、眉心轮宁静、无刺耳感"""
    base_freq = 852.0
    duration = 10.0
    modes = [
        (1.000, 0.95, 9.2, -0.05, 1.4, 0.30),
        (1.002, 0.82, 8.8,  0.05, 1.4, 0.30),
        (2.710, 0.30, 4.8, -0.12, 2.0, 0.20),
        (5.310, 0.14, 2.5,  0.14, 2.8, 0.15),
        (8.750, 0.04, 1.1, -0.18, 0.0, 0.0),
    ]
    return synthesize_yinqing_single_strike(base_freq, duration, modes, strike_type="soft")

def generate_yinqing_4_double_strike():
    """4. 禅堂仪轨连击磬 (Double Strike - 叮~叮~~) - 典型禅堂连扣声"""
    base_freq = 1180.0
    duration = 10.5
    modes = [
        (1.000, 0.85, 8.5, -0.05, 1.6, 0.25),
        (1.002, 0.75, 8.0,  0.05, 1.6, 0.25),
        (2.745, 0.32, 4.5, -0.14, 2.2, 0.20),
        (5.390, 0.16, 2.2,  0.16, 0.0, 0.0),
        (8.880, 0.06, 1.0, -0.20, 0.0, 0.0),
    ]
    
    # Strike 1: 轻击 (t=0)
    l1, r1 = synthesize_yinqing_single_strike(base_freq, duration, modes, strike_type="metal", pan_center=-0.1)
    
    # Strike 2: 凝神主击 (t=0.68s)
    strike_2_time = 0.68
    l2, r2 = synthesize_yinqing_single_strike(base_freq, duration - strike_2_time, modes, strike_type="metal", pan_center=0.1)
    
    strike_2_sample = int(strike_2_time * SAMPLE_RATE)
    # Mix together: strike 1 slightly softer (0.65), strike 2 full (1.0)
    total_samples = int(duration * SAMPLE_RATE)
    mix_l = np.zeros(total_samples, dtype=np.float64)
    mix_r = np.zeros(total_samples, dtype=np.float64)
    
    mix_l += l1 * 0.65
    mix_r += r1 * 0.65
    
    len2 = len(l2)
    mix_l[strike_2_sample:strike_2_sample + len2] += l2 * 1.0
    mix_r[strike_2_sample:strike_2_sample + len2] += r2 * 1.0
    
    return mix_l, mix_r

def generate_yinqing_5_harmonic_528():
    """5. 空灵治愈谐波引磬 (528Hz 基音 + 1056Hz 八度清磬 + 纯五度) - 身心共振、疗愈松弛"""
    duration = 11.0
    # 巧妙融合 528Hz (索尔菲吉奥奇迹频率) 与 1056Hz 清越磬峰
    modes = [
        # 528Hz 垫底纯净基频
        (528.0,  0.65, 10.2, -0.05, 1.0, 0.25),
        (528.8,  0.55, 9.8,   0.05, 1.0, 0.25),
        # 1056Hz 主引磬清音 (高八度)
        (1056.0, 0.85, 8.5,  -0.10, 1.8, 0.25),
        (1057.2, 0.70, 8.0,   0.10, 1.8, 0.25),
        # 1584Hz 纯五度纯美泛音
        (1584.0, 0.35, 5.5,   0.15, 2.5, 0.20),
        # 2880Hz 高阶水滴泛音
        (2880.0, 0.15, 2.8,  -0.20, 0.0, 0.0),
        (4750.0, 0.05, 1.2,   0.20, 0.0, 0.0),
    ]
    
    total_samples = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, total_samples, endpoint=False)
    left = np.zeros(total_samples, dtype=np.float64)
    right = np.zeros(total_samples, dtype=np.float64)
    
    for (freq, amp, decay_sec, pan, beat_hz, beat_depth) in modes:
        env = np.exp(-t / decay_sec * 3.6)
        if beat_hz > 0:
            mod = 1.0 - beat_depth * 0.5 * (1.0 - np.cos(2 * np.pi * beat_hz * t))
        else:
            mod = 1.0
        phase = np.random.uniform(0, 2 * np.pi)
        wave = np.sin(2 * np.pi * freq * t + phase) * env * mod * amp
        angle = (pan + 1.0) * (np.pi / 4)
        left += wave * np.cos(angle)
        right += wave * np.sin(angle)
        
    strike = create_metallic_strike(strike_type="soft")
    strike_len = min(len(strike), total_samples)
    left[:strike_len] += strike[:strike_len] * 0.7
    right[:strike_len] += strike[:strike_len] * 0.7
    
    fade_len = int(0.8 * SAMPLE_RATE)
    fade_out = np.linspace(1.0, 0.0, fade_len)
    left[-fade_len:] *= fade_out
    right[-fade_len:] *= fade_out
    
    return left, right

def save_wav(filename, left, right, sample_rate=SAMPLE_RATE):
    stereo = np.column_stack([left, right])
    peak = np.max(np.abs(stereo))
    if peak > 0:
        target_peak = 0.89  # -1.0 dBFS
        stereo = stereo * (target_peak / peak)
    int16_data = (stereo * 32767.0).astype(np.int16)
    wavfile.write(filename, sample_rate, int16_data)
    print(f"✅ 已生成: {filename} ({len(left)/sample_rate:.1f}s)")

def main():
    sounds_dir = os.path.join(os.path.dirname(__file__), "sounds")
    os.makedirs(sounds_dir, exist_ok=True)
    
    print("🔔 开始合成五种引磬之声...")
    
    # 1. 经典禅门引磬
    l1, r1 = generate_yinqing_1_classic_bronze()
    save_wav(os.path.join(sounds_dir, "yinqing_01_classic_bronze.wav"), l1, r1)
    
    # 2. 破空晶莹高磬
    l2, r2 = generate_yinqing_2_crystalline_high()
    save_wav(os.path.join(sounds_dir, "yinqing_02_crystalline_high.wav"), l2, r2)
    
    # 3. 温润紫铜引磬
    l3, r3 = generate_yinqing_3_warm_soft()
    save_wav(os.path.join(sounds_dir, "yinqing_03_warm_soft.wav"), l3, r3)
    
    # 4. 禅堂仪轨连击磬 (Double Strike)
    l4, r4 = generate_yinqing_4_double_strike()
    save_wav(os.path.join(sounds_dir, "yinqing_04_double_strike.wav"), l4, r4)
    
    # 5. 空灵治愈谐波引磬 (528Hz)
    l5, r5 = generate_yinqing_5_harmonic_528()
    save_wav(os.path.join(sounds_dir, "yinqing_05_harmonic_528.wav"), l5, r5)
    
    print("\n🎉 五种引磬音频全部生成完毕！")

if __name__ == "__main__":
    main()
