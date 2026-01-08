# Whisper Tool

Claude Code tool for transcribing audio files (Voice Memos, etc.) via OpenAI's Whisper API.

## What It Does

1. Takes an audio file path (`.m4a`, `.mp3`, `.wav`, etc.)
2. Transcribes via OpenAI API
3. Returns text for further processing (summarize, extract tasks, etc.)

## Queue-Based Workflow (New!)

The queue system enables efficient batch processing of multiple voice memos. Instead of transcribing files one at a time, drop audio files into the `queue/` directory and process them all at once with parallel sub-agents.

### Directory Structure

- **queue/** - Unprocessed audio files waiting for transcription
- **archive/** - Processed audio files (preserved for reference)
- **output/** - Transcription results organized by intelligent title + timestamp

Each directory contains a README explaining its purpose in detail.

### Queue Commands

**Check queue status:**
```bash
/queue_status
```
Shows pending audio files, total duration, and estimated processing time.

**Process all queued files:**
```bash
/process_queue
```
Transcribes all audio files in `queue/` using parallel sub-agents, generates intelligent titles, and moves processed audio to `archive/`.

### Example Workflow

1. **Add voice memos to queue:**
   - Drag and drop `.m4a` files from Voice Memos app into `queue/` directory
   - Or save recordings directly to `queue/` (hotkey support coming soon)

2. **Check what's queued (optional):**
   ```bash
   /queue_status
   ```
   Output:
   ```
   Files queued: 3
   Total duration: ~15 minutes
   ```

3. **Process the queue:**
   ```bash
   /process_queue
   ```
   Output:
   ```
   Processing 3 files in parallel...
   Queue Processing Complete
   Total files: 3
   Successfully processed: 3
   ```

4. **Browse transcriptions:**
   - Check `output/` directory for organized transcriptions
   - Example directory names: `api-refactor-discussion_2026-01-08_14-30-22/`
   - Each contains a README with full transcription and metadata

### Output Organization

Transcriptions are organized in `output/` with format:
```
output/INTELLIGENT-TITLE_YYYY-MM-DD_HH-MM-SS/
```

Example:
- `api-refactor-discussion_2026-01-08_14-30-22/`
- `standup-ideas-jan-8_2026-01-08_09-15-03/`
- `feature-planning-auth_2026-01-07_16-45-10/`

Titles are auto-generated based on transcription content, making past memos easy to find.

### Coming Soon: Instant Capture

**System-wide hotkey** (in development):
- Press a global hotkey to start/stop recording from anywhere
- Audio automatically saved to `queue/` with no manual file management
- Works on macOS and Ubuntu

**Claude command** (in development):
```bash
/record_memo
```
Start recording directly from within Claude Code sessions.

## Architecture

See [Recording System Architecture](docs/architecture/recording-system.md) for design decisions and system overview. This document explains the standalone hotkey + Claude integration approach, queue-based processing pipeline, and technology choices.

## Setup

- Requires `OPENAI_API_KEY` in environment
- Requires `ffmpeg` installed (`brew install ffmpeg` on macOS)
- Install: `uv sync` or `pip install openai pydub python-dotenv`

## Supported Formats

`mp3`, `mp4`, `mpeg`, `mpga`, `m4a`, `wav`, `webm` — max 25MB

## Models

| Model | Use Case |
|-------|----------|
| `gpt-4o-mini-transcribe` | Fast, cheap (default) |
| `gpt-4o-transcribe` | Higher quality |
| `whisper-1` | Timestamps support |

## Notes

- Mac Voice Memos: Share → Save to Files → use the `.m4a` directly
- For files >25MB: compress with ffmpeg or chunk
- **Long audio**: Files over 8 minutes are automatically split into 5-minute chunks for reliable transcription
- **Queue processing**: Process multiple voice memos at once with `/process_queue` (3-5x faster than one-at-a-time)

---

## Claude Code Slash Commands Reference

### File Locations

| Location | Scope |
|----------|-------|
| `.claude/commands/` | Project (shared with team) |
| `~/.claude/commands/` | Personal (all projects) |

### Basic Command

`.claude/commands/transcribe.md`:
```markdown
Transcribe the audio file at $ARGUMENTS and summarize the content.
```

Usage: `/transcribe /path/to/memo.m4a`

### Queue Commands

- `/queue_status` - View pending audio files in queue
- `/process_queue` - Batch process all queued audio files

### With Frontmatter

```markdown
---
allowed-tools: Bash(python:*)
description: Transcribe audio file
argument-hint: [audio-path]
model: claude-3-5-sonnet-20241022
---

Run the transcription script on $ARGUMENTS
```

### Frontmatter Options

| Field | Purpose |
|-------|---------|
| `allowed-tools` | Tools the command can use (e.g., `Bash(git:*)`) |
| `description` | Shows in command list |
| `argument-hint` | Usage hint (e.g., `[file] [format]`) |
| `model` | Override model for this command |

### Arguments

- `$ARGUMENTS` — all args as one string
- `$1`, `$2`, etc. — individual positional args

### Inline Bash (Dynamic Context)

```markdown
Current branch: !`git branch --show-current`
Recent commits: !`git log --oneline -5`
```

### File References

```markdown
Follow the patterns in @src/utils/helpers.js
```

### Skills vs Slash Commands

| | Slash Commands | Skills |
|-|----------------|--------|
| Structure | Single `.md` file | Directory with `SKILL.md` + resources |
| Use case | Simple prompts | Complex workflows with multiple files |