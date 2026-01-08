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
