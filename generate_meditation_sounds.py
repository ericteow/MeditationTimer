#!/usr/bin/env python3
"""
Meditation Sound Generator (禅修大器/宏大冥想之声生成器)
Generates high-fidelity, organic meditation instruments:
1. 庄严大钟 (Grand Temple Bell): 浑厚深沉、晨钟暮鼓、余韵悠长
2. 禅修大磬/颂钵 (Singing Bowl / Large Chime): 纯净空灵、自然拍频(Acoustic Beating)、抚平思绪
3. 冥想铜锣 (Deep Zen Gong): 宏大开阔、空间感强、深邃沉静
4. 清心引磬 (Healing 432Hz Chime): 清脆通透、点亮专注
"""

import numpy as np
from scipy.io import wavfile
import os

SAMPLE_RATE = 48000

def create_modal_voice(duration_sec, modes, sample_rate=SAMPLE_RATE):
    """
    Synthesize resonant acoustic voice from modal decomposition.
    modes: list of tuples (freq, amp, decay_time, pan_lr, beat_freq, beat_depth)
    pan_lr: -1.0 (left) to +1.0 (right)
    """
    total_samples = int(duration_sec * sample_rate)
    t = np.linspace(0, duration_sec, total_samples, endpoint=False)
    
    left = np.zeros(total_samples, dtype=np.float64)
    right = np.zeros(total_samples, dtype=np.float64)
    
    for (freq, amp, decay_t, pan, beat_freq, beat_depth) in modes:
        # Exponential decay for this partial
        decay_curve = np.exp(-t / max(0.1, decay_t) * 3.5)
        
        # Subtle organic amplitude modulation (beating/undulation)
        if beat_freq > 0:
            am = 1.0 - beat_depth * 0.5 * (1.0 - np.cos(2 * np.pi * beat_freq * t))
        else:
            am = 1.0
            
        # Modal sine wave with slight initial phase randomization
        phase = np.random.uniform(0, 2 * np.pi)
        wave = np.sin(2 * np.pi * freq * t + phase) * decay_curve * am * amp
        
        # Stereo panning (constant energy law)
        pan_norm = np.clip(pan, -1.0, 1.0)
        angle = (pan_norm + 1.0) * (np.pi / 4) # 0 to pi/2
        pan_l = np.cos(angle)
        pan_r = np.sin(angle)
        
        left += wave * pan_l
        right += wave * pan_r
        
    return left, right

def generate_grand_temple_bell(duration=16.0, base_freq=96.0):
    """
    1. 禅宗庄严大钟 (Grand Temple Bell)
    特质：木槌击撞瞬间的浑厚低音、青铜巨钟的金属质感与多重自然微拍频，超长驻波共鸣。
    """
    total_samples = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, total_samples, endpoint=False)
    
    modes = [
        # Sub-bass "Hum" tone (钟鸣地振感)
        (base_freq * 0.52, 0.45, 15.0, 0.0, 0.4, 0.25),
        (base_freq * 0.52 + 0.6, 0.40, 14.0, 0.1, 0.4, 0.2),
        
        # Fundamental "Prime" (基频，微双音干涉拍频)
        (base_freq, 0.85, 14.0, -0.05, 0.6, 0.3),
        (base_freq + 0.8, 0.75, 13.5, 0.05, 0.6, 0.3),
        
        # Tierce (小三度/中三度泛音)
        (base_freq * 1.22, 0.45, 10.0, -0.15, 0.8, 0.2),
        
        # Quint (五度泛音)
        (base_freq * 1.51, 0.35, 8.5, 0.15, 1.2, 0.25),
        
        # Octave / Nominal (名义音/高八度)
        (base_freq * 2.01, 0.50, 7.0, -0.2, 1.5, 0.3),
        (base_freq * 2.02, 0.40, 6.5, 0.2, 1.5, 0.3),
        
        # Upper Partials (金属亮泽与撞击清脆度)
        (base_freq * 2.78, 0.30, 4.5, -0.25, 2.0, 0.2),
        (base_freq * 3.42, 0.22, 3.2, 0.25, 2.5, 0.2),
        (base_freq * 4.25, 0.16, 2.2, -0.3, 0.0, 0.0),
        (base_freq * 5.30, 0.10, 1.5, 0.3, 0.0, 0.0),
        (base_freq * 6.80, 0.06, 0.9, -0.35, 0.0, 0.0),
        (base_freq * 8.40, 0.03, 0.6, 0.35, 0.0, 0.0),
    ]
    
    left, right = create_modal_voice(duration, modes)
    
    # 撞击瞬态（木槌击打青铜的低频冲击与轻微噪声）
    strike_len = int(0.08 * SAMPLE_RATE)
    noise = np.random.normal(0, 1, strike_len)
    strike_env = np.exp(-np.linspace(0, 10, strike_len))
    
    strike_sound = noise * strike_env * 0.18
    strike_sub = np.sin(2 * np.pi * 55.0 * t[:strike_len]) * strike_env * 0.35
    
    left[:strike_len] += (strike_sound + strike_sub)
    right[:strike_len] += (strike_sound + strike_sub)
    
    # 柔和淡出
    fade_len = int(0.5 * SAMPLE_RATE)
    fade_out = np.linspace(1.0, 0.0, fade_len)
    left[-fade_len:] *= fade_out
    right[-fade_len:] *= fade_out
    
    return left, right

def generate_singing_bowl_daqing(duration=18.0, base_freq=136.1):
    """
    2. 禅修大磬/西藏颂钵 (Singing Bowl / Large Chime)
    特质：136.1Hz 宇宙心轮/OM Tone，悠扬飘渺、长达18秒的平稳呼吸感拍频。
    """
    modes = [
        # 基频与极其轻柔的同相干涉（Theta波约 3.5Hz 差频，诱导深层冥想）
        (base_freq, 0.90, 16.0, -0.1, 0.25, 0.25),
        (base_freq + 0.35, 0.85, 15.5, 0.1, 0.25, 0.25),
        
        # 环形碗体非线性二阶泛音 (2.76x)
        (base_freq * 2.76, 0.45, 12.0, -0.2, 0.5, 0.2),
        (base_freq * 2.76 + 0.5, 0.38, 11.5, 0.2, 0.5, 0.2),
        
        # 三阶泛音 (5.40x)
        (base_freq * 5.40, 0.22, 7.5, 0.25, 0.8, 0.15),
        
        # 四阶高阶金属泛音 (8.93x)
        (base_freq * 8.93, 0.08, 4.0, -0.25, 1.2, 0.1),
    ]
    
    left, right = create_modal_voice(duration, modes)
    
    # 软羊毛槌触碗瞬间的温润起音
    attack_len = int(0.04 * SAMPLE_RATE)
    att_env = np.sin(np.linspace(0, np.pi/2, attack_len))
    left[:attack_len] *= att_env
    right[:attack_len] *= att_env
    
    fade_len = int(1.0 * SAMPLE_RATE)
    fade_out = np.linspace(1.0, 0.0, fade_len)
    left[-fade_len:] *= fade_out
    right[-fade_len:] *= fade_out
    
    return left, right

def generate_deep_zen_gong(duration=20.0, base_freq=70.0):
    """
    3. 冥想巨型铜锣 (Deep Zen Gong)
    特质：低频深沉如海浪翻涌，能量随时间缓慢释放膨胀(Gong Wash)，浩大而摄人心魄。
    """
    modes = [
        # 超深潜低频 (Sub Bass Drone)
        (base_freq * 0.75, 0.60, 18.0, 0.0, 0.3, 0.35),
        (base_freq, 0.80, 17.0, -0.1, 0.5, 0.3),
        (base_freq + 0.7, 0.70, 16.5, 0.1, 0.5, 0.3),
        
        # 锣面扩散泛音
        (base_freq * 2.15, 0.40, 12.0, -0.2, 1.0, 0.25),
        (base_freq * 3.12, 0.32, 9.0, 0.25, 1.5, 0.25),
        (base_freq * 4.65, 0.25, 6.0, -0.3, 2.2, 0.2),
        (base_freq * 6.20, 0.18, 4.5, 0.3, 3.0, 0.2),
        (base_freq * 8.85, 0.10, 3.0, -0.35, 4.0, 0.15),
    ]
    
    left, right = create_modal_voice(duration, modes)
    
    swell_len = int(0.35 * SAMPLE_RATE)
    swell_env = np.sin(np.linspace(0.2, np.pi/2, swell_len))
    left[:swell_len] *= swell_env
    right[:swell_len] *= swell_env
    
    fade_len = int(1.5 * SAMPLE_RATE)
    fade_out = np.linspace(1.0, 0.0, fade_len)
    left[-fade_len:] *= fade_out
    right[-fade_len:] *= fade_out
    
    return left, right

def generate_ambient_chime(duration=12.0, base_freq=432.0):
    """
    4. 432Hz 治愈引磬 (Healing 432Hz Chime)
    特质：A=432Hz 自然调和律，清澈通透，适合冥想启程或收尾唤醒。
    """
    modes = [
        (base_freq, 0.85, 10.0, -0.05, 0.8, 0.2),
        (base_freq + 1.2, 0.75, 9.5, 0.05, 0.8, 0.2),
        (base_freq * 2.0, 0.35, 6.0, 0.15, 1.2, 0.15),
        (base_freq * 3.0, 0.18, 4.0, -0.15, 1.8, 0.1),
        (base_freq * 4.15, 0.08, 2.5, 0.2, 0.0, 0.0),
    ]
    
    left, right = create_modal_voice(duration, modes)
    
    fade_len = int(0.8 * SAMPLE_RATE)
    fade_out = np.linspace(1.0, 0.0, fade_len)
    left[-fade_len:] *= fade_out
    right[-fade_len:] *= fade_out
    
    return left, right

def save_wav(filename, left, right, sample_rate=SAMPLE_RATE):
    """Normalize cleanly to -1.0 dB peak and save as 16-bit stereo WAV."""
    stereo = np.column_stack([left, right])
    peak = np.max(np.abs(stereo))
    if peak > 0:
        target_peak = 0.89  # -1.0 dBFS headroom
        stereo = stereo * (target_peak / peak)
    
    int16_data = (stereo * 32767.0).astype(np.int16)
    wavfile.write(filename, sample_rate, int16_data)
    print(f"✅ 已生成: {filename} (时长: {len(left)/sample_rate:.1f}s, 采样率: {sample_rate}Hz)")

def main():
    sounds_dir = os.path.join(os.path.dirname(__file__), "sounds")
    os.makedirs(sounds_dir, exist_ok=True)
    
    print("🔔 开始合成冥想大器之声...")
    
    # 1. 庄严大钟 (Grand Temple Bell)
    l1, r1 = generate_grand_temple_bell(duration=16.0, base_freq=96.0)
    save_wav(os.path.join(sounds_dir, "01_grand_temple_bell.wav"), l1, r1)
    
    # 2. 禅修大磬/颂钵 (Singing Bowl / Large Chime)
    l2, r2 = generate_singing_bowl_daqing(duration=18.0, base_freq=136.1)
    save_wav(os.path.join(sounds_dir, "02_singing_bowl_daqing.wav"), l2, r2)
    
    # 3. 冥想巨型铜锣 (Deep Zen Gong)
    l3, r3 = generate_deep_zen_gong(duration=20.0, base_freq=70.0)
    save_wav(os.path.join(sounds_dir, "03_deep_zen_gong.wav"), l3, r3)
    
    # 4. 432Hz 治愈引磬 (432Hz Ambient Chime)
    l4, r4 = generate_ambient_chime(duration=12.0, base_freq=432.0)
    save_wav(os.path.join(sounds_dir, "04_healing_432hz_chime.wav"), l4, r4)
    
    print("\n🎉 全部音频生成完成！位于 sounds/ 目录中。")

if __name__ == "__main__":
    main()
