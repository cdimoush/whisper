# Feature: Claude-Integrated Record Command

## Feature Description

Implement a `/record_memo` slash command that triggers audio recording from within Claude Code sessions. The command launches the recording script (`scripts/record_memo.sh`) and provides real-time feedback about the recording process. This gives users the convenience of voice capture without leaving their Claude Code workflow.

This is the "Claude integration" path of the dual recording system (hotkey + Claude command), making voice capture accessible from within coding sessions.

## User Story

As a developer working in a Claude Code session
I want to start recording a voice memo without switching apps
So that I can capture thoughts mid-session and continue working

## Problem Statement

While the system hotkey provides universal voice capture, users working actively in Claude Code may prefer to trigger recording directly from their current context without reaching for a global hotkey. Current workflow requires:
1. Switching away from Claude Code session
2. Opening terminal or hotkey trigger
3. Managing recording manually
4. Returning to Claude Code session

This breaks flow and adds friction for in-session voice capture.

## Solution Statement

Create a `/record_memo` slash command that:
1. Launches `scripts/record_memo.sh` as a background process
2. Provides recording instructions and stop signal
3. Waits for recording to complete
4. Reports success and file location
5. Suggests next steps (`/process_queue` to transcribe)

The command uses Claude's Bash tool to execute the recording script, making voice capture a first-class feature within Claude Code sessions.

## Relevant Files

Use these files to implement the feature:

- `scripts/record_memo.sh` - Recording script (must exist, created in previous feature)
- `.claude/commands/transcribe.md` - Reference for command structure and allowed-tools patterns
- `.claude/commands/act_on_audio.md` - Reference for audio processing commands

### New Files
- `.claude/commands/record_memo.md` - Slash command definition for in-session recording

## Step by Step Tasks

IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create slash command definition
- Create `.claude/commands/record_memo.md` with frontmatter:
  ```yaml
  ---
  allowed-tools: Bash(scripts/record_memo.sh:*), Bash(ls:*), Glob
  description: Record voice memo to queue
  argument-hint: [optional: duration_in_seconds]
  ---
  ```

### Step 2: Add command description
- Write clear instructions for what the command does:
  ```markdown
  # Record Voice Memo

  Starts audio recording from your microphone and saves to the queue/ directory.
  Press Ctrl+C to stop recording, or recording will auto-stop after the specified duration.

  ## Usage

  Record with default 5-minute max duration:
  ```
  /record_memo
  ```

  Record with custom duration (e.g., 60 seconds):
  ```
  /record_memo 60
  ```
  ```

### Step 3: Implement recording launch logic
- Check that recording script exists and is executable:
  ```bash
  ls -la scripts/record_memo.sh
  ```
- If missing, display helpful error:
  ```
  Error: Recording script not found.
  Run: chmod +x scripts/record_memo.sh
  ```

### Step 4: Execute recording script
- Launch the recording script with optional duration argument:
  ```bash
  ./scripts/record_memo.sh ${1:-300}
  ```
- The script handles all recording logic (sox, filename generation, saving to queue/)
- Display recording output to user (includes "Recording..." indicator and stop instructions)

### Step 5: Handle recording completion
- After recording completes (user presses Ctrl+C or duration expires):
- Verify the recording was saved successfully (check queue/ for new file)
- Display success message with file details:
  ```
  ✓ Recording saved to queue/

  Next steps:
  - Check queue status: /queue_status
  - Process the queue: /process_queue
  - Process immediately: /act_on_audio queue/memo_[timestamp].m4a
  ```

### Step 6: Add error handling
- Handle case where sox is not installed:
  ```
  Error: sox is not installed.

  Install sox for audio recording:
  - macOS: brew install sox
  - Ubuntu: sudo apt-get install sox libsox-fmt-all

  See README.md for detailed setup instructions.
  ```
- Handle microphone permission errors (macOS):
  ```
  Error: Microphone access denied.

  On macOS:
  1. Open System Preferences → Security & Privacy → Microphone
  2. Enable microphone access for Terminal (or your terminal app)
  3. Try recording again
  ```

### Step 7: Add recording tips
- Include helpful tips at the bottom of the command:
  ```markdown
  ## Tips

  - **Stop early**: Press Ctrl+C to stop recording before max duration
  - **Check queue**: Run /queue_status to see all pending recordings
  - **Batch process**: Record multiple memos, then run /process_queue to transcribe all at once
  - **Immediate transcription**: Use /act_on_audio for instant transcription of a single memo
  - **System hotkey**: For recording outside Claude Code sessions, set up a system-wide hotkey (see README.md)
  ```

### Step 8: Add troubleshooting section
- Include common issues and solutions:
  ```markdown
  ## Troubleshooting

  **No audio recorded / silent file:**
  - Check default microphone input in System Preferences (macOS) or Sound Settings (Ubuntu)
  - Test recording: `sox -d test.wav trim 0 5`
  - Verify microphone is working in other apps

  **"sox: command not found":**
  - Install sox (see error message above)

  **Recording doesn't stop on Ctrl+C:**
  - Try Ctrl+C twice
  - If still stuck, open a new terminal and kill the process: `pkill sox`
  ```

### Step 9: Test command integration
- Verify command appears in Claude Code command list
- Test that Bash tool can execute the recording script
- Validate error messages display correctly

## Acceptance Criteria

- [ ] `/record_memo` command exists and is documented
- [ ] Launches `scripts/record_memo.sh` successfully
- [ ] Accepts optional duration argument (e.g., `/record_memo 60` for 60 seconds)
- [ ] Displays recording indicator and stop instructions
- [ ] Stops recording on Ctrl+C
- [ ] Verifies recording was saved successfully
- [ ] Reports file location after recording completes
- [ ] Suggests next steps (`/queue_status`, `/process_queue`)
- [ ] Handles missing sox gracefully (helpful error message)
- [ ] Handles microphone permission errors (macOS-specific guidance)
- [ ] Provides troubleshooting tips for common issues
- [ ] Works consistently across multiple invocations

## Validation Commands

Execute every command to validate the feature works correctly.

```bash
# Verify slash command exists
cat .claude/commands/record_memo.md

# Verify command has proper frontmatter
head -6 .claude/commands/record_memo.md | grep "allowed-tools"

# Test command functionality (manual test in Claude Code session)
# Run: /record_memo 10
# Expected:
#   - Recording starts
#   - "Recording..." message displays
#   - Press Ctrl+C to stop (or wait 10 seconds)
#   - Success message with file path
#   - File exists in queue/

# Verify recording was saved
ls -lh queue/memo_*.m4a
# Expected: Shows recording file with timestamp

# Test immediate transcription
# Run: /act_on_audio queue/memo_[latest timestamp].m4a
# Expected: Transcribes the recording you just made

# Test error handling (sox not installed)
# Temporarily rename sox: sudo mv $(which sox) $(which sox).bak
# Run: /record_memo
# Expected: Clear error message with installation instructions
# Restore sox: sudo mv $(which sox).bak $(which sox)

# Test with custom duration
# Run: /record_memo 5
# Expected: Records for max 5 seconds (or until Ctrl+C)

# Verify help documentation in command file
grep "Troubleshooting" .claude/commands/record_memo.md
grep "Tips" .claude/commands/record_memo.md

# Cleanup test recordings
rm queue/memo_*.m4a queue/memo_*.wav
```

## Notes

- **Command execution**: Uses Claude's Bash tool to execute `scripts/record_memo.sh`
- **Background vs foreground**: Recording runs in foreground (blocking) so user knows it's active and can stop with Ctrl+C
- **Duration default**: Inherits 5-minute default from recording script
- **Integration with queue workflow**: Recording automatically saves to queue/, ready for batch processing
- **Comparison with system hotkey**:
  - `/record_memo`: Convenient for in-session recording, requires Claude Code to be running
  - System hotkey: Universal capture from any app, works independently of Claude
  - Both save to the same queue/, processed by the same pipeline
- **User experience design**:
  - Clear recording indicator prevents user wondering if it's working
  - Stop instructions reduce confusion ("how do I stop this?")
  - Next steps guide users through the workflow (record → check queue → process)
- **Error message quality**: Prioritize helpful, actionable error messages (don't just say "failed", explain why and how to fix)
- **Future enhancements**:
  - Start/stop recording with two separate commands (instead of Ctrl+C)
  - Background recording (non-blocking, show status with separate command)
  - Record and immediately transcribe (combine record + act_on_audio)
  - Voice-activated recording (start on voice detection, stop on silence)
- **Testing strategy**: USER BREAKPOINT #6 validates:
  - `/record_memo` works from Claude Code sessions
  - Experience is smooth and intuitive
  - Error handling is clear and helpful
  - Integration with queue workflow is seamless
- **Documentation linking**: Command should reference README.md for detailed setup (sox installation, hotkey setup)
- **Allowed-tools constraint**: Only permit execution of recording script, not arbitrary bash commands (security/safety)
