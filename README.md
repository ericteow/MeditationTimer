# Meditation Timer · 禅修计时器

[English](#english) | [中文说明](#chinese)

---

<a name="english"></a>
## English Overview

An immersive, acoustic-grade meditation and mindfulness Web Timer. Powered by procedural physical acoustics modeling of authentic Buddhist temple bells, Daqing bronze bowls, Tibetan singing bowls, and Yinqing ritual chimes (20+ master recordings), meticulously tuned for both mobile and desktop browsers.

- **Live GitHub Pages**: [https://ericteow.github.io/MeditationTimer/](https://ericteow.github.io/MeditationTimer/)
- **Repository**: [https://github.com/ericteow/MeditationTimer](https://github.com/ericteow/MeditationTimer)

### Key Features
1. **Bilingual Support (English / 中文)**: Default English interface with an instant one-click toggle to Chinese (preferences saved in localStorage).
2. **Instant Presets & Fine Adjustments**:
   - Presets: **15 min**, **30 min**, **45 min**, **60 min**, **90 min**, **120 min**.
   - Fine-tuning: `-5 min`, `-1 min`, `+1 min`, `+5 min`.
   - Quick tests: `⚡ Test 10s` and `⚡ 1 min` to preview the full completion cycle.
3. **Adaptive Interval Mindfulness Chimes**:
   - If total duration exceeds 15 minutes, a gentle Yinqing chime sounds every 15 minutes (15m, 30m, 45m, 60m...) to restore presence without breaking meditation depth.
   - Distinct, resonant conclusion bell at the finish.
4. **Mobile Browser Background Keep-Alive (iOS & Android)**:
   - **Wall-Clock Timing**: Immune to system timer throttling when phone is locked.
   - **Silent Audio Keep-Alive**: Prevents iOS Safari from putting the tab to sleep.
   - **MediaSession API**: Lock-screen display and pause/resume controls on iPhone/Android.
   - **Screen WakeLock**: Keeps the display active when desired.
5. **Procedural Acoustic Sound Vault**:
   - **Daqing 3-Strike Crescendos (Soft → Med → Loud)**: 108Hz ancient bronze, 216Hz white bronze, 136.1Hz OM bowl, 174Hz Solfeggio, 120Hz deep valley.
   - **Yinqing 3-Strike Crescendos**: 1080Hz monastic ritual, 1200Hz crisp focus, 852Hz third-eye chakra.
   - **Single strikes & Gongs**: Temple bells, Tibetan singing bowls, oceanic gong wash.

---

<a name="chinese"></a>
## 中文说明

专为禅修、冥想与正念静坐设计的沉浸式 Web 计时器。包含物理声学建模合成的东方大钟、古铜大磬、西藏颂钵、正统引磬等 20+ 款高保真法器音效，针对移动端与桌面端浏览器进行了深度优化。

- **在线使用地址**：[https://ericteow.github.io/MeditationTimer/](https://ericteow.github.io/MeditationTimer/)

### 核心特性
1. **双语一键切换**：默认 English 版本，右上角提供 `🌐 中文` 按钮无缝切换。
2. **预设时长一键静坐**：15、30、45、60、90、120 分钟预设，微调与 10 秒/1 分钟快速测铃。
3. **自适应间歇正念提示音 (超过 15 分钟时)**：每 15 分钟节点轻击一声引磬，拉回散乱妄念；到时鸣响宏大出定钟声。
4. **移动端深度适配**：绝对时钟校准、后台音频保活、锁屏控制器显示、屏幕常亮。
5. **高品质声学法器库**：五种大磬三声（小声到大声）、引磬渐强三击、东方晨钟、深海巨锣。

---

## 🛠️ Procedural Synthesis Scripts

* `generate_daqing_crescendo.py`: 5 crescendo Daqing strikes
* `generate_crescendo_yinqing.py`: 3 crescendo Yinqing strikes
* `generate_daqing_sounds.py`: 5 single Daqing strikes
* `generate_yinqing_sounds.py`: 5 single Yinqing strikes
* `generate_meditation_sounds.py`: Temple bell, gong & OM bowl

---

## 📄 License
MIT License
