# macOS Photo Booth Screenshot

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
