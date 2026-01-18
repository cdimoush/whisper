# Whisper Tool

Claude Code tool for transcribing audio files (Voice Memos, etc.) via OpenAI's Whisper API.

## What It Does

1. Takes an audio file path (`.m4a`, `.mp3`, `.wav`, etc.)
2. Transcribes via OpenAI API
3. Returns text for further processing (summarize, extract tasks, etc.)

## Queue-Based Workflow (New!)

The queue system enables efficient batch processing of multiple voice memos. Instead of transcribing files one at a time, drop audio files into the `queue/` directory and process them all at once with parallel sub-agents.

### Directory Structure

- **queue/** - Unprocessed audio files waiting for processing
- **output/** - Results organized by intelligent title + timestamp (includes source audio)

Each output directory is self-contained with the original audio, transcription, and deliverables.

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
Processes all audio files in `queue/` using parallel sub-agents. Each file is fully acted upon: transcribed, analyzed for requests, deliverables created, then moved to output.

**Act on a single audio file:**
```bash
/act /path/to/audio.m4a
```
Transcribes the audio, generates an intelligent title, interprets the spoken request, creates deliverables (summaries, research, code, plans), and moves audio to output.

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

4. **Browse results:**
   - Check `output/` directory for organized results
   - Example directory names: `api-refactor-discussion_2026-01-08_14-30-22/`
   - Each contains the source audio, README with transcription, and deliverables

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

### Instant Capture

Record voice memos directly to the queue with zero friction.

**From terminal:**
```bash
./scripts/record_memo.sh        # Record (press Ctrl+C to stop)
./scripts/record_memo.sh 60     # Record for max 60 seconds
```

**From Claude Code:**
```bash
/record_memo                    # Start recording from within session
```

**System-wide hotkey (Recommended):**
- Press `Ctrl+Shift+R` to record and save to queue
- **macOS**: Uses Raycast - see [macOS Hotkey Setup](docs/hotkey-setup-macos.md)
- **Ubuntu**: Uses GNOME/xbindkeys - see [Ubuntu Hotkey Setup](docs/hotkey-setup-ubuntu.md)

### Instant Memo to Clipboard

Record, transcribe, and copy to clipboard instantly - no files saved to queue.

**From terminal:**
```bash
./scripts/instant_memo.sh       # Record, transcribe, copy to clipboard
./scripts/instant_memo.sh 30    # Record for max 30 seconds
```

**System-wide hotkey:**
- Set up a second hotkey (e.g., `Ctrl+Shift+T`) for instant transcription
- Same setup as above, but import `scripts/instant_memo_raycast.sh` instead
- Use this for quick notes, dictation, or capturing thoughts without saving files

## Brain System (New!)

The `brain/` directory is Whisper's persistent memory - context that agents access across all voice memos. This solves the problem of agents starting from scratch every conversation.

### What's in the Brain

- **summary.md** - Chronological summary of all memos to date
- **claudes_wants_this.md** - Strategic roadmap and time allocation
- **active_projects.md** - Current projects, priorities, and blockers
- **people.md** - Team members and communication context
- **technical_systems.md** - Architecture docs for all technical systems
- **glossary.md** - Technical terms, acronyms, project names
- **tags.md** - Tagging strategy and tag reference

### Why Brain Matters

**Before**: "Help me with Design Lab" → Agent: "What's Design Lab?" → Explain for 5 minutes

**After**: "Design Lab work - check brain/technical_systems.md" → Agent: [Reads once, gets to work]

### Usage

Brain files are automatically referenced by agents when processing voice memos. You can also manually point to them:

```bash
# In a voice memo, mention:
"See brain/active_projects.md for context on Simulation Mandate"
"Check brain/people.md for info about Nick"
```

Future: Automatic context injection based on project tags (see brain/tags.md).

**Note**: brain/ is not committed to git (personal context). Each user maintains their own brain.

## Architecture

See [Recording System Architecture](docs/architecture/recording-system.md) for design decisions and system overview. This document explains the standalone hotkey + Claude integration approach, queue-based processing pipeline, and technology choices.

For Claude Code agents, see [CLAUDE.md](CLAUDE.md) for complete agent guide including brain system usage, tagging strategy, and development workflows.

## Setup

- Requires `OPENAI_API_KEY` in environment
- Requires `ffmpeg` installed (`brew install ffmpeg` on macOS)
- Install: `uv sync` or `pip install openai pydub python-dotenv`

### Audio Recording (for instant capture)

To use the recording features (`/record_memo`, hotkey capture), install sox:

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

**Note:** sox is only required for recording. Transcription of existing audio files works without sox.

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

## Troubleshooting

### Audio Recording Issues

**macOS: Microphone access denied**
- Go to System Settings → Privacy & Security → Microphone
- Enable microphone access for Terminal (or iTerm, or your terminal app)

**Ubuntu: No default audio input device**
- Check available devices: `arecord -l`
- Set default device in PulseAudio settings
- Test recording: `sox -d test.wav trim 0 5`

**Recording quality issues**
- Test with higher sample rate: `sox -d -r 44100 output.wav trim 0 5`
- Ensure microphone is not muted in system settings

**"sox: command not found"**
- Install sox (see Setup section above)

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
- `/process_queue` - Batch process all queued audio files (invokes `/act` for each)
- `/act <path>` - Process a single audio file: transcribe, analyze, create deliverables, move to output

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