# Feature: Recording Script with Auto-Queue

## Feature Description

Create `scripts/record_memo.sh` - a standalone bash script that uses sox to record audio from the system microphone and automatically saves the recording to the `queue/` directory with a timestamped filename. The script runs independently of Claude Code and can be triggered by system hotkeys, making it the foundation for instant voice capture.

This script bridges the gap between "press hotkey" and "audio file appears in queue" without requiring any manual file management.

## User Story

As a developer who wants to capture thoughts instantly
I want a simple script that records my voice and queues it for transcription
So that I can brain-dump without thinking about file names, paths, or organization

## Problem Statement

Current workflow requires manually:
1. Opening Voice Memos app (or equivalent)
2. Recording audio
3. Saving/exporting the file
4. Navigating to the file location
5. Moving it to the queue/ directory

This 5-step process takes 1-2 minutes and breaks flow state. We need a 1-step process: press hotkey, speak, done.

## Solution Statement

Create a bash script that:
1. Starts recording audio from the default microphone using sox
2. Displays recording indicator (console output + visual feedback)
3. Records until user stops (Ctrl+C or time limit)
4. Saves audio to `queue/memo_YYYY-MM-DD_HH-MM-SS.m4a`
5. Confirms file was saved successfully
6. Exits cleanly

The script should be simple, robust, and platform-agnostic (works on macOS and Ubuntu). It's designed to be called by hotkey managers or Claude Code's `/record_memo` command.

## Relevant Files

Use these files to implement the feature:

- `scripts/transcribe.py` - Reference for supported audio formats and naming conventions
- `queue/` - Destination directory for recorded audio (must exist)

### New Files
- `scripts/record_memo.sh` - Main recording script with sox integration
- `docs/recording-script-usage.md` - Detailed usage documentation for the recording script

## Step by Step Tasks

IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create recording script structure
- Create `scripts/record_memo.sh` with shebang: `#!/usr/bin/env bash`
- Set up error handling: `set -euo pipefail`
- Add script description comment block at top

### Step 2: Check dependencies
- Verify sox is installed:
  ```bash
  if ! command -v sox &> /dev/null; then
    echo "Error: sox is not installed"
    echo "Install with: brew install sox (macOS) or apt-get install sox (Ubuntu)"
    exit 1
  fi
  ```
- Verify queue/ directory exists, create if missing:
  ```bash
  QUEUE_DIR="$(dirname "$0")/../queue"
  mkdir -p "$QUEUE_DIR"
  ```

### Step 3: Generate timestamped filename
- Create filename with format: `memo_YYYY-MM-DD_HH-MM-SS.m4a`
- Use bash date command:
  ```bash
  TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
  OUTPUT_FILE="$QUEUE_DIR/memo_$TIMESTAMP.m4a"
  ```

### Step 4: Implement recording with sox
- Start recording with optimal settings for voice:
  ```bash
  echo "🎙️  Recording... Press Ctrl+C to stop"
  echo "Output: $OUTPUT_FILE"

  # Record with settings optimized for voice
  sox -d \
    -r 16000 \
    -c 1 \
    -b 16 \
    "$OUTPUT_FILE" \
    trim 0 300  # Max 5 minutes (300 seconds)
  ```
- Parameters explained:
  - `-d`: Record from default audio input device
  - `-r 16000`: 16kHz sample rate (sufficient for voice, smaller files)
  - `-c 1`: Mono (voice doesn't need stereo)
  - `-b 16`: 16-bit depth (good quality, efficient size)
  - `trim 0 300`: Maximum 5-minute recording (prevents accidentally leaving it running)

### Step 5: Add recording indicators
- Display clear start message: "🎙️ Recording... Press Ctrl+C to stop"
- Show output file path
- Optional: Add timer display (count up seconds recorded)
- Add visual indicator that recording is active

### Step 6: Implement graceful shutdown
- Trap Ctrl+C (SIGINT) to stop recording cleanly:
  ```bash
  trap cleanup SIGINT SIGTERM

  cleanup() {
    echo ""
    echo "✓ Recording stopped"
    verify_recording
    exit 0
  }
  ```

### Step 7: Verify recording was successful
- After recording completes, check file exists and has content:
  ```bash
  verify_recording() {
    if [ -f "$OUTPUT_FILE" ]; then
      FILE_SIZE=$(stat -f%z "$OUTPUT_FILE" 2>/dev/null || stat -c%s "$OUTPUT_FILE" 2>/dev/null)
      if [ "$FILE_SIZE" -gt 1000 ]; then
        echo "✓ Saved: $OUTPUT_FILE ($(numfmt --to=iec-i --suffix=B $FILE_SIZE 2>/dev/null || echo "$FILE_SIZE bytes"))"
        echo ""
        echo "Process with: /process_queue"
      else
        echo "⚠️  Warning: Recording file is very small ($FILE_SIZE bytes)"
        echo "Check microphone permissions and try again"
      fi
    else
      echo "❌ Error: Recording failed"
      exit 1
    fi
  }
  ```

### Step 8: Add command-line options
- Support optional duration argument:
  ```bash
  DURATION=${1:-300}  # Default 5 minutes, or user-specified
  ```
- Add `--help` flag:
  ```bash
  if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
    echo "Usage: $0 [duration_in_seconds]"
    echo ""
    echo "Records audio from microphone and saves to queue/ directory"
    echo "Press Ctrl+C to stop recording early"
    echo ""
    echo "Examples:"
    echo "  $0          # Record for max 5 minutes"
    echo "  $0 60       # Record for max 60 seconds"
    echo "  $0 1800     # Record for max 30 minutes"
    exit 0
  fi
  ```

### Step 9: Make script executable
- Set execute permissions: `chmod +x scripts/record_memo.sh`
- Test execution: `./scripts/record_memo.sh --help`

### Step 10: Add fallback to WAV format
- If m4a encoding fails (missing codec), fall back to WAV:
  ```bash
  # Try m4a first, fallback to wav
  OUTPUT_FILE="$QUEUE_DIR/memo_$TIMESTAMP.m4a"

  if ! sox -d "$OUTPUT_FILE" trim 0 1 2>/dev/null; then
    echo "⚠️  m4a not supported, using wav format"
    OUTPUT_FILE="$QUEUE_DIR/memo_$TIMESTAMP.wav"
  fi
  ```

### Step 11: Create usage documentation
- Create `docs/recording-script-usage.md` explaining:
  - How to run the script manually
  - How to set up system hotkeys (covered in detail in separate chore)
  - How to integrate with Claude Code
  - Troubleshooting common issues (microphone permissions, sox not found, etc.)

## Acceptance Criteria

- [ ] `scripts/record_memo.sh` exists and is executable
- [ ] Checks for sox installation, displays helpful error if missing
- [ ] Records audio from default microphone
- [ ] Uses voice-optimized settings (16kHz, mono, 16-bit)
- [ ] Saves to `queue/memo_YYYY-MM-DD_HH-MM-SS.m4a` (or .wav as fallback)
- [ ] Creates queue/ directory if it doesn't exist
- [ ] Displays clear recording indicator ("🎙️ Recording...")
- [ ] Stops recording on Ctrl+C gracefully
- [ ] Enforces maximum duration (default 5 minutes, configurable)
- [ ] Verifies recording was successful (file exists, has content)
- [ ] Displays file path and size after recording
- [ ] Provides `--help` documentation
- [ ] Works on both macOS and Ubuntu
- [ ] Handles missing codecs gracefully (falls back to WAV)

## Validation Commands

Execute every command to validate the feature works correctly.

```bash
# Verify script exists and is executable
ls -la scripts/record_memo.sh
head -1 scripts/record_memo.sh  # Should show #!/usr/bin/env bash

# Test help output
./scripts/record_memo.sh --help

# Test sox dependency check (temporarily rename sox to test error handling)
# This validates the error message for missing sox
# sudo mv $(which sox) $(which sox).bak
# ./scripts/record_memo.sh
# Expected: Error message about sox not installed
# sudo mv $(which sox).bak $(which sox)

# Test actual recording (CRITICAL for USER BREAKPOINT #5)
./scripts/record_memo.sh 10
# [speak for 5 seconds, then press Ctrl+C]
# Expected:
#   - "Recording..." message appears
#   - Recording stops on Ctrl+C
#   - Success message with file path
#   - File exists in queue/

# Verify recording was saved
ls -lh queue/memo_*.m4a  # Should show file with timestamp
# Or if wav fallback:
ls -lh queue/memo_*.wav

# Test that file is valid audio (transcribe it)
uv run python scripts/transcribe.py queue/memo_*.m4a
# Expected: Transcription of what you said

# Test maximum duration (30-second recording)
./scripts/record_memo.sh 30
# [wait 30 seconds without stopping]
# Expected: Automatically stops after 30 seconds

# Test queue directory creation
rm -rf queue
./scripts/record_memo.sh 5
# Expected: Creates queue/ directory automatically

# Verify documentation exists
cat docs/recording-script-usage.md

# Cleanup test recordings
rm queue/memo_*.m4a queue/memo_*.wav
```

## Notes

- **Audio format**: Prefer m4a (AAC encoding) for smaller file sizes; fallback to WAV if codec unavailable
- **Sample rate**: 16kHz is sufficient for voice transcription and produces smaller files than 44.1kHz
- **Maximum duration**: 5 minutes is a reasonable default (prevents accidentally leaving recording running overnight)
- **Microphone permissions**: On macOS Catalina+, Terminal needs microphone access (users must grant in System Preferences)
- **sox recording format**: The `-d` flag tells sox to record from the default input device
- **Graceful shutdown**: The `trap` command ensures Ctrl+C doesn't leave corrupted audio files
- **File size check**: Verify recording is >1KB to catch cases where mic wasn't working (silent recording)
- **Integration points**:
  - Called by hotkey manager (Phase 2B)
  - Called by `/record_memo` Claude command (Phase 2B)
  - Can be run manually for testing
- **Future enhancements**:
  - Background recording (run in background, press hotkey again to stop)
  - Visual recording indicator (system tray icon, menubar status)
  - Audio level meter (show mic input level during recording)
  - Configurable quality presets (low/medium/high)
  - Pause/resume functionality
- **Platform differences**:
  - macOS: `stat -f%z` for file size
  - Linux: `stat -c%s` for file size
  - Script handles both with fallback
- **Testing strategy**: USER BREAKPOINT #5 validates:
  - Recording works from command line
  - Audio quality is acceptable for transcription
  - File appears in queue/ automatically
  - Process is fast and frictionless
