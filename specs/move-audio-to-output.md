# Chore: Move Audio to Output Directory

## Chore Description
Change where processed audio files are stored. Instead of moving them to a separate `archive/` directory, move them into the output directory alongside their transcription and deliverables. This keeps all related files together in one place.

## Problem
Currently, processed audio files are moved to `archive/` which is separate from `output/`. This creates two problems:
1. Audio files are disconnected from their transcriptions - you have to cross-reference by filename/timestamp
2. Finding the original audio for a transcription requires looking in a different directory
3. The `archive/` directory is just a flat list with no organization

## Solution
Move the audio file into the output directory (e.g., `output/api-refactor-discussion_2026-01-08/`) alongside the README and other deliverables. This:
1. Keeps source audio with its transcription for easy reference
2. Eliminates the need for a separate `archive/` directory
3. Makes output directories self-contained packages

## Relevant Files
### Files to Modify
- `.claude/commands/act.md` - Change archive step to move audio into output directory instead of `archive/`
- `README.md` - Update directory structure documentation to reflect new behavior
- `output/README.md` - Update to mention audio files are included in output directories

### New Files
None

## Step by Step Tasks

### Step 1: Update `/act` command to move audio to output directory
- Change Step 9 from `mv "$ARGUMENTS" archive/` to `mv "$ARGUMENTS" "output/{title}_{timestamp}/"`
- Update the step description to reflect the new behavior
- Update the README template in Step 6 to note the audio file will be in the same directory

### Step 2: Update main README.md
- Update the Directory Structure section to remove `archive/` references
- Update the example workflow to show audio ends up in output directory
- Update queue commands description

### Step 3: Update output/README.md
- Add `source.m4a` (or similar) to the directory structure example
- Update "Output Contents" section to mention the source audio file

### Step 4: Determine fate of archive/ directory
- The `archive/` directory and its README can remain for now (existing files there)
- Or optionally remove if empty and update `.gitignore`

### Step 5: Run Validation Commands

## Validation Commands
- `grep -c "output/{title}" .claude/commands/act.md` - Should show the audio being moved to output dir
- `grep -c "archive/" .claude/commands/act.md` - Should return 0 (no longer archiving separately)
- `cat output/README.md` - Should mention source audio files

## Notes
- Existing files in `archive/` are unaffected - this only changes future processing
- The output directory becomes a self-contained package with audio + transcription + deliverables
- This simplifies backup - just back up `output/` to have everything
