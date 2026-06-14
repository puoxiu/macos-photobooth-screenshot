# macOS Photo Booth Screenshot

[English](#english) | [中文](#中文)

---

<a id="english"></a>

A lightweight macOS automation tool that opens Photo Booth, captures a window screenshot, and closes it — all in one command. Designed for [WorkBuddy](https://workbuddy.ai) skills ecosystem.

## Features

- Open Photo Booth automatically
- Wait for camera initialization (configurable delay)
- Capture the Photo Booth window using CoreGraphics + `screencapture`
- Close Photo Booth after capture
- No interactive prompts — fully scriptable

## Requirements

- macOS 12.0+
- Python 3 with `pyobjc-framework-Quartz` installed
- Photo Booth app (pre-installed on macOS)

## Quick Start

```bash
# Install dependency
pip install pyobjc-framework-Quartz

# Take a screenshot
python3 scripts/photobooth_screenshot.py --output screenshot.png --delay 3
```

## Usage

```
python3 scripts/photobooth_screenshot.py [OPTIONS]

Options:
  -o, --output PATH    Output file path (default: ./photobooth_screenshot.png)
  --delay SECONDS      Seconds to wait after opening Photo Booth (default: 3.0)
```

### Example

```bash
# Save to Desktop with 5-second delay
python3 scripts/photobooth_screenshot.py --output ~/Desktop/booth.png --delay 5
```

## How It Works

1. Opens Photo Booth via `open -a "Photo Booth"`
2. Waits for the camera to initialize (default 3 seconds)
3. Uses `CGWindowListCopyWindowInfo` (CoreGraphics/Quartz) to find the Photo Booth window ID
4. Captures the window via `screencapture -l <window_id>`
5. Closes Photo Booth via AppleScript

## Why CoreGraphics?

- `screencapture -W` (interactive selection) hangs in automation
- AppleScript `System Events` requires Accessibility permissions
- CoreGraphics works reliably without extra permissions

## WorkBuddy Integration

This skill is designed to work as a [WorkBuddy](https://workbuddy.ai) skill. The `SKILL.md` file contains the skill definition and workflow instructions for the WorkBuddy agent.

### Key notes for IM delivery

- **PNG attachments may not render** in some IM channels (e.g. WeChat) — convert to JPG before delivering
- Use `deliver_attachments` tool to send files to the user
- Output path should be `~/Desktop/` — `/tmp` paths may not work with some delivery methods

## License

MIT License. See [LICENSE](LICENSE) for details.

---

<a id="中文"></a>

# macOS Photo Booth 截图工具

一款轻量的 macOS 自动化工具，一键打开 Photo Booth、截取窗口画面、关闭应用。专为 [WorkBuddy](https://workbuddy.ai) 技能生态设计。

## 功能特性

- 自动打开 Photo Booth
- 等待摄像头初始化（延迟可配置）
- 使用 CoreGraphics + `screencapture` 截取 Photo Booth 窗口
- 截图后自动关闭 Photo Booth
- 无交互式提示，完全可脚本化

## 环境要求

- macOS 12.0+
- Python 3，需安装 `pyobjc-framework-Quartz`
- Photo Booth 应用（macOS 预装）

## 快速开始

```bash
# 安装依赖
pip install pyobjc-framework-Quartz

# 截图
python3 scripts/photobooth_screenshot.py --output screenshot.png --delay 3
```

## 使用方法

```
python3 scripts/photobooth_screenshot.py [选项]

选项：
  -o, --output 路径     输出文件路径（默认：./photobooth_screenshot.png）
  --delay 秒数          打开 Photo Booth 后等待的秒数（默认：3.0）
```

### 示例

```bash
# 保存到桌面，等待 5 秒
python3 scripts/photobooth_screenshot.py --output ~/Desktop/booth.png --delay 5
```

## 工作原理

1. 通过 `open -a "Photo Booth"` 打开 Photo Booth
2. 等待摄像头初始化（默认 3 秒）
3. 使用 `CGWindowListCopyWindowInfo`（CoreGraphics/Quartz）获取 Photo Booth 窗口 ID
4. 通过 `screencapture -l <窗口ID>` 截取窗口
5. 通过 AppleScript 关闭 Photo Booth

## 为什么用 CoreGraphics？

- `screencapture -W`（交互式选择）在自动化中会卡住
- AppleScript `System Events` 需要辅助功能权限
- CoreGraphics 无需额外权限，稳定可靠

## WorkBuddy 集成

本工具作为 [WorkBuddy](https://workbuddy.ai) 技能使用，`SKILL.md` 文件包含技能定义和 WorkBuddy 智能体的工作流说明。

### IM 渠道发送注意事项

- **PNG 附件可能在部分 IM 渠道（如微信）无法正常显示**——发送前请转换为 JPG
- 使用 `deliver_attachments` 工具向用户发送文件
- 输出路径应为 `~/Desktop/`——`/tmp` 路径在某些发送方式下可能不可用

## 开源协议

MIT 协议，详见 [LICENSE](LICENSE)。
