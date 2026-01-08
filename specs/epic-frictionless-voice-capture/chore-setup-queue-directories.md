# Chore: Setup Queue Directory Structure

## Chore Description

Create the three-directory system that forms the foundation of the queue-based workflow: `queue/` for unprocessed audio, `archive/` for processed audio files, and `output/` for transcription results. Each directory gets a README explaining its purpose to help users understand the workflow.

Update `.gitignore` to prevent accidentally committing voice memos (which may contain sensitive information) while keeping the directory structure tracked in git via `.gitkeep` files.

## Relevant Files

Use these files to resolve the chore:

- `.gitignore` - Add entries to exclude audio files and transcription outputs while preserving directory structure
- `queue/README.md` - Explain what belongs in this directory (NEW)
- `archive/README.md` - Explain the purpose of archived audio (NEW)
- `output/README.md` - Explain how transcription outputs are organized (NEW)

### New Files
- `queue/.gitkeep` - Ensures queue/ directory is tracked by git even when empty
- `archive/.gitkeep` - Ensures archive/ directory is tracked by git even when empty
- `output/.gitkeep` - Ensures output/ directory is tracked by git even when empty
- `queue/README.md` - Instructions for using the queue directory
- `archive/README.md` - Explanation of archived audio files
- `output/README.md` - Explanation of transcription output structure

## Step by Step Tasks

IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create directory structure
- Create `queue/` directory with `mkdir -p queue`
- Create `archive/` directory with `mkdir -p archive`
- Create `output/` directory with `mkdir -p output`

### Step 2: Create .gitkeep files
- Create empty `queue/.gitkeep` file to track the directory in git
- Create empty `archive/.gitkeep` file to track the directory in git
- Create empty `output/.gitkeep` file to track the directory in git

### Step 3: Update .gitignore
- Add the following entries to `.gitignore`:
  ```
  # Voice memo queue system - ignore audio files and outputs but keep directory structure
  queue/*.m4a
  queue/*.mp3
  queue/*.wav
  queue/*.mp4
  queue/*.mpeg
  queue/*.mpga
  queue/*.webm
  archive/*.m4a
  archive/*.mp3
  archive/*.wav
  archive/*.mp4
  archive/*.mpeg
  archive/*.mpga
  archive/*.webm
  output/*/
  !output/.gitkeep
  ```
- This prevents committing audio files while preserving the directory structure

### Step 4: Create queue/README.md
- Write a clear explanation of the queue directory:
  ```markdown
  # Queue Directory

  This directory holds **unprocessed audio files** waiting to be transcribed.

  ## How to Use

  ### Manual Queue (Current)
  1. Save your voice memos here (drag and drop `.m4a`, `.mp3`, `.wav` files)
  2. Run `/process_queue` to transcribe all files in this directory
  3. Processed files automatically move to `../archive/`
  4. Transcriptions appear in `../output/TITLE_YYYY-MM-DD_HH-MM-SS/`

  ### Automatic Queue (Coming Soon)
  - System-wide hotkey will auto-save recordings here
  - `/record_memo` command will save recordings here

  ## Supported Formats
  - `.m4a` (Mac Voice Memos default)
  - `.mp3`, `.wav`, `.mp4`, `.mpeg`, `.mpga`, `.webm`
  - Max file size: 25MB (OpenAI Whisper API limit)
  - Files over 8 minutes are automatically chunked during transcription

  ## File Naming
  - Any filename works - the system will auto-generate intelligent titles
  - Recording scripts will use format: `memo_YYYY-MM-DD_HH-MM-SS.m4a`

  ## Privacy Note
  - This directory is in `.gitignore` - your audio files won't be committed to git
  - Audio files contain your voice and potentially sensitive information
  - Processed audio moves to `archive/` for reference but is also gitignored
  ```

### Step 5: Create archive/README.md
- Write an explanation of the archive directory:
  ```markdown
  # Archive Directory

  This directory holds **processed audio files** that have been successfully transcribed.

  ## Purpose
  - Preserves original audio after transcription completes
  - Allows you to re-listen if transcription misses something
  - Enables re-processing with different settings in the future

  ## What Gets Archived
  - Audio files from `../queue/` after successful transcription
  - Files are moved here automatically by `/process_queue`
  - Filename is preserved from the original queue file

  ## Organization
  - Files are stored flat (no subdirectories)
  - Use `ls -lt` to see most recently archived files first
  - Corresponding transcriptions are in `../output/TITLE_YYYY-MM-DD_HH-MM-SS/`

  ## Disk Space Management
  - Audio files can take significant disk space over time
  - Safe to manually delete old archived files once you've verified transcriptions
  - Consider keeping the most recent week or month of archives

  ## Privacy Note
  - This directory is in `.gitignore` - archived audio won't be committed to git
  - If you sync this repo, exclude the archive/ directory from sync
  ```

### Step 6: Create output/README.md
- Write an explanation of the output directory structure:
  ```markdown
  # Output Directory

  This directory holds **transcription results** organized by intelligent titles and timestamps.

  ## Directory Structure
  Each transcription creates a subdirectory:
  ```
  output/
  ├── api-refactor-discussion_2026-01-08_14-30-22/
  │   ├── README.md
  │   └── [additional files based on request type]
  ├── standup-ideas-jan-8_2026-01-08_09-15-03/
  │   ├── README.md
  │   └── summary.md
  └── feature-planning-auth_2026-01-07_16-45-10/
      ├── README.md
      └── plan.md
  ```

  ## Naming Convention
  - Format: `INTELLIGENT-TITLE_YYYY-MM-DD_HH-MM-SS/`
  - **Intelligent title**: Auto-generated memorable name based on transcription content
  - **Timestamp**: Ensures uniqueness and chronological sorting

  ## Output Contents
  Each directory contains:
  - `README.md` - Summary, transcription, source audio reference
  - Additional files based on the request type:
    - `summary.md` - For summary requests
    - `research.md` - For research requests (with web sources)
    - `plan.md` - For planning/feature requests
    - `*.py`, `*.js`, etc. - For code requests

  ## Finding Past Transcriptions
  - Browse directory names to find topics (much easier than timestamps!)
  - Use `ls -lt` to see most recent transcriptions first
  - Use `grep -r "keyword" output/` to search across all transcriptions
  - Future: Full-text search index for instant lookup

  ## Privacy Note
  - This directory is in `.gitignore` - transcriptions won't be committed to git
  - Transcriptions may contain sensitive information from your voice memos
  - Safe to commit specific outputs if you want to share (manually copy elsewhere)
  ```

## Validation Commands

Execute every command to validate the chore is complete.

```bash
# Verify all directories exist
ls -la | grep -E "queue|archive|output"

# Verify .gitkeep files exist
ls queue/.gitkeep archive/.gitkeep output/.gitkeep

# Verify README files exist in each directory
cat queue/README.md
cat archive/README.md
cat output/README.md

# Verify .gitignore entries exist
grep -A 10 "Voice memo queue system" .gitignore

# Verify directory structure is tracked by git (should show .gitkeep files)
git status --short queue/ archive/ output/

# Test that audio files would be ignored
touch queue/test.m4a
git status --short queue/test.m4a  # Should show nothing (file is ignored)
rm queue/test.m4a
```

## Notes

- The three-directory system is the foundation of the entire queue-based workflow
- README files in each directory serve as inline documentation for users
- `.gitignore` entries prevent accidentally committing sensitive voice recordings
- `.gitkeep` files ensure the directory structure is preserved when cloning the repo
- This structure is designed to be intuitive: queue → process → archive (audio) + output (transcriptions)
- Future enhancements may add subdirectories in output/ for categorization (e.g., output/work/, output/personal/)
