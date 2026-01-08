# Chore: Reshuffle Command Dependencies

## Chore Description
Refactor the `/act` and `/process_queue` commands so they work together properly. Currently `/process_queue` only transcribes audio files and generates titles, but it should invoke the `/act` command to fully process each audio file. Additionally, `/act` doesn't use the intelligent title generation feature. The commands need to be restructured so `/act` is the core processor and `/process_queue` delegates to it.

## Problem
1. **`/process_queue` doesn't act on audio**: It only transcribes and generates titles, missing the core value of `/act` which interprets requests and creates deliverables
2. **`/act` doesn't use title generation**: The cool new `generate_title.py` feature isn't integrated into `/act`, so output directories use timestamps only
3. **Duplicated logic**: Both commands transcribe audio independently instead of `/process_queue` delegating to `/act`
4. **Poor composition**: Commands don't wrap each other properly - they should form a clean hierarchy

## Solution
Restructure the commands with clear responsibilities:

1. **`/act` (core processor)**: Transcribe audio → Generate intelligent title → Create output directory with title → Execute request → Archive audio
2. **`/process_queue` (batch orchestrator)**: Find queue files → Spawn `/act` for each file in parallel → Report summary

This creates a clean composition where `/process_queue` simply parallelizes `/act` calls.

## Relevant Files
### Files to Modify
- `.claude/commands/act.md` - Add title generation step, update directory naming, add archive step
- `.claude/commands/process_queue.md` - Simplify to spawn `/act` sub-agents instead of doing transcription inline

### New Files
None - this is a refactoring of existing commands

## Step by Step Tasks

### Step 1: Update `/act` to use intelligent title generation
- Add title generation step after transcription using `scripts/generate_title.py`
- Change output directory format from `output/YYYY-MM-DD_HH-MM-SS/` to `output/{title}_{timestamp}/`
- Add archive step at the end: move processed audio to `archive/`
- Update README template to include the generated title
- Add `Bash(mv:*)` to allowed-tools for archive step

### Step 2: Simplify `/process_queue` to delegate to `/act`
- Remove inline transcription and title generation logic
- Instead, spawn Task agents that invoke the `/act` command via Skill tool
- Update the sub-agent prompt to use: `Invoke the /act skill with argument: {audio_file_path}`
- Keep parallel processing and summary reporting logic
- Simplify allowed-tools since heavy lifting moves to `/act`

### Step 3: Update README documentation
- Update the queue workflow example to reflect new behavior
- Clarify that `/process_queue` now fully acts on each audio file, not just transcribes

### Step 4: Run Validation Commands

## Validation Commands
- `cat .claude/commands/act.md` - Verify act command includes title generation and archive step
- `cat .claude/commands/process_queue.md` - Verify process_queue delegates to /act
- `grep -c "generate_title" .claude/commands/act.md` - Should return >= 1
- `grep -c "archive" .claude/commands/act.md` - Should return >= 1
- `grep -c "transcribe.py" .claude/commands/process_queue.md` - Should return 0 (no longer does transcription directly)

## Notes
- The `/act` command becomes the single source of truth for audio processing logic
- `/process_queue` becomes a thin orchestration layer
- This makes future enhancements easier - changes to processing logic only need to be made in `/act`
- Archive behavior ensures queue items are moved out after successful processing
- Failed items remain in queue for retry (existing error handling preserved)
