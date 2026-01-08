# Chore: Platform-Specific Hotkey Setup Guides

## Chore Description

Create comprehensive documentation for setting up system-wide hotkeys that trigger voice recording on macOS and Ubuntu. The guides should be detailed, step-by-step, with screenshots or ASCII diagrams where helpful. Each platform has different hotkey management approaches, so the documentation must be platform-specific and thorough.

This is the final piece that enables true "frictionless" voice capture - pressing a single hotkey from anywhere to instantly start recording.

## Relevant Files

Use these files to resolve the chore:

- `scripts/record_memo.sh` - Recording script that hotkeys will execute (must exist)
- `README.md` - Main documentation (will be updated with links to hotkey guides)
- `docs/architecture/recording-system.md` - Architecture context for hotkey system

### New Files
- `docs/hotkey-setup-macos.md` - Detailed macOS hotkey setup guide
- `docs/hotkey-setup-ubuntu.md` - Detailed Ubuntu hotkey setup guide

## Step by Step Tasks

IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create macOS hotkey setup guide
- Create `docs/hotkey-setup-macos.md` with the following sections:
  - **Overview**: Brief explanation of what we're setting up (global hotkey → record audio → save to queue)
  - **Prerequisites**: List requirements (sox installed, microphone permissions granted, recording script tested)
  - **Method 1: Keyboard Maestro** (most popular, paid):
    - Install Keyboard Maestro ($36, popular among power users)
    - Create new macro with hotkey trigger (e.g., Ctrl+Shift+R)
    - Add "Execute Shell Script" action: `/path/to/whisper-tool/scripts/record_memo.sh`
    - Configure to run in Terminal (for Ctrl+C stop functionality)
    - Test the hotkey
  - **Method 2: BetterTouchTool** (free for basic use):
    - Install BetterTouchTool (free trial, then $9)
    - Create keyboard shortcut (e.g., Ctrl+Shift+R)
    - Assign "Execute Terminal Command" action
    - Enter script path: `/path/to/whisper-tool/scripts/record_memo.sh`
    - Test the hotkey
  - **Method 3: Automator + System Shortcuts** (free, built-in):
    - Open Automator, create new "Quick Action"
    - Add "Run Shell Script" action
    - Set workflow receives "no input" in "any application"
    - Enter script path: `/path/to/whisper-tool/scripts/record_memo.sh`
    - Save as "Record Voice Memo"
    - Open System Preferences → Keyboard → Shortcuts → Services
    - Find "Record Voice Memo", assign hotkey (e.g., Ctrl+Shift+R)
    - Test the hotkey
  - **Choosing a Hotkey**: Recommendations for conflict-free hotkeys:
    - `Ctrl+Shift+R` (R for Record)
    - `Ctrl+Option+V` (V for Voice)
    - `Ctrl+Shift+M` (M for Memo)
    - Avoid hotkeys used by common apps (check for conflicts)
  - **Troubleshooting**: Common issues and solutions:
    - Hotkey doesn't work: Check for conflicts with other apps
    - Recording doesn't start: Verify script path is absolute
    - Permission errors: Grant Terminal microphone access in System Preferences
    - Can't stop recording: Try Ctrl+C in Terminal window (Automator limitation)
  - **Advanced: Background Recording**: Notes on running recording in background vs foreground

### Step 2: Create Ubuntu hotkey setup guide
- Create `docs/hotkey-setup-ubuntu.md` with the following sections:
  - **Overview**: Brief explanation of system (global hotkey → record audio → save to queue)
  - **Prerequisites**: sox installed, ALSA/PulseAudio configured, recording script tested
  - **Method 1: GNOME Settings** (Ubuntu 20.04+ with GNOME):
    - Open Settings → Keyboard → Keyboard Shortcuts
    - Click "Custom Shortcuts" → "+"
    - Name: "Record Voice Memo"
    - Command: `/path/to/whisper-tool/scripts/record_memo.sh`
    - Click "Set Shortcut" and press desired hotkey (e.g., Ctrl+Shift+R)
    - Test the hotkey
  - **Method 2: xbindkeys** (Universal, works on any desktop environment):
    - Install xbindkeys: `sudo apt-get install xbindkeys`
    - Create config: `xbindkeys --defaults > ~/.xbindkeysrc`
    - Edit `~/.xbindkeysrc`, add:
      ```
      "/path/to/whisper-tool/scripts/record_memo.sh"
        Control+Shift+R
      ```
    - Start xbindkeys: `xbindkeys`
    - Add to startup: Create `~/.config/autostart/xbindkeys.desktop`
    - Test the hotkey
  - **Method 3: i3 Window Manager** (for i3 users):
    - Edit `~/.config/i3/config`
    - Add binding: `bindsym $mod+Shift+r exec --no-startup-id /path/to/whisper-tool/scripts/record_memo.sh`
    - Reload i3: `i3-msg reload`
    - Test the hotkey
  - **Desktop Environment Specific**:
    - KDE Plasma: System Settings → Shortcuts → Custom Shortcuts
    - XFCE: Settings → Keyboard → Application Shortcuts
    - Cinnamon: System Settings → Keyboard → Shortcuts → Custom Shortcuts
  - **Choosing a Hotkey**: Recommendations for conflict-free hotkeys (same as macOS)
  - **Troubleshooting**: Common issues:
    - Hotkey doesn't work: Check if another app is using the hotkey
    - No audio recorded: Check PulseAudio default input device (`pactl list sources`)
    - Permission errors: Ensure sox has access to audio devices
    - xbindkeys not starting: Check logs in `~/.xbindkeys.log`
  - **Terminal Window Management**: Options for running script in separate terminal vs background

### Step 3: Add visual indicators for recording
- Document how to add visual feedback when recording starts:
  - **macOS**: Use AppleScript to display notification or menu bar icon
  - **Ubuntu**: Use `notify-send` to display notification
- Example notification script:
  ```bash
  notify-send "🎙️ Recording" "Press Ctrl+C to stop" --urgency=low
  ```
- Integrate into recording script or hotkey trigger

### Step 4: Document stopping mechanism
- Explain how to stop recording for each method:
  - **Foreground recording**: Press Ctrl+C in the terminal window
  - **Background recording**: Second hotkey press, or `pkill sox`
  - **Automator/GNOME**: May need to open terminal and press Ctrl+C
- Recommend foreground recording for better user control (can see when recording is active)

### Step 5: Add security and privacy notes
- Include section on privacy considerations:
  ```markdown
  ## Security & Privacy

  - **Microphone access**: Hotkeys give instant microphone access - ensure your system is secure
  - **Sensitive recordings**: Audio files are stored locally in queue/ (not synced to cloud)
  - **Accidental recordings**: Choose a hotkey that won't be pressed accidentally
  - **Multi-user systems**: If sharing a computer, consider per-user queue directories
  - **Git safety**: queue/ and archive/ are in .gitignore - audio won't be committed
  ```

### Step 6: Create quick reference card
- Add a "Quick Reference" section at the top of each guide:
  ```markdown
  ## Quick Reference

  **Recommended Hotkey**: Ctrl+Shift+R
  **Script Path**: `/absolute/path/to/whisper-tool/scripts/record_memo.sh`
  **Stop Recording**: Press Ctrl+C in terminal window
  **Check Queue**: `/queue_status` in Claude Code
  **Process Queue**: `/process_queue` in Claude Code
  ```

### Step 7: Link guides from main README
- Update `README.md` with a "Hotkey Setup" section:
  ```markdown
  ## Hotkey Setup (System-Wide Recording)

  Set up a global hotkey to record voice memos from anywhere:

  - **macOS**: See [macOS Hotkey Setup Guide](docs/hotkey-setup-macos.md)
  - **Ubuntu**: See [Ubuntu Hotkey Setup Guide](docs/hotkey-setup-ubuntu.md)

  Recommended hotkey: **Ctrl+Shift+R**

  After setup:
  1. Press hotkey to start recording
  2. Speak your memo
  3. Press Ctrl+C to stop
  4. Audio automatically saved to queue/
  5. Run `/process_queue` to transcribe
  ```

### Step 8: Add integration testing instructions
- Create section in each guide for testing the complete workflow:
  ```markdown
  ## Testing the Complete Workflow

  1. **Test recording script directly**: `./scripts/record_memo.sh 5`
  2. **Test hotkey trigger**: Press your hotkey, record 5 seconds, stop
  3. **Verify file in queue**: `ls -lh queue/`
  4. **Test transcription**: `/process_queue` (or `/act_on_audio queue/memo_*.m4a`)
  5. **Verify output**: Check `output/` for transcription with intelligent title

  If any step fails, refer to Troubleshooting section.
  ```

### Step 9: Document alternative workflow (without hotkey)
- For users who can't or don't want system hotkeys, document alternative:
  ```markdown
  ## Alternative: Manual Recording

  If you prefer not to set up system hotkeys:

  1. **From terminal**: Run `./scripts/record_memo.sh` directly
  2. **From Claude Code**: Use `/record_memo` command
  3. **From Voice Memos app**: Save recordings to queue/ directory manually

  All methods feed the same queue → same processing workflow.
  ```

## Validation Commands

Execute every command to validate the chore is complete.

```bash
# Verify macOS guide exists and is comprehensive
cat docs/hotkey-setup-macos.md
wc -l docs/hotkey-setup-macos.md  # Should be 150+ lines

# Verify Ubuntu guide exists and is comprehensive
cat docs/hotkey-setup-ubuntu.md
wc -l docs/hotkey-setup-ubuntu.md  # Should be 150+ lines

# Verify key sections exist in macOS guide
grep "Keyboard Maestro" docs/hotkey-setup-macos.md
grep "BetterTouchTool" docs/hotkey-setup-macos.md
grep "Automator" docs/hotkey-setup-macos.md
grep "Troubleshooting" docs/hotkey-setup-macos.md

# Verify key sections exist in Ubuntu guide
grep "GNOME Settings" docs/hotkey-setup-ubuntu.md
grep "xbindkeys" docs/hotkey-setup-ubuntu.md
grep "Troubleshooting" docs/hotkey-setup-ubuntu.md

# Verify README links to guides
grep "hotkey-setup-macos.md" README.md
grep "hotkey-setup-ubuntu.md" README.md

# Verify security/privacy section exists
grep -i "privacy" docs/hotkey-setup-macos.md
grep -i "privacy" docs/hotkey-setup-ubuntu.md

# Verify quick reference exists
grep "Quick Reference" docs/hotkey-setup-macos.md
grep "Quick Reference" docs/hotkey-setup-ubuntu.md

# Manual validation (CRITICAL for USER BREAKPOINT #6)
# User should follow one of the guides start-to-finish:
# 1. Choose a method (Keyboard Maestro, GNOME Settings, etc.)
# 2. Follow setup steps exactly as documented
# 3. Test hotkey trigger
# 4. Record a test memo
# 5. Verify audio in queue/
# 6. Process and transcribe
# 7. Evaluate: Is the workflow truly "frictionless"?
```

## Notes

- **Platform coverage**: Focus on macOS and Ubuntu (most common); mention other Linux desktop environments but don't create full guides
- **Tool recommendations**: Prioritize free/built-in methods first, then suggest paid tools as alternatives
- **Absolute paths**: Emphasize that script paths must be absolute (not relative) for system hotkeys to work
- **Terminal requirements**: Some methods require a terminal window to be open (for Ctrl+C stop functionality)
- **Background vs foreground**: Foreground recording is more user-friendly (visible, easy to stop) but background recording is more seamless
- **Hotkey conflicts**: Warn users to check for conflicts with existing app hotkeys (especially common dev tools)
- **Microphone permissions**: macOS Catalina+ requires explicit microphone permissions for Terminal (or hotkey app)
- **Visual feedback**: Recording indicator is critical for user confidence ("is it recording? how do I stop?")
- **Testing thoroughness**: USER BREAKPOINT #6 depends on these guides being accurate and complete
- **Iteration expectation**: Users may need to try 2-3 different hotkey methods to find what works best for their workflow
- **Documentation style**: Use clear headings, numbered steps, code blocks for commands, and ASCII diagrams where helpful
- **Maintenance notes**: Update guides as new macOS/Ubuntu versions change hotkey configuration UIs
- **Future enhancements**:
  - Video tutorials or GIFs showing setup process
  - Pre-configured hotkey profiles (download and import)
  - Script that detects platform and suggests best method
  - Auto-setup script that configures hotkeys programmatically (advanced)
- **Community contributions**: These guides will benefit from user feedback (different desktop environments, edge cases)
