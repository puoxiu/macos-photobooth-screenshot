---
name: macos-window-screenshot
description: "Use the Mac's camera (Photo Booth) to take a screenshot and send it to the user. Automatically opens Photo Booth, captures the window, closes it, and delivers the JPG image via attachment. Triggers: 截摄像头、拍照、摄像头截图、看摄像头、打开摄像头、camera screenshot、webcam、Photo Booth、帮我截个摄像头、拍一张、看看摄像头画面、打开Photo Booth、摄像头发给我、拍照发给我. Any request involving using the computer's camera/webcam to capture and send an image."
agent_created: true
---

# macOS Window Screenshot — Photo Booth

## Overview

Automate the full workflow of opening Photo Booth, taking a window screenshot, closing it, converting to JPG, and delivering the image as an attachment to the user via IM. Screenshots are saved to `~/Desktop/photobooth_screenshots/` with timestamps for archiving.

## When to Use

- User asks to open Photo Booth and take a screenshot
- User wants to capture what the camera sees
- User wants the screenshot sent/delivered to them (phone, chat, etc.)
- Any request to programmatically screenshot the Photo Booth window

## Workflow

### Step 1: Ensure screenshot folder exists

```bash
mkdir -p ~/Desktop/photobooth_screenshots
```

### Step 2: Run the screenshot script

Generate a timestamp-based filename and run the script:

```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
/Users/xing/anaconda3/bin/python3 ~/.workbuddy/skills/macos-window-screenshot/scripts/photobooth_screenshot.py --output ~/Desktop/photobooth_screenshots/photobooth_${TIMESTAMP}.png --delay 3
```

The script automatically:

1. Opens Photo Booth
2. Waits 3 seconds for the camera to initialize
3. Gets the window ID via CoreGraphics (`CGWindowListCopyWindowInfo`)
4. Captures the window via `screencapture -l <window_id>`
5. Closes Photo Booth

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--output, -o` | `./photobooth_screenshot.png` | Output file path (must end in .png) |
| `--delay` | `3.0` | Seconds to wait after opening Photo Booth |

### Step 3: Convert PNG to JPG (required!)

The script outputs PNG, but IM channels do not support PNG attachments. **Must convert to JPG**:

```bash
sips -s format jpeg ~/Desktop/photobooth_screenshots/photobooth_${TIMESTAMP}.png --out ~/Desktop/photobooth_screenshots/photobooth_${TIMESTAMP}.jpg
```

### Step 4: Deliver the image via attachment

Use the `deliver_attachments` tool to send the JPG file. **Do NOT delete the files** — the user wants to keep all screenshots archived in the folder.

**Tool call:**

```json
{
  "attachments": "[\"/Users/xing/Desktop/photobooth_screenshots/photobooth_<TIMESTAMP>.jpg\"]",
  "explanation": "Send Photo Booth screenshot to user"
}
```

**Expected successful response:**

```json
{
  "type": "deliver_attachments_tool_result",
  "attachments": [
    {
      "filePath": "/Users/xing/Desktop/photobooth_screenshots/photobooth_<TIMESTAMP>.jpg",
      "fileName": "photobooth_<TIMESTAMP>.jpg",
      "fileSize": 80000,
      "mimeType": "image/jpeg"
    }
  ],
  "message": "Successfully delivered 1 attachment(s)"
}
```

If the response shows `"isError": false` and includes the file path, the delivery was successful. If `"isError": true`, check:
- File path is correct and file exists on disk
- File format is JPG (not PNG — PNG attachments fail silently on some IM channels)
- Path is under `~/Desktop/` (not `/tmp/`)

### Step 5: Inform the user

Tell the user the screenshot has been sent and is also saved in `~/Desktop/photobooth_screenshots/`.

## Complete Example

```bash
# 1. Ensure folder exists
mkdir -p ~/Desktop/photobooth_screenshots

# 2. Take screenshot
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
/Users/xing/anaconda3/bin/python3 ~/.workbuddy/skills/macos-window-screenshot/scripts/photobooth_screenshot.py --output ~/Desktop/photobooth_screenshots/photobooth_${TIMESTAMP}.png --delay 3

# 3. Convert to JPG
sips -s format jpeg ~/Desktop/photobooth_screenshots/photobooth_${TIMESTAMP}.png --out ~/Desktop/photobooth_screenshots/photobooth_${TIMESTAMP}.jpg

# 4. Deliver via deliver_attachments tool (use the JPG file)

# 5. Do NOT delete files — keep archived
```

## Key Technical Details

- Must use system Python (`/Users/xing/anaconda3/bin/python3`) because the managed Python lacks `pyobjc-framework-Quartz`
- `screencapture -W` (interactive mode) hangs in automation — always use `-l <window_id>` instead
- AppleScript `System Events` requires Accessibility permissions — use CoreGraphics instead
- The script filters for windows larger than 100x100 to skip overlay/system windows
- **Output path must be ~/Desktop/** — `deliver_attachments` does not work with /tmp paths, only Desktop is reliable
- **PNG attachments are NOT supported by IM channels** — must convert to JPG before delivering
- Always use `deliver_attachments` (not HTTP server or other methods) to send files to the user
- **Do NOT delete screenshots** — keep them archived in `~/Desktop/photobooth_screenshots/` with timestamps
