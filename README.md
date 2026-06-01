# 📚 korean-video-generator (中韩高亮朗读视频生成器)

`korean-video-generator` 是一款为智能体（Hermes）和学习者打造的**高品质、零配跨平台、中韩双语对照高亮朗读竖屏视频生成工具**。

本项目完美集成了 **MiniMax 翻译与大模型 TTS 生态**，能够自动实现中韩互译、逐句音频精准合成以及基于手账网格纸张美学的高级高亮视觉渲染。

---

## 🎨 视觉美学设计 (Visual Aesthetics)

*   **精致手账纸网格**：背景采用极其护眼舒缓的暖阳米黄色 (`#FAF5E6`)，并点缀了 40px 等距分布的经典淡卡其网格点阵，完美复刻高档 Dotted-Journal 书写感。
*   **东方古风高对比配色**：当前正在播放的句子以极为典雅温润的**复古朱红色（#A03020，韩语）**与厚重的**深胡桃褐色（#483524，中文）**高亮呈现，非高亮句则温柔淡化为**柔和卡其灰（#C2B49A）**，字字清晰，呼吸感极强。
*   **双衬线书法字风组合**：
    *   **韩文**：自动补全经典的 **`Nanum Myeongjo` (Naver 官方开源明朝 바탕체)**。
    *   **中文**：自动补全极具国潮写意骨架的 **`ZCOOL XiaoWei` (站酷小薇体)**。
*   **黄金排版比例 (段内紧凑，段间宽舒)**：长句折行保持 1.25 倍自然行高，中韩文间距 25px（段内强聚合）；段落与段落之间空开 **120px** 大空隙，留白极其通透。

---

## ⚡️ 核心亮点特性 (Key Features)

*   **100% 绝对音画同步**：利用 `ffmpeg -shortest` 机制，令画面高亮变色帧的时长与 TTS 音频长度天然保持绝对精准对齐，避开了繁琐的时间戳校准，品质坚如磐石。
*   **自适应零配置部署 (VPS-Ready)**：脚本集成了 **jsDelivr 全球高速 CDN 代理**与 **`requests` 流式流重试机制**。当部署在没有任何字体的全新 **Linux VPS 服务器**上时，首次运行会自动静默补全拉取所缺的 9MB 中韩双语字库，实现真正的**一键免配置出海运行**。
*   **多模式智能兼容**：
    *   *单语模式*：输入纯中文，自动调用 MiniMax 翻译为韩文并执行分句对齐。
    *   *双语模式*：支持传入已校对好的 `中文 | 韩文` 逐行对照格式，100% 绕过大模型翻译，零 Token 损耗极速合成。

---

## 🚀 极速上手 (Quick Start)

### 1. 克隆并安装依赖

```bash
# 克隆仓库
git clone https://github.com/raystar27-code/mmx-hanyuskill.git
cd mmx-hanyuskill

# 安装 Python 依赖
pip install -r requirements.txt

# 确保您的系统里安装了 ffmpeg 命令行工具 (Mac 推荐 brew install ffmpeg)
```

### 2. 配置 MiniMax CLI
请确保您的本地或服务器已安装官方 MiniMax CLI (`npm install -g mmx-cli`) 并且已成功配置登录您的 API 凭证 (`mmx auth login`)。

### 3. 一键编译视频

```bash
# 模式 A：单语自动翻译渲染（中文 -> 韩文 -> 视频）
python3 scripts/generate_video.py --text "你好！今天我们来学习实用的韩语。学习一门新的语言非常有趣，只要每天坚持练习就一定能取得进步。让我们一起努力，加油！" --output multi_sentence_test.mp4

# 模式 B：对照双语直接渲染（直接传入对照，绕过翻译大模型）
python3 scripts/generate_video.py --bilingual --text "你好，今天天气真好。 | 안녕하세요, 오늘 날씨가 정말 좋네요." --output test_korean.mp4
```

---

## 🛠 命令行参数说明

| 参数名 | 默认值 | 作用描述 |
| :--- | :--- | :--- |
| `--text` | `None` | 直接输入的文本内容。 |
| `--file` | `None` | 文本文件路径（可传入纯中文文本或中韩 `中文 | 韩文` 对照文件）。 |
| `--bilingual` | `False` | 旗帜参数。若声明此项，表明输入已经是中韩对照，将跳过翻译大模型。 |
| `--voice` | `female` | 朗读音色。默认女声 `female` (Korean_SweetGirl)，男声 `male` (Korean_CalmGentleman)。 |
| `--output` | `output.mp4` | 最终输出的视频文件名。 |

---

## 📁 目录结构规划

```bash
/Users/wanglei/ai/mmx_hanyuskill/
├── README.md                # 本使用指南说明
├── SKILL.md                 # 供智能体 (Hermes) 读取的指令规格声明
├── requirements.txt         # 核心 Python 库依赖声明
├── .gitignore               # 过滤大容量媒体缓存的 Git 声明
├── scripts/
│   ├── generate_video.py    # 核心总控脚本
│   ├── minimax_client.py    # MiniMax 翻译与 TTS 代理客户端
│   ├── parser.py            # 分句与双语文本对齐解析器
│   └── renderer.py          # 高速自适应下载与手账点阵渲染器
└── tests/
    └── test_*.py            # TDD 自动化测试集合
```
