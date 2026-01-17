# Feature: Queue Processor with Parallel Sub-agents

## Feature Description

Implement a `/process_queue` slash command that batch-processes all audio files in the `queue/` directory using Claude's Task tool to spawn parallel sub-agents. Each sub-agent handles one audio file: transcribes it, generates an intelligent title, creates an output directory with organized results, and moves the processed audio to `archive/`.

This is the core feature of Path 1 (Queue System) that transforms the workflow from sequential one-at-a-time processing to efficient batch processing with parallelization.

## User Story

As a developer who has captured multiple voice memos
I want to transcribe all queued audio files with one command
So that I can batch-process my thoughts efficiently instead of transcribing each file individually

## Problem Statement

Current workflow requires:
1. Finding each audio file individually
2. Running `/transcribe` or `/act_on_audio` with the file path
3. Manually organizing the output
4. Repeating for every single file (sequential bottleneck)

With 5-10 voice memos per day, this becomes tedious and error-prone. Users need a way to "process everything I've recorded today" in one command, with automatic organization and parallel processing for speed.

## Solution Statement

Create a `/process_queue` slash command that:
1. Discovers all audio files in `queue/` directory (supported formats: mp3, m4a, wav, mp4, mpeg, mpga, webm)
2. Spawns parallel sub-agents using Claude's Task tool (one agent per audio file)
3. Each sub-agent:
   - Transcribes the audio using existing `scripts/transcribe.py`
   - Generates an intelligent title using `scripts/generate_title.py`
   - Creates output directory: `output/TITLE_YYYY-MM-DD_HH-MM-SS/`
   - Creates `README.md` with transcription, metadata, and source audio reference
   - Moves processed audio from `queue/` to `archive/`
4. Reports summary: X files processed, Y successful, Z failed

The command orchestrates parallel processing but delegates the actual transcription work to sub-agents, maximizing throughput for large queues.

## Relevant Files

Use these files to implement the feature:

- `scripts/transcribe.py` - Existing transcription logic (will be called by sub-agents)
- `scripts/generate_title.py` - Title generation module (must exist, created in previous feature)
- `.claude/commands/act_on_audio.md` - Reference for output directory structure and README format

### New Files
- `.claude/commands/process_queue.md` - Slash command definition that orchestrates queue processing
- `queue/` - Source directory for unprocessed audio files (must exist)
- `archive/` - Destination directory for processed audio files (must exist)
- `output/` - Destination directory for transcription results (must exist)

## Step by Step Tasks

IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Design the slash command structure
- Create `.claude/commands/process_queue.md` with frontmatter:
  ```yaml
  ---
  allowed-tools: Bash(ls:*), Bash(mv:*), Bash(mkdir:*), Bash(date:*), Bash(python:*), Bash(uv:*), Task, Read, Write, Glob
  description: Process all audio files in queue directory
  argument-hint: [optional: --model gpt-4o-transcribe]
  ---
  ```

### Step 2: Implement queue discovery logic
- Use Glob tool to find all audio files: `queue/*.{m4a,mp3,wav,mp4,mpeg,mpga,webm}`
- Count total files found
- If queue is empty, display friendly message: "Queue is empty. Add audio files to queue/ directory."
- Display list of files to be processed with brief summary

### Step 3: Implement parallel sub-agent spawning
- For each audio file in queue, spawn a Task agent with:
  - `subagent_type: "general-purpose"`
  - `description: "Process {filename}"`
  - `prompt`: Detailed instructions for processing one audio file (see Step 4)
- Use multiple Task tool calls in a single response block to process files in parallel
- Store task IDs to track completion

### Step 4: Design sub-agent prompt template
- Each sub-agent should be given this prompt:
  ```
  Process this audio file from the queue:

  Audio file: {audio_file_path}

  Steps:
  1. Transcribe the audio using: `uv run python scripts/transcribe.py {audio_file_path}`
  2. Generate intelligent title: `echo "{transcription}" | uv run python scripts/generate_title.py`
  3. Create output directory: `mkdir -p output/{title}_{timestamp}/`
  4. Create README.md in output directory with:
     - Title: {title}
     - Source: {audio_file_path}
     - Transcribed: {current timestamp}
     - Full transcription text
  5. Move processed audio: `mv {audio_file_path} archive/`

  Report completion status: success or failure with error details.
  ```
- Timestamp format: `YYYY-MM-DD_HH-MM-SS` (using `date +%Y-%m-%d_%H-%M-%S`)

### Step 5: Implement completion tracking
- After spawning all sub-agents, wait for completion
- Collect results from each sub-agent (success/failure status)
- Generate summary report:
  ```
  Queue Processing Complete

  Total files: X
  Successfully processed: Y
  Failed: Z

  Output directories created in: output/
  Processed audio archived in: archive/
  ```

### Step 6: Add error handling
- Handle case where queue/ directory doesn't exist (create it with helpful message)
- Handle case where sub-agent fails (transcription error, API issues)
- Don't move audio to archive if transcription fails (leave in queue for retry)
- Log errors for failed files

### Step 7: Add optional model selection
- Support optional `--model` argument to override transcription model
- Default: `gpt-4o-mini-transcribe` (fast, cheap)
- Optional: `gpt-4o-transcribe` (higher quality, more expensive)
- Pass model selection to transcribe.py if supported

### Step 8: Add progress indicators
- Display "Processing X files in parallel..." message when starting
- Display "Waiting for sub-agents to complete..." while processing
- Display summary when done

## Acceptance Criteria

- [ ] `/process_queue` command exists and is documented
- [ ] Discovers all supported audio formats in queue/ directory (m4a, mp3, wav, etc.)
- [ ] Spawns parallel sub-agents (one per audio file) using Task tool
- [ ] Each sub-agent successfully:
  - [ ] Transcribes audio using existing transcribe.py
  - [ ] Generates intelligent title using generate_title.py
  - [ ] Creates output directory with format: `TITLE_YYYY-MM-DD_HH-MM-SS/`
  - [ ] Creates README.md with transcription and metadata
  - [ ] Moves processed audio from queue/ to archive/
- [ ] Handles empty queue gracefully (friendly message, no errors)
- [ ] Handles transcription failures (logs error, keeps file in queue)
- [ ] Reports summary after processing (total, succeeded, failed)
- [ ] Works with 1 file (edge case) and 10+ files (parallel efficiency test)

## Validation Commands

Execute every command to validate the feature works correctly.

```bash
# Verify slash command exists
cat .claude/commands/process_queue.md

# Setup: Create test audio files in queue (manual step - user must provide real audio)
# For now, create dummy files for structure testing
mkdir -p queue archive output
touch queue/test1.m4a queue/test2.m4a queue/test3.m4a

# Test 1: Empty queue handling
rm queue/*.m4a  # Clear queue
# Run: /process_queue
# Expected: "Queue is empty" message, no errors

# Test 2: Queue discovery
touch queue/sample1.m4a queue/sample2.mp3 queue/sample3.wav
# Run: /process_queue
# Expected: Discovers all 3 files, spawns 3 sub-agents

# Test 3: Parallel processing (with real audio - CRITICAL for USER BREAKPOINT #3)
# User should manually add 3-5 real voice memo files to queue/
# Run: /process_queue
# Expected:
#   - All files transcribed successfully
#   - Output directories created with intelligent titles
#   - Audio files moved to archive/
#   - Summary report shows all successes

# Test 4: Verify output structure
ls -la output/
# Expected: Directories with format TITLE_YYYY-MM-DD_HH-MM-SS/

# Test 5: Verify archive
ls -la archive/
# Expected: Original audio files preserved

# Test 6: Verify README contents
cat output/*/README.md
# Expected: Contains transcription, metadata, source reference

# Test 7: Re-run with empty queue (after successful processing)
# Run: /process_queue
# Expected: "Queue is empty" message (all files were moved to archive)

# Cleanup test files
rm -rf queue/test*.m4a queue/sample*.{m4a,mp3,wav}
```

## Notes

- **Parallelization strategy**: Use multiple Task tool calls in a single message to spawn sub-agents concurrently
- **Sub-agent model**: Use `model: "sonnet"` for sub-agents to minimize cost (transcription and title generation are simple tasks)
- **Error resilience**: If one sub-agent fails, others should continue processing (don't fail the entire batch)
- **Scalability**: Designed to handle 1-50 files efficiently; for >50 files, may need to batch the sub-agent spawning
- **Integration with act_on_audio**: This feature focuses on basic transcription + title + README; future enhancement could integrate act_on_audio's request detection (summary, research, code, planning)
- **USER BREAKPOINT #3 dependencies**:
  - This feature requires `scripts/generate_title.py` to exist (previous feature)
  - This feature requires queue/, archive/, output/ directories (chore)
  - User must have real voice memo files to test meaningfully
- **Future enhancements**:
  - Priority processing (--urgent flag to process specific files first)
  - Incremental processing (watch queue/ and auto-process new files)
  - Request type detection (integrate act_on_audio logic for smart output)
  - Progress bar or real-time status updates
- **Performance expectations**:
  - 3 audio files (5 minutes each): ~2-3 minutes total (parallel)
  - 10 audio files (5 minutes each): ~5-7 minutes total (parallel batching)
  - Sequential would take 15-50 minutes respectively (major improvement)
