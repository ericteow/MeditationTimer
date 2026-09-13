# 禅修计时器 (Meditation Timer)

一款专为禅修、冥想与正念静坐设计的沉浸式 Web 计时器。包含物理声学建模合成的东方大钟、古铜大磬、西藏颂钵、正统引磬等 20+ 款高保真法器音效，针对移动端与桌面端浏览器进行了深度优化。

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Audio](https://img.shields.io/badge/Audio-48kHz%20Master-gold.svg)
![Mobile](https://img.shields.io/badge/Mobile-iOS%20%7C%20Android-green.svg)

---

## ✨ 核心特性

1. **预设时长一键静坐**：
   - 完整支持 **15 min**、**30 min**、**45 min**、**60 min**、**90 min**、**120 min** 常用禅修预设。
   - 提供 `-5分`、`-1分`、`+1分`、`+5分` 精准微调。
   - 提供 `⚡ 测试 10 秒` 与 `⚡ 1 分钟` 快速校验出定音效。

2. **自适应间歇正念提示音 (超过 15 分钟时)**：
   - 当静坐时长超过 15 分钟时，系统自动在每 15 分钟节点（如 15m、30m、45m、60m 等）轻击一声引磬，拉回散乱妄念，保持正念觉知。
   - 到时准时响彻选定的宏大出定钟声。

3. **专为移动端（iOS Safari / Android Chrome）深度优化**：
   - **绝对时钟校准 (Wall-Clock Timing)**：手机锁屏或切换后台时，倒计时绝不冻结。
   - **后台音频保活 (Silent Audio Keep-Alive)**：利用微量静音会话防止 iOS 挂起定时器，黑屏锁屏也能准时鸣响出定钟声。
   - **锁屏控制 (MediaSession API)**：在 iPhone 锁屏界面或 Android 通知栏直接查看静坐进度与控制暂停。
   - **屏幕常亮 (Screen WakeLock)**：静坐过程中防止设备息屏。

4. **高品质声学法器库 (Procedural Acoustic Synthesis)**：
   - **大磬三击 (由轻至重)**：108Hz 禅林古铜大磬、216Hz 白铜玉磬、136.1Hz OM 颂钵、174Hz 安神大磬、120Hz 空灵深潭大磬。
   - **引磬三击 (由轻至重)**：1080Hz 经典禅门三击、1200Hz 紧凑清越三击、852Hz 温润紫铜三击。
   - **单击原音**：古铜大磬、白铜玉磬、黑金颂钵、引磬单击、双槌叠韵、东方晨钟、深海巨锣。
   - 提供 48kHz 无损 WAV 与轻量 MP3 双格式。

---

## 🚀 快速使用

### 本地直接打开
直接用浏览器打开 `index.html`：
```bash
open index.html
```

### 局域网在手机端运行
启动 Python 本地 Web 服务，同 Wi-Fi 下手机浏览器直接访问：
```bash
python3 -m http.server 8080
```
然后在手机 Safari 或 Chrome 打开：
```
http://<你的电脑IP>:8080
```

---

## 🛠️ 音频生成代码

项目包含基于物理模态振动与非谐波泛音分解（Inharmonic Bessel Modes & Acoustic Beating）的 Python 合成脚本：
* `generate_daqing_crescendo.py`：大磬渐强三推合成
* `generate_crescendo_yinqing.py`：引磬渐强三击合成
* `generate_daqing_sounds.py`：五种大磬单击原声合成
* `generate_yinqing_sounds.py`：五种引磬单击原声合成
* `generate_meditation_sounds.py`：大钟、巨锣与颂钵合成

运行合成：
```bash
python3 generate_daqing_crescendo.py
python3 generate_crescendo_yinqing.py
```

---

## 📄 License
MIT License
