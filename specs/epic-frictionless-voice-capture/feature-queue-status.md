# Feature: Queue Status Command

## Feature Description

Implement a `/queue_status` slash command that displays a summary of unprocessed audio files in the `queue/` directory. Shows file count, total duration, file sizes, and filenames to help users understand what's pending before running `/process_queue`.

This is a convenience feature that provides visibility into the queue state without having to manually `ls queue/` or inspect files.

## User Story

As a developer with multiple voice memos queued
I want to see what's pending transcription before processing
So that I can verify the right files are queued and estimate processing time

## Problem Statement

Users currently have no visibility into queue status without manually running terminal commands. They can't quickly answer:
- "How many files are waiting?"
- "How much audio is queued up?" (total duration)
- "Is that file I recorded this morning actually in the queue?"
- "Should I process now or wait for more files?"

## Solution Statement

Create a simple `/queue_status` slash command that:
1. Scans the `queue/` directory for audio files
2. Calculates total file count and cumulative size
3. Attempts to extract duration metadata for each file (using pydub if available)
4. Displays a formatted summary with file list

The command provides quick visibility without processing anything, making it safe to run anytime.

## Relevant Files

Use these files to implement the feature:

- `scripts/transcribe.py` - Reference for `get_audio_duration_ms()` function and supported formats
- `queue/` - Directory to scan for audio files

### New Files
- `.claude/commands/queue_status.md` - Slash command definition

## Step by Step Tasks

IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create slash command definition
- Create `.claude/commands/queue_status.md` with frontmatter:
  ```yaml
  ---
  allowed-tools: Bash(ls:*), Bash(du:*), Bash(find:*), Bash(python:*), Bash(uv:*), Read, Glob
  description: Show status of audio files in queue
  ---
  ```

### Step 2: Implement queue discovery
- Use Glob to find all audio files in queue/ with pattern: `queue/*.{m4a,mp3,wav,mp4,mpeg,mpga,webm}`
- If queue is empty, display friendly message:
  ```
  Queue is empty ✓

  Add audio files to queue/ to get started:
  - Drag and drop voice memos into queue/
  - Use system hotkey (coming soon)
  - Use /record_memo command (coming soon)
  ```
- If queue has files, proceed to analysis

### Step 3: Calculate basic statistics
- Count total files found
- Calculate total size using `du -ch queue/*.m4a queue/*.mp3` etc. (or equivalent)
- List filenames with sizes

### Step 4: Extract duration metadata (optional but recommended)
- For each file, attempt to get duration using Python:
  ```python
  from pydub import AudioSegment
  audio = AudioSegment.from_file(path)
  duration_seconds = len(audio) / 1000
  ```
- Calculate total duration across all files
- Handle errors gracefully (if pydub fails, skip duration and show "Unknown duration")

### Step 5: Format output display
- Create a clear, readable summary:
  ```
  Queue Status
  ============

  Files queued: 5
  Total size: 23.4 MB
  Total duration: ~32 minutes

  Files:
  1. memo_2026-01-08_09-15-30.m4a (4.2 MB, 6.3 min)
  2. standup-ideas.m4a (5.1 MB, 7.8 min)
  3. feature-planning.m4a (6.8 MB, 10.2 min)
  4. quick-note.m4a (3.1 MB, 4.7 min)
  5. research-notes.m4a (4.2 MB, 6.4 min)

  Ready to process? Run: /process_queue
  ```

### Step 6: Add estimated processing time (optional)
- Based on total duration, estimate transcription time
- Rule of thumb: transcription takes ~20-40% of audio duration (1 minute audio ≈ 15-20 seconds to transcribe)
- Display estimate: "Estimated processing time: 8-12 minutes (parallel)"

### Step 7: Add helpful tips
- If queue is large (>10 files), suggest: "Large queue detected. Processing will happen in parallel."
- If queue has very short files (<1 minute each), suggest: "Quick files detected. Processing should be fast."
- If queue/ directory doesn't exist, display setup instructions

## Acceptance Criteria

- [ ] `/queue_status` command exists and is documented
- [ ] Displays file count accurately
- [ ] Shows total size of queued audio files
- [ ] Lists all queued files with individual sizes
- [ ] Optionally shows duration for each file (if pydub is available)
- [ ] Calculates total duration across all files
- [ ] Handles empty queue gracefully (friendly message, no errors)
- [ ] Provides helpful next-step guidance ("Run /process_queue" or "Add files to queue/")
- [ ] Runs quickly (<2 seconds for typical queue of 5-10 files)

## Validation Commands

Execute every command to validate the feature works correctly.

```bash
# Verify slash command exists
cat .claude/commands/queue_status.md

# Test 1: Empty queue
rm -f queue/*.m4a queue/*.mp3 queue/*.wav  # Clear queue
# Run: /queue_status
# Expected: "Queue is empty" message with helpful tips

# Test 2: Queue with files (create test files)
touch queue/test1.m4a queue/test2.mp3 queue/test3.wav
# Run: /queue_status
# Expected: Shows 3 files, sizes, and list

# Test 3: Queue with real audio files (IMPORTANT for meaningful validation)
# User manually adds 2-3 real voice memo files to queue/
# Run: /queue_status
# Expected:
#   - Accurate file count (2-3)
#   - Real file sizes displayed
#   - Duration metadata extracted (if pydub works)
#   - Estimated processing time shown

# Test 4: Verify duration calculation accuracy
# Compare reported duration with actual audio file duration (check in audio player)
# Should be within 1-2 seconds of actual duration

# Test 5: Large queue (10+ files)
# Add 10+ test files to queue/
# Run: /queue_status
# Expected: Shows all files, suggests parallel processing

# Cleanup
rm -f queue/test*.{m4a,mp3,wav}
```

## Notes

- **Performance**: Should be fast (<2 seconds) even for 50+ files in queue
- **Duration extraction**: Use pydub's `AudioSegment.from_file()` (same library used in transcribe.py)
- **Error handling**: If duration extraction fails for a file (corrupted, unsupported format), show "Unknown duration" instead of crashing
- **File size display**: Use human-readable format (MB, KB) instead of bytes
- **Sorting**: Display files in chronological order (newest first or oldest first - choose based on typical workflow)
- **Future enhancements**:
  - Show file age (e.g., "recorded 2 hours ago")
  - Group files by day ("Today: 3 files, Yesterday: 2 files")
  - Show which files are likely to be chunked (>8 minutes)
  - Estimate cost (based on Whisper API pricing)
  - Color coding (green for ready, yellow for large files, red for potential issues)
- **Integration**: This command is purely informational and doesn't modify anything (safe to run anytime)
- **Use case**: Helps users decide when to run `/process_queue` (e.g., "I'll wait until I have 5+ files to batch them")
