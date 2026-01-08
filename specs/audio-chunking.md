# Chore: Add Audio Chunking for Long Dictations

## Chore Description

Long audio dictations (20+ minutes) are losing 50% or more of their content during transcription, even though shorter 8-minute dictations work well. The issue is that the OpenAI Whisper API can struggle with longer audio files, even when they're under the 25MB file size limit.

The solution is to add audio chunking support to `scripts/transcribe.py` that:
1. Splits longer audio files into smaller chunks (e.g., 5-minute segments)
2. Transcribes each chunk separately via the OpenAI API
3. Concatenates the transcribed text from all chunks into a single output

This should be a minimal change that preserves the existing API and behavior for shorter files.

## Relevant Files

Use these files to resolve the chore:

- `scripts/transcribe.py` - The main transcription script that needs to be upgraded with chunking logic. Currently handles single-file transcription without chunking.
- `pyproject.toml` - Dependencies file. Will need to add `pydub` for audio manipulation (splitting).
- `README.md` - May need minor update to mention chunking behavior and ffmpeg dependency.

## Step by Step Tasks

### Step 1: Add pydub dependency to pyproject.toml

- Add `pydub>=0.25.1` to the dependencies list in `pyproject.toml`
- pydub is the standard Python library for audio manipulation and supports splitting audio files
- Note: pydub requires ffmpeg to be installed on the system for m4a/mp3 support

### Step 2: Add chunking constants and helper function to transcribe.py

- Add a new constant `CHUNK_DURATION_MS = 5 * 60 * 1000` (5 minutes in milliseconds) at the top of the file
- Add a new constant `CHUNK_THRESHOLD_MS = 8 * 60 * 1000` (8 minutes) - only chunk files longer than this
- Import `tempfile` module for creating temporary chunk files
- Add a helper function `get_audio_duration_ms(path: str) -> int` that uses pydub to get audio duration
- Add a helper function `split_audio_into_chunks(path: str, chunk_duration_ms: int) -> list[str]` that:
  - Loads the audio file using pydub's `AudioSegment.from_file()`
  - Checks if the audio is longer than the threshold
  - If shorter, returns a list with just the original path
  - If longer, splits into chunks of `chunk_duration_ms` using slicing: `audio[start:end]`
  - Exports each chunk to a temporary file (using `tempfile.NamedTemporaryFile`)
  - Returns a list of chunk file paths

### Step 3: Add multi-chunk transcription function

- Add a new function `transcribe_chunks(chunk_paths: list[str], model: str) -> str` that:
  - Iterates through each chunk path
  - Calls the existing `transcribe_audio()` function for each chunk
  - Collects all transcribed text
  - Returns the concatenated text with space separators
  - Handles cleanup of temporary files after transcription

### Step 4: Update main() to use chunking logic

- After file validation passes, call `get_audio_duration_ms()` to check duration
- If duration exceeds threshold, print a message to stderr: `"Audio is {duration} minutes, splitting into chunks..."`
- Call `split_audio_into_chunks()` to get chunk paths
- If multiple chunks, use `transcribe_chunks()` instead of single `transcribe_audio()`
- Ensure temporary chunk files are cleaned up in a finally block
- Keep the existing behavior for shorter files (no chunking, direct transcription)

### Step 5: Update README.md with chunking info

- Add a note in the "Notes" section that files longer than 8 minutes are automatically chunked
- Add a note that ffmpeg must be installed for pydub to work with m4a files
- Add installation command: `brew install ffmpeg` (macOS)

### Step 6: Run validation commands

- Run validation commands to verify the chore is complete

## Validation Commands

Execute every command to validate the chore is complete with zero regressions.

- `cd /Users/conner/dev/whisper_tool && uv pip install -e .` - Install dependencies including new pydub
- `cd /Users/conner/dev/whisper_tool && uv run python -c "from pydub import AudioSegment; print('pydub OK')"` - Verify pydub is installed
- `cd /Users/conner/dev/whisper_tool && uv run python scripts/transcribe.py input/melissa_sprint.m4a 2>&1 | head -20` - Test transcription on a shorter file (should work without chunking)
- `cd /Users/conner/dev/whisper_tool && uv run python scripts/transcribe.py --help 2>&1 || true` - Verify script still runs (will show usage error, that's OK)

## Notes

- **pydub + ffmpeg**: pydub is a simple audio manipulation library but requires ffmpeg to be installed on the system for handling m4a, mp3, and other compressed formats. Without ffmpeg, only WAV files work.
- **Chunk duration choice**: 5 minutes was chosen as a safe chunk size. OpenAI's API works well with this duration and it balances API call overhead vs reliability.
- **Threshold of 8 minutes**: Since 8-minute dictations work well, we only chunk files longer than this to avoid unnecessary API calls.
- **Temporary files**: Using Python's `tempfile` module ensures proper cleanup and avoids polluting the filesystem.
- **No overlap**: This implementation uses simple non-overlapping chunks. If word-boundary issues are noticed, a future enhancement could add 5-10 second overlaps with intelligent joining, but that adds complexity.
- **Error handling**: If one chunk fails, the entire transcription fails. A future enhancement could retry failed chunks.

Sources:
- [OpenAI Developer Community - Best practices for long audio](https://community.openai.com/t/best-practice-for-generating-transcriptions-from-long-audio-files/751737)
- [Breaking down large audio files for Whisper ASR](https://www.educative.io/answers/breaking-down-large-audio-files-for-whisper-asr)
- [async-whisper GitHub - Chunking with overlap](https://github.com/DamianB-BitFlipper/async-whisper)
