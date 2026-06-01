# korean-video-generator

一个用于将中文内容自动翻译为韩语，并生成精美逐句朗读高亮变色竖屏视频的官方 Skill。主要供 Hermes 智能体使用。

## 调用命令与使用范例

```bash
python scripts/generate_video.py --text "你好，今天天气真好！" --voice female --output my_video.mp4
```

### 参数说明
* `--text`: 直接输入的中文文本。
* `--file`: 文本文件路径（支持单语中文文件，或中韩双语对照文件）。
* `--bilingual`: （旗帜参数）如果声明此项，表明输入已经是中韩对照双语格式（每行格式为 `中文 | 韩文`），将跳过 MiniMax Chat 大模型翻译，直接进行生图和 TTS 朗读。
* `--voice`: 朗读声音，可选 `female` (经典韩语女声) 或 `male` (沉稳韩语男声)，默认为 `female`。
* `--output`: 最终生成的 MP4 视频文件名（默认为 `output.mp4`）。

### 双语对照格式范例
在双语模式下，请确保您的文件或文本满足以下结构：
```text
你好，今天天气真好。 | 안녕하세요, 오늘 날씨가 정말 좋네요.
我们一起出去玩吧！ | 우리 같이 놀러 가요!
```
