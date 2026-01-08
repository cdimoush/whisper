# Chore: Install sox Audio Capture Tool

## Chore Description

Add sox (Sound eXchange) as a dependency for cross-platform audio recording. Document installation instructions for macOS and Ubuntu, test that sox can record audio from the default microphone, and add sox to the project's setup documentation.

sox is a mature, open-source audio tool that works reliably across macOS and Linux, making it the ideal choice for a DIY voice recording system.

## Relevant Files

Use these files to resolve the chore:

- `README.md` - Main project documentation (will be updated with sox installation)
- `docs/architecture/recording-system.md` - Architecture document (reference for why sox was chosen)

## Step by Step Tasks

IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Test sox installation on current system
- Check if sox is already installed: `which sox`
- If not installed, install using platform-specific package manager:
  - **macOS**: `brew install sox`
  - **Ubuntu/Debian**: `sudo apt-get install sox libsox-fmt-all`
- Verify installation: `sox --version`

### Step 2: Test audio recording capability
- Test that sox can record from default microphone:
  ```bash
  # Record 5 seconds of audio to test file
  sox -d test_recording.wav trim 0 5
  ```
- Verify the test file was created: `ls -lh test_recording.wav`
- Optionally play back to verify audio quality: `sox test_recording.wav -d`
- Delete test file: `rm test_recording.wav`
- Note any issues (permission errors, microphone access, etc.)

### Step 3: Document installation in README
- Add a new subsection under "Setup" titled `### Audio Recording (for instant capture)`
- Add platform-specific installation instructions:
  ```markdown
  ### Audio Recording (for instant capture)

  To use the system-wide hotkey recording feature, install sox:

  **macOS:**
  ```bash
  brew install sox
  ```

  **Ubuntu/Debian:**
  ```bash
  sudo apt-get install sox libsox-fmt-all
  ```

  Verify installation:
  ```bash
  sox --version
  ```

  **Note:** sox is only required for the recording features (`/record_memo` and hotkey capture). Transcription of existing audio files works without sox.
  ```

### Step 4: Add troubleshooting section
- Create a new `## Troubleshooting` section in README (or add to existing one)
- Add sox-specific troubleshooting:
  ```markdown
  ### Audio Recording Issues

  **macOS: Microphone access denied**
  - Go to System Preferences → Security & Privacy → Microphone
  - Enable microphone access for Terminal (or iTerm, or your terminal app)

  **Ubuntu: No default audio input device**
  - Check available devices: `arecord -l`
  - Set default device in PulseAudio or ALSA configuration
  - Test recording: `sox -d test.wav trim 0 5`

  **Recording quality issues**
  - Increase sample rate: `sox -d -r 44100 output.wav`
  - Use mono instead of stereo: `sox -d -c 1 output.wav`
  - Refer to recording script in `scripts/record_memo.sh` for optimal settings
  ```

### Step 5: Document sox recording parameters
- Add a technical note explaining recommended sox settings:
  ```markdown
  ### Recording Parameters

  The recording script uses these sox parameters for optimal quality:
  - Format: `.m4a` (compressed, compatible with Voice Memos)
  - Sample rate: 16kHz (sufficient for voice, smaller file size)
  - Channels: 1 (mono, voice doesn't need stereo)
  - Encoding: AAC (good compression for speech)

  These settings balance audio quality with file size for efficient transcription.
  ```

### Step 6: Update architecture document
- Add sox details to `docs/architecture/recording-system.md` under "Technology Choices":
  ```markdown
  - **sox**: Cross-platform audio recording
    - Mature, open-source, widely available
    - Works on macOS (via Homebrew) and Linux (via apt)
    - Simple CLI interface: `sox -d output.wav trim 0 duration`
    - Supports various formats (wav, mp3, m4a via plugins)
    - No complex dependencies or proprietary drivers
  ```

### Step 7: Test sox on both platforms (if available)
- If running on macOS, test: `sox -d /tmp/test_macos.wav trim 0 3`
- If running on Ubuntu, test: `sox -d /tmp/test_ubuntu.wav trim 0 3`
- Verify file was created and contains audio
- Document any platform-specific quirks

## Validation Commands

Execute every command to validate the chore is complete.

```bash
# Verify sox is installed
which sox
sox --version

# Test recording functionality
sox -d /tmp/test_recording.wav trim 0 3
ls -lh /tmp/test_recording.wav  # Should show ~100-200KB file
rm /tmp/test_recording.wav

# Verify README documentation
grep -A 10 "sox" README.md
grep "brew install sox" README.md
grep "apt-get install sox" README.md

# Verify troubleshooting section exists
grep -A 5 "Audio Recording Issues" README.md

# Verify architecture doc mentions sox
grep -i "sox" docs/architecture/recording-system.md

# Test that sox can record in m4a format (may require additional codec)
sox -d /tmp/test.m4a trim 0 3
# If this fails, document in troubleshooting that wav format is fallback
rm -f /tmp/test.m4a
```

## Notes

- **Platform compatibility**: sox is available on macOS (Homebrew), Ubuntu (apt), and most Linux distributions
- **Codec support**: Basic sox installation supports WAV format; m4a/AAC encoding may require additional plugins:
  - macOS: `brew install sox` includes AAC support via `libsox-fmt-all`
  - Ubuntu: Must install `libsox-fmt-all` package separately for m4a support
- **Fallback strategy**: If m4a encoding isn't available, recording script should fall back to WAV format (transcription supports both)
- **Permission issues**: On macOS Catalina+, Terminal needs explicit microphone permissions (user must grant in System Preferences)
- **Alternative tools considered**:
  - ffmpeg: More complex, overkill for simple recording
  - arecord (Linux-only): Not cross-platform
  - Python sounddevice: Requires additional Python dependencies, less mature
  - sox chosen for simplicity, maturity, and cross-platform support
- **Future consideration**: Local Whisper models may prefer specific audio formats/sample rates (document if needed)
- **Testing importance**: USER BREAKPOINT #5 relies on sox working correctly, so thorough testing here is critical
