#!/usr/bin/env python3
"""
Photo Booth Screenshot Tool

Opens Photo Booth, takes a window screenshot, then closes it.
Uses CoreGraphics (Quartz) to get the window ID and screencapture to capture it.

Usage:
    python3 photobooth_screenshot.py [--output PATH] [--delay SECONDS]
"""

import subprocess
import sys
import time
import argparse

APP_NAME = "Photo Booth"


def get_window_id() -> int | None:
    """Get the window ID of Photo Booth using CoreGraphics."""
    try:
        import Quartz
    except ImportError:
        print("ERROR: pyobjc-framework-Quartz is required.", file=sys.stderr)
        print("Install it with: pip install pyobjc-framework-Quartz", file=sys.stderr)
        sys.exit(1)

    window_list = Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListOptionOnScreenOnly,
        Quartz.kCGNullWindowID
    )

    candidates = []
    for window in window_list:
        owner = window.get('kCGWindowOwnerName', '')
        if APP_NAME in owner:
            wid = window['kCGWindowNumber']
            bounds = window.get('kCGWindowBounds', {})
            candidates.append((wid, bounds))

    if not candidates:
        return None

    # Prefer windows with meaningful size (skip tiny overlay windows)
    for wid, bounds in candidates:
        w = bounds.get('Width', 0)
        h = bounds.get('Height', 0)
        if w > 100 and h > 100:
            return wid

    return candidates[0][0]


def main():
    parser = argparse.ArgumentParser(description='Photo Booth Screenshot Tool')
    parser.add_argument('--output', '-o', default=None, help='Output file path (default: ./photobooth_screenshot.png)')
    parser.add_argument('--delay', type=float, default=3.0, help='Seconds to wait after opening Photo Booth (default: 3.0)')
    args = parser.parse_args()

    output_path = args.output or "./photobooth_screenshot.png"

    # Step 1: Open Photo Booth
    print(f"Opening {APP_NAME}...")
    subprocess.run(['open', '-a', APP_NAME], capture_output=True, check=True)
    print(f"Waiting {args.delay}s for camera to initialize...")
    time.sleep(args.delay)

    # Step 2: Get window ID
    wid = get_window_id()
    if wid is None:
        print(f"ERROR: Could not find {APP_NAME} window.", file=sys.stderr)
        sys.exit(1)

    # Step 3: Take screenshot
    print(f"Window ID: {wid}")
    print(f"Saving screenshot to: {output_path}")
    result = subprocess.run(
        ['screencapture', '-l', str(wid), '-x', output_path],
        capture_output=True
    )
    if result.returncode != 0:
        print("ERROR: screencapture failed", file=sys.stderr)
        sys.exit(1)
    print("Screenshot saved!")

    # Step 4: Close Photo Booth
    print(f"Closing {APP_NAME}...")
    subprocess.run(
        ['osascript', '-e', f'tell application "{APP_NAME}" to quit'],
        capture_output=True
    )
    print("Done.")


if __name__ == '__main__':
    main()
