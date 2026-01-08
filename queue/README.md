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
