# macOS Hotkey Setup Guide

Set up a global hotkey to record voice memos from anywhere on your Mac.

## Quick Reference

| Item | Value |
|------|-------|
| **Recommended Method** | **Raycast (easiest, fastest)** |
| Record to Queue | `Ctrl+Shift+R` |
| Instant to Clipboard | `Ctrl+Shift+T` (optional) |
| Stop Recording | `Ctrl+C` in terminal window |
| Check Queue | `/queue_status` in Claude Code |
| Process Queue | `/process_queue` in Claude Code |

## Prerequisites

1. **sox installed**: `brew install sox`
2. **Microphone permissions**: Terminal must have microphone access
3. **Recording script tested**: `./scripts/record_memo.sh --help`

## Method 1: Raycast (Recommended - 2 Minutes Setup)

**Why Raycast?** Fastest setup, auto-closes terminal, works reliably, plus you get a better Spotlight replacement.

### Setup

1. **Install Raycast**:
   ```bash
   brew install --cask raycast
   ```

2. **Open Raycast** and allow it to replace Spotlight (optional but recommended)

3. **Import the script**:
   - Press `Cmd+Space` to open Raycast
   - Type: **Import Script Command**
   - Navigate to: `/path/to/whisper/scripts/record_memo_raycast.sh`
   - Raycast will auto-detect it with the 🎙️ icon

4. **Assign hotkey**:
   - In Raycast, type: **Record Memo (Hotkey)**
   - Press `Cmd+K` when you see it
   - Choose **Assign Hotkey**
   - Press: `Ctrl+Shift+R`

5. **Done!** Press `Ctrl+Shift+R` from anywhere, record, press `Ctrl+C`, terminal auto-closes.

### Optional: Add Instant Memo (Clipboard)

For quick dictation without saving files, add a second hotkey:

1. In Raycast, type: **Import Script Command**
2. Select: `/path/to/whisper/scripts/instant_memo_raycast.sh`
3. Assign hotkey (e.g., `Ctrl+Shift+T`)
4. Now you have two options:
   - `Ctrl+Shift+R` → Record to queue (for processing later)
   - `Ctrl+Shift+T` → Instant transcription to clipboard (no files saved)

### Advantages

- ✅ Terminal automatically closes after recording
- ✅ Clean, fast workflow
- ✅ Raycast replaces Spotlight with better features
- ✅ 2-minute setup
- ✅ Optional instant clipboard transcription

## Method 2: Automator + System Shortcuts (Free, Built-in)

This method uses macOS built-in tools with no additional software.

### Step 1: Create Automator Quick Action

1. Open **Automator** (search in Spotlight)
2. Choose **Quick Action** (or "Service" in older macOS)
3. Configure the workflow:
   - "Workflow receives" → **no input**
   - "in" → **any application**
4. From the left sidebar, drag **Run Shell Script** to the workflow area
5. Set "Shell" to `/bin/bash`
6. Set "Pass input" to **as arguments**
7. Enter the script path (use YOUR actual path):
   ```bash
   /Users/YOUR_USERNAME/path/to/whisper/scripts/record_memo.sh
   ```
8. **Save** as "Record Voice Memo"

### Step 2: Assign Keyboard Shortcut

1. Open **System Settings** → **Keyboard** → **Keyboard Shortcuts**
2. Select **Services** (or **App Shortcuts** → **Services**) in the left sidebar
3. Find "Record Voice Memo" under **General**
4. Click to add shortcut, press `Ctrl+Shift+R` (or your preferred hotkey)
5. Close System Settings

### Step 3: Test

1. Press your hotkey from any application
2. A Terminal window should open with "Recording..." message
3. Speak your memo
4. Press `Ctrl+C` to stop
5. Check `queue/` directory for the new file

### Troubleshooting Automator Method

**Hotkey doesn't trigger anything:**
- Ensure the Quick Action was saved
- Check System Settings → Keyboard → Shortcuts → Services
- Try a different hotkey (some are reserved by system/apps)

**Terminal opens but script doesn't run:**
- Verify the script path is absolute and correct
- Check script is executable: `chmod +x scripts/record_memo.sh`

**"Operation not permitted" error:**
- Grant Terminal microphone access in System Settings → Privacy & Security → Microphone

## Method 2: Keyboard Maestro ($36, Most Powerful)

[Keyboard Maestro](https://www.keyboardmaestro.com/) is the most flexible option for power users.

### Setup

1. Download and install Keyboard Maestro
2. Create a new macro:
   - **Trigger**: Hot Key → `Ctrl+Shift+R`
   - **Action**: Execute Shell Script
   - **Script**: `/path/to/whisper/scripts/record_memo.sh`
   - Check "Execute in new Terminal window"
3. Save the macro

### Advantages

- More reliable than Automator
- Can add visual indicators (notifications, menu bar icons)
- Supports complex workflows (e.g., auto-process after recording)

## Method 3: BetterTouchTool ($10, Feature-Rich)

[BetterTouchTool](https://folivora.ai/) is a versatile automation tool.

### Setup

1. Download and install BetterTouchTool
2. Open Preferences → Keyboard
3. Click "+" to add new shortcut
4. Record shortcut: `Ctrl+Shift+R`
5. Add action: **Run Shell Script / Task**
6. Enter script path: `/path/to/whisper/scripts/record_memo.sh`
7. Check "Launch in Terminal"

## Method 4: Raycast (Free, Modern)

[Raycast](https://www.raycast.com/) is a modern Spotlight replacement with scripting support.

### Setup

1. Install Raycast
2. Open Raycast → Extensions → Script Commands
3. Create new script command pointing to `record_memo.sh`
4. Assign hotkey in Raycast preferences

## Choosing a Hotkey

**Recommended hotkeys** (less likely to conflict):
- `Ctrl+Shift+R` - R for Record
- `Ctrl+Option+V` - V for Voice
- `Ctrl+Shift+M` - M for Memo
- `Cmd+Shift+0` - Easy to reach

**Avoid** hotkeys used by:
- VS Code: `Cmd+Shift+P`, `Cmd+B`, etc.
- Chrome: `Cmd+T`, `Cmd+W`, etc.
- System: `Cmd+Space`, `Cmd+Tab`, etc.

## Security & Privacy

- **Microphone access**: The hotkey gives instant microphone access. Ensure your system is secure.
- **Local storage**: Audio files are stored locally in `queue/` (not synced to cloud).
- **Git safety**: `queue/` and `archive/` are in `.gitignore` - audio won't be committed.
- **Accidental recordings**: Choose a hotkey that won't be pressed accidentally.

## Testing the Complete Workflow

1. **Test script directly**: `./scripts/record_memo.sh 5`
2. **Test hotkey**: Press your hotkey, record 5 seconds, stop with Ctrl+C
3. **Verify file**: `ls -lh queue/`
4. **Process**: Run `/process_queue` in Claude Code
5. **Check output**: Look in `output/` for transcription

## Alternative: No Hotkey

If you prefer not to set up system hotkeys:

1. **From terminal**: `./scripts/record_memo.sh`
2. **From Claude Code**: `/record_memo`
3. **From Voice Memos app**: Save recordings to `queue/` manually

All methods use the same queue and processing workflow.
