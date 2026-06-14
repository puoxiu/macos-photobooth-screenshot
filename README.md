# macOS Photo Booth Screenshot Skill

[English](#english) | [中文](#中文)

---

<a id="english"></a>

A [WorkBuddy](https://workbuddy.ai) skill that lets your AI assistant take webcam screenshots on macOS and deliver them to your phone or chat — with a single sentence.

Just say **"截个摄像头"** or **"take a webcam screenshot"**, and the AI will: open Photo Booth → capture the camera view → close it → send the image to you.

## What It Does

- 📸 Automatically opens Photo Booth, captures the camera window, and closes it
- 📱 Delivers the screenshot directly to your IM (WeChat, DingTalk, etc.) via WorkBuddy's `deliver_attachments`
- 💾 Archives all screenshots with timestamps in `~/Desktop/photobooth_screenshots/`
- 🤖 Fully automatic — no clicks, no manual steps

## Trigger Examples

The skill is automatically matched when you say things like:

| Language | Example |
|----------|---------|
| Chinese | 截个摄像头、拍照、摄像头截图、看看摄像头、打开摄像头、拍照发给我 |
| English | take a webcam screenshot, camera screenshot, capture Photo Booth, webcam capture |

## Install

### Prerequisites

- macOS 12.0+
- Python 3 with `pyobjc-framework-Quartz` installed
- [WorkBuddy](https://workbuddy.ai) desktop app

### Steps

1. Clone this repo into your WorkBuddy skills directory:

```bash
git clone https://github.com/puoxiu/macos-photobooth-screenshot.git ~/.workbuddy/skills/macos-window-screenshot
```

2. Install the Python dependency:

```bash
pip install pyobjc-framework-Quartz
```

3. Restart WorkBuddy — the skill is ready to use!

## How It Works

When triggered, the WorkBuddy agent follows this workflow (defined in `SKILL.md`):

1. **Ensure folder exists** — creates `~/Desktop/photobooth_screenshots/`
2. **Take screenshot** — runs the Python script which opens Photo Booth, waits for the camera, captures the window, and closes Photo Booth
3. **Convert to JPG** — converts PNG to JPG (PNG attachments don't render in some IM channels like WeChat)
4. **Deliver** — sends the JPG via `deliver_attachments` to your phone/chat
5. **Archive** — keeps all screenshots in the folder with timestamps

## Skill Structure

```
macos-window-screenshot/
├── SKILL.md                          # Skill definition & workflow for WorkBuddy agent
└── scripts/
    └── photobooth_screenshot.py      # Core script: open → capture → close
```

## Technical Notes

- Uses **CoreGraphics** (`CGWindowListCopyWindowInfo`) to find the Photo Booth window ID — no Accessibility permissions needed
- `screencapture -W` (interactive) hangs in automation, so `-l <window_id>` is used instead
- **PNG attachments may not render** in some IM channels (e.g. WeChat) — always convert to JPG before delivering
- Output path must be `~/Desktop/` — `/tmp` paths don't work with `deliver_attachments`
- Screenshots are never deleted — all archived in `~/Desktop/photobooth_screenshots/`

## License

MIT License. See [LICENSE](LICENSE) for details.

---

<a id="中文"></a>

# macOS Photo Booth 截图技能

一个 [WorkBuddy](https://workbuddy.ai) 技能，让你的 AI 助手一句话就能在 macOS 上截取摄像头画面并发送到手机或聊天窗口。

只需说 **"截个摄像头"**，AI 就会：打开 Photo Booth → 截取摄像头画面 → 关闭 → 把图片发给你。

## 功能亮点

- 📸 自动打开 Photo Booth、截取摄像头窗口、关闭应用
- 📱 通过 WorkBuddy 的 `deliver_attachments` 直接把截图发到你的 IM（微信、钉钉等）
- 💾 所有截图带时间戳归档到 `~/Desktop/photobooth_screenshots/`
- 🤖 全自动——无需点击，无需手动操作

## 触发示例

只需正常说话，AI 会自动匹配这个技能：

| 示例 | 说明 |
|------|------|
| 截个摄像头 | 最常用的说法 |
| 帮我拍一张 | 同样会触发 |
| 看看摄像头画面 | 也能识别 |
| 摄像头发给我 | 截图并发送 |
| take a webcam screenshot | 英文也支持 |

## 安装

### 前置条件

- macOS 12.0+
- Python 3，需安装 `pyobjc-framework-Quartz`
- [WorkBuddy](https://workbuddy.ai) 桌面端

### 安装步骤

1. 将仓库克隆到 WorkBuddy 技能目录：

```bash
git clone https://github.com/puoxiu/macos-photobooth-screenshot.git ~/.workbuddy/skills/macos-window-screenshot
```

2. 安装 Python 依赖：

```bash
pip install pyobjc-framework-Quartz
```

3. 重启 WorkBuddy —— 技能即可使用！

## 工作流程

当技能被触发时，WorkBuddy 智能体会按以下流程执行（定义在 `SKILL.md` 中）：

1. **创建截图文件夹** — 创建 `~/Desktop/photobooth_screenshots/`
2. **截取摄像头** — 运行 Python 脚本，自动打开 Photo Booth、等待摄像头、截取窗口、关闭应用
3. **转换为 JPG** — PNG 附件在微信等 IM 渠道可能无法显示，需转为 JPG
4. **发送截图** — 通过 `deliver_attachments` 发送到你的手机/聊天
5. **归档保留** — 截图带时间戳保存在文件夹中，不删除

## 技能结构

```
macos-window-screenshot/
├── SKILL.md                          # 技能定义 & WorkBuddy 智能体工作流
└── scripts/
    └── photobooth_screenshot.py      # 核心脚本：打开 → 截图 → 关闭
```

## 技术说明

- 使用 **CoreGraphics**（`CGWindowListCopyWindowInfo`）获取 Photo Booth 窗口 ID——无需辅助功能权限
- `screencapture -W`（交互模式）在自动化中会卡住，因此使用 `-l <窗口ID>` 替代
- **PNG 附件在部分 IM 渠道（如微信）可能无法显示**——发送前务必转为 JPG
- 输出路径必须为 `~/Desktop/`——`/tmp` 路径在 `deliver_attachments` 中不可用
- 截图不会被删除——全部归档在 `~/Desktop/photobooth_screenshots/`

## 开源协议

MIT 协议，详见 [LICENSE](LICENSE)。
