#!/usr/bin/env python3
"""
Generate 5 Distinct Types of Buddhist Daqing (大磬/大罄) Sounds:
1. 禅林古铜大磬 (Ancient Bronze Monastery Daqing): 108Hz 沉浑古朴、百八烦恼寂灭、超长驻波(20s)
2. 清修白铜玉磬 (Pure Resonant White-Bronze Daqing): 216Hz 清澈透润、如玉温润、澄明心境(18s)
3. 藏密黑金颂钵大磬 (Tibetan OM Full-Moon Daqing): 136.1Hz 宇宙心轮、3.5Hz深层Theta共振拍(22s)
4. 索尔菲吉奥174Hz安神大磬 (Solfeggio 174Hz Grounding Daqing): 174Hz 大地安神、极简温厚、抚平身心(19s)
5. 空灵双槌叠韵大磬 (Zen Ethereal Dual-Strike Layered Daqing): 禅门双击层叠、驻波环绕、如临空谷(22s)
"""

import numpy as np
from scipy.io import wavfile
import os

SAMPLE_RATE = 48000

def create_felt_mallet_strike(intensity=1.0, softness=1.0, duration=0.06, sample_rate=SAMPLE_RATE):
    """
    Simulates a cloth/leather-wrapped wooden mallet striking the rim of a large standing bronze bowl.
    softness: higher = softer felt mallet (less click, more warm low thud)
    """
    total_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, total_samples, endpoint=False)
    
    # Soft thud envelope
    decay_rate = 60 + 40 * (1.0 - softness)
    env = np.exp(-t * decay_rate)
    noise = np.random.normal(0, 1, total_samples)
    
    # Low thud + subtle contact friction
    thud_freq = 60.0 + 30.0 * (1.0 - softness)
    thud = np.sin(2 * np.pi * thud_freq * t) * env
    friction = noise * env * (0.08 * (1.0 - softness) + 0.02)
    
    strike = (thud * 0.7 + friction) * intensity
    return strike

def synthesize_daqing_voice(base_freq, duration, modes_config, strike_params=None, pan_center=0.0):
    """
    Synthesize physical standing bell/bowl resonance.
    modes_config: list of (ratio, amp, decay_sec, pan_off, beat_hz, beat_depth)
    """
    total_samples = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, total_samples, endpoint=False)
    
    left = np.zeros(total_samples, dtype=np.float64)
    right = np.zeros(total_samples, dtype=np.float64)
    
    for (ratio, amp, decay_sec, pan_off, beat_hz, beat_depth) in modes_config:
        freq = base_freq * ratio
        # Bowl modal decay curve
        env = np.exp(-t / max(0.5, decay_sec) * 3.2)
        
        # Subtle acoustic breathing/beating
        if beat_hz > 0:
            mod = 1.0 - beat_depth * 0.5 * (1.0 - np.cos(2 * np.pi * beat_hz * t))
        else:
            mod = 1.0
            
        phase = np.random.uniform(0, 2 * np.pi)
        wave = np.sin(2 * np.pi * freq * t + phase) * env * mod * amp
        
        pan = np.clip(pan_center + pan_off, -1.0, 1.0)
        angle = (pan + 1.0) * (np.pi / 4)
        left += wave * np.cos(angle)
        right += wave * np.sin(angle)
        
    # Attack envelope on the resonance to avoid click and blend with mallet
    attack_len = int(0.02 * SAMPLE_RATE)
    att_env = np.sin(np.linspace(0, np.pi/2, attack_len)) ** 2
    left[:attack_len] *= att_env
    right[:attack_len] *= att_env
    
    if strike_params:
        strike = create_felt_mallet_strike(**strike_params)
        slen = min(len(strike), total_samples)
        s_angle = (np.clip(pan_center, -1.0, 1.0) + 1.0) * (np.pi / 4)
        left[:slen] += strike[:slen] * np.cos(s_angle)
        right[:slen] += strike[:slen] * np.sin(s_angle)
        
    # Smooth tail fade out
    fade_len = int(1.5 * SAMPLE_RATE)
    fade_out = np.linspace(1.0, 0.0, fade_len)
    left[-fade_len:] *= fade_out
    right[-fade_len:] *= fade_out
    
    return left, right

# 1. 禅林古铜大磬 (108Hz)
def generate_daqing_1_ancient_bronze():
    duration = 20.0
    base_freq = 108.0
    modes = [
        # (ratio, amp, decay_sec, pan_off, beat_hz, beat_depth)
        # 次低频地气共振 (Sub resonance)
        (0.51, 0.35, 18.0, 0.0, 0.3, 0.20),
        # 基音 108Hz (吉祥百八佛号频率) + 0.38Hz 超缓呼吸拍频
        (1.000, 0.88, 19.0, -0.06, 0.38, 0.30),
        (1.0035, 0.78, 18.2, 0.06, 0.38, 0.30),
        # 环形二阶泛音 (2.76x)
        (2.760, 0.42, 13.0, -0.15, 0.8, 0.22),
        (2.768, 0.35, 12.5, 0.15, 0.8, 0.22),
        # 三阶泛音 (5.38x)
        (5.380, 0.20, 7.5, -0.22, 1.4, 0.18),
        # 四阶古铜金属亮韵 (8.85x)
        (8.850, 0.08, 4.0, 0.25, 0.0, 0.0),
    ]
    strike_params = {"intensity": 0.85, "softness": 0.8}
    return synthesize_daqing_voice(base_freq, duration, modes, strike_params)

# 2. 清修白铜玉磬 (216Hz)
def generate_daqing_2_pure_resonant():
    duration = 18.0
    base_freq = 216.0  # 432Hz的下八度，通透澄明
    modes = [
        (1.000, 0.90, 16.5, -0.05, 0.5, 0.25),
        (1.002, 0.82, 16.0,  0.05, 0.5, 0.25),
        (2.745, 0.48, 12.0, -0.12, 1.2, 0.20),
        (2.752, 0.40, 11.5,  0.12, 1.2, 0.20),
        (5.350, 0.25, 7.0,   0.18, 2.0, 0.15),
        (8.750, 0.10, 4.2,  -0.20, 0.0, 0.0),
        (12.80, 0.04, 2.0,   0.20, 0.0, 0.0),
    ]
    strike_params = {"intensity": 0.90, "softness": 0.65}
    return synthesize_daqing_voice(base_freq, duration, modes, strike_params)

# 3. 藏密黑金颂钵大磬 (136.1Hz OM)
def generate_daqing_3_tibetan_om():
    duration = 22.0
    base_freq = 136.1 # 宇宙地心频率 OM
    modes = [
        # 基频与约 3.5Hz 深度 Theta 脑波同步诱导
        (1.000, 0.92, 20.0, -0.08, 0.28, 0.35),
        (1.0025, 0.85, 19.5, 0.08, 0.28, 0.35),
        # 钵壁环向驻波
        (2.780, 0.45, 15.0, -0.16, 0.65, 0.25),
        (2.786, 0.38, 14.5, 0.16, 0.65, 0.25),
        (5.420, 0.22, 9.0,   0.22, 1.1, 0.20),
        (8.950, 0.09, 5.0,  -0.25, 0.0, 0.0),
    ]
    strike_params = {"intensity": 0.80, "softness": 0.95}
    return synthesize_daqing_voice(base_freq, duration, modes, strike_params)

# 4. 索尔菲吉奥174Hz安神大磬
def generate_daqing_4_grounding_174():
    duration = 19.0
    base_freq = 174.0 # Solfeggio 174Hz 大地安神频率
    modes = [
        # 极其平稳温厚的基音，少高频，低谐波包裹
        (0.50,  0.40, 17.0,  0.0,  0.2, 0.15),
        (1.000, 0.95, 18.0, -0.04, 0.35, 0.25),
        (1.0018, 0.88, 17.5, 0.04, 0.35, 0.25),
        (2.710, 0.32, 11.0, -0.12, 0.7, 0.18),
        (5.280, 0.12, 5.5,   0.14, 0.0, 0.0),
    ]
    strike_params = {"intensity": 0.75, "softness": 1.0}
    return synthesize_daqing_voice(base_freq, duration, modes, strike_params)

# 5. 禅门双槌叠韵大磬 (Dual-Strike Layered)
def generate_daqing_5_dual_strike_layered():
    duration = 22.0
    base_freq = 120.0
    modes = [
        (1.000, 0.88, 18.5, -0.06, 0.45, 0.28),
        (1.003, 0.78, 18.0,  0.06, 0.45, 0.28),
        (2.750, 0.42, 13.0, -0.15, 0.9, 0.20),
        (5.360, 0.20, 7.5,   0.18, 1.5, 0.15),
        (8.800, 0.07, 3.8,  -0.22, 0.0, 0.0),
    ]
    
    # 击打1: 润物微扣 (t=0.0s, pan 左偏)
    l1, r1 = synthesize_daqing_voice(base_freq, duration, modes, 
                                     {"intensity": 0.70, "softness": 0.9}, pan_center=-0.15)
    
    # 击打2: 气韵宏扣 (t=2.2s, 此时第一声的波浪正展开，第二声推入，pan 右偏)
    strike_2_time = 2.2
    dur2 = duration - strike_2_time
    l2, r2 = synthesize_daqing_voice(base_freq, dur2, modes, 
                                     {"intensity": 0.95, "softness": 0.8}, pan_center=0.15)
    
    total_samples = int(duration * SAMPLE_RATE)
    mix_l = np.copy(l1)
    mix_r = np.copy(r1)
    
    st2_sample = int(strike_2_time * SAMPLE_RATE)
    len2 = len(l2)
    mix_l[st2_sample:st2_sample+len2] += l2
    mix_r[st2_sample:st2_sample+len2] += r2
    
    return mix_l, mix_r

def save_wav(filename, left, right, sample_rate=SAMPLE_RATE):
    stereo = np.column_stack([left, right])
    peak = np.max(np.abs(stereo))
    if peak > 0:
        target_peak = 0.89  # -1.0 dBFS
        stereo = stereo * (target_peak / peak)
    int16_data = (stereo * 32767.0).astype(np.int16)
    wavfile.write(filename, sample_rate, int16_data)
    print(f"✅ 大磬音频已生成: {filename} ({len(left)/sample_rate:.1f}s)")

def main():
    sounds_dir = os.path.join(os.path.dirname(__file__), "sounds")
    os.makedirs(sounds_dir, exist_ok=True)
    
    print("🥣 开始合成五种大磬之声 (Daqing)...")
    
    # 1. 禅林古铜大磬
    l1, r1 = generate_daqing_1_ancient_bronze()
    save_wav(os.path.join(sounds_dir, "daqing_01_ancient_bronze.wav"), l1, r1)
    
    # 2. 清修白铜玉磬
    l2, r2 = generate_daqing_2_pure_resonant()
    save_wav(os.path.join(sounds_dir, "daqing_02_pure_resonant.wav"), l2, r2)
    
    # 3. 藏密黑金颂钵大磬
    l3, r3 = generate_daqing_3_tibetan_om()
    save_wav(os.path.join(sounds_dir, "daqing_03_tibetan_om.wav"), l3, r3)
    
    # 4. 索尔菲吉奥174Hz安神大磬
    l4, r4 = generate_daqing_4_grounding_174()
    save_wav(os.path.join(sounds_dir, "daqing_04_grounding_174.wav"), l4, r4)
    
    # 5. 空灵双槌叠韵大磬
    l5, r5 = generate_daqing_5_dual_strike_layered()
    save_wav(os.path.join(sounds_dir, "daqing_05_dual_strike_layered.wav"), l5, r5)
    
    print("\n🎉 五种大磬音频全部合成完毕！")

if __name__ == "__main__":
    main()
