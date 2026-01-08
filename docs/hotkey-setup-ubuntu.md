# Ubuntu Hotkey Setup Guide

Set up a global hotkey to record voice memos from anywhere on Ubuntu.

## Quick Reference

| Item | Value |
|------|-------|
| Recommended Hotkey | `Ctrl+Shift+R` |
| Script Path | `/path/to/whisper/scripts/record_memo.sh` |
| Stop Recording | `Ctrl+C` in terminal window |
| Check Queue | `/queue_status` in Claude Code |
| Process Queue | `/process_queue` in Claude Code |

## Prerequisites

1. **sox installed**: `sudo apt-get install sox libsox-fmt-all`
2. **Audio input configured**: Check with `arecord -l`
3. **Recording script tested**: `./scripts/record_memo.sh --help`

## Method 1: GNOME Settings (Ubuntu 20.04+ Default)

The easiest method for standard Ubuntu with GNOME desktop.

### Setup

1. Open **Settings** → **Keyboard** → **Keyboard Shortcuts**
2. Scroll to bottom, click **Custom Shortcuts**
3. Click **+** to add new shortcut
4. Fill in:
   - **Name**: Record Voice Memo
   - **Command**: `gnome-terminal -- /path/to/whisper/scripts/record_memo.sh`
5. Click **Set Shortcut**, press `Ctrl+Shift+R`
6. Close Settings

### Test

1. Press `Ctrl+Shift+R` from any application
2. Terminal opens with "Recording..." message
3. Speak your memo
4. Press `Ctrl+C` to stop
5. Check `queue/` for the new file

### Troubleshooting

**Hotkey doesn't work:**
- Check for conflicts in Settings → Keyboard → Shortcuts
- Try a different hotkey combination

**Terminal opens but closes immediately:**
- Verify script path is absolute and correct
- Check script is executable: `chmod +x scripts/record_memo.sh`
- Test script directly first: `./scripts/record_memo.sh --help`

**No audio recorded:**
- Check audio input: `arecord -l`
- Set default device in Sound Settings or `pavucontrol`
- Test sox: `sox -d test.wav trim 0 5`

## Method 2: xbindkeys (Universal, Any Desktop)

Works on any Linux desktop environment.

### Install

```bash
sudo apt-get install xbindkeys
```

### Configure

1. Generate default config:
   ```bash
   xbindkeys --defaults > ~/.xbindkeysrc
   ```

2. Edit `~/.xbindkeysrc`, add at the end:
   ```
   # Record voice memo
   "gnome-terminal -- /path/to/whisper/scripts/record_memo.sh"
     Control+Shift+r
   ```

3. Start xbindkeys:
   ```bash
   xbindkeys
   ```

4. Test your hotkey

### Auto-start on Login

Create `~/.config/autostart/xbindkeys.desktop`:

```ini
[Desktop Entry]
Type=Application
Name=xbindkeys
Exec=xbindkeys
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
```

### Find Key Names

If your hotkey doesn't work, find the correct key name:

```bash
xbindkeys --key
# Press your desired key combination
# Copy the output to your config
```

## Method 3: KDE Plasma

For Kubuntu or KDE Plasma desktop.

### Setup

1. Open **System Settings** → **Shortcuts** → **Custom Shortcuts**
2. Click **Edit** → **New** → **Global Shortcut** → **Command/URL**
3. Name it "Record Voice Memo"
4. Set trigger to `Ctrl+Shift+R`
5. Set action to:
   ```
   konsole -e /path/to/whisper/scripts/record_memo.sh
   ```
6. Apply

## Method 4: XFCE

For Xubuntu or XFCE desktop.

### Setup

1. Open **Settings** → **Keyboard** → **Application Shortcuts**
2. Click **Add**
3. Command: `xfce4-terminal -e "/path/to/whisper/scripts/record_memo.sh"`
4. Press `Ctrl+Shift+R` when prompted
5. OK

## Method 5: i3 Window Manager

For i3 users.

### Setup

Edit `~/.config/i3/config`:

```
# Record voice memo
bindsym $mod+Shift+r exec --no-startup-id alacritty -e /path/to/whisper/scripts/record_memo.sh
```

Reload i3: `$mod+Shift+r` or `i3-msg reload`

## Audio Device Configuration

### Check Available Devices

```bash
# List recording devices
arecord -l

# List PulseAudio sources
pactl list sources short
```

### Set Default Input Device

```bash
# GUI method
pavucontrol  # Install: sudo apt-get install pavucontrol

# Command line
pactl set-default-source <source_name>
```

### Test Recording

```bash
# Record 5 seconds
sox -d test.wav trim 0 5

# Play back
sox test.wav -d

# Clean up
rm test.wav
```

## Choosing a Hotkey

**Recommended** (less likely to conflict):
- `Ctrl+Shift+R` - R for Record
- `Ctrl+Alt+V` - V for Voice
- `Super+Shift+M` - M for Memo

**Check for conflicts:**
- GNOME: Settings → Keyboard → Shortcuts
- Run `xbindkeys --key` to test key combinations

## Security & Privacy

- **Microphone access**: The hotkey gives instant microphone access. Ensure your system is secure.
- **Local storage**: Audio files are stored locally in `queue/` (not synced to cloud).
- **Git safety**: `queue/` and `archive/` are in `.gitignore` - audio won't be committed.
- **Multi-user systems**: Consider per-user queue directories if sharing a computer.

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
3. **Manual**: Record with any app, save to `queue/`

All methods use the same queue and processing workflow.
