# Bug: Audio Chunking Fails for m4a Files

## Bug Description
When transcribing audio files longer than 8 minutes, the script splits them into 5-minute chunks using pydub. However, when exporting m4a files (commonly used by iPhone Voice Memos), pydub fails because it tries to use `m4a` as the ffmpeg format parameter, but ffmpeg does not recognize `m4a` as a valid output format. The error message is: `Requested output format 'm4a' is not known`.

Expected behavior: m4a files should be chunked and transcribed successfully like other audio formats.
Actual behavior: Export fails with ffmpeg error code 234 when attempting to chunk m4a files.

## Problem Statement
The `split_audio_into_chunks` function uses the file extension directly as the pydub export format (line 49: `chunk.export(temp_file.name, format=ext.lstrip("."))`). For m4a files, ffmpeg requires the format to be specified as `ipod` rather than `m4a`. This causes chunking to fail for iPhone Voice Memos and other m4a sources.

## Solution Statement
Create a mapping from file extensions to their correct ffmpeg export format names. For most formats, the extension matches the format name, but m4a requires `ipod`, and mpga (MPEG audio) should use `mp3`. This solution requires no new dependencies and handles all supported formats with a simple dictionary lookup.

## Steps to Reproduce
1. Record a voice memo on iPhone longer than 8 minutes
2. Transfer the .m4a file to the input directory
3. Run `python scripts/transcribe.py input/your_file.m4a`
4. Observe the ffmpeg error: `Requested output format 'm4a' is not known`

## Root Cause Analysis
The root cause is in `scripts/transcribe.py` line 49:
```python
chunk.export(temp_file.name, format=ext.lstrip("."))
```

When the file extension is `.m4a`, the code passes `m4a` as the format to pydub's export function. However, ffmpeg's muxer for AAC audio in an MP4 container (what m4a actually is) is called `ipod`, not `m4a`. This is because m4a is a file extension convention, not an official ffmpeg format name.

The same issue could theoretically affect `mpga` files, which are MPEG audio files that should use the `mp3` format.

## Relevant Files
Use these files to fix the bug:

- `scripts/transcribe.py` - Contains the `split_audio_into_chunks` function where the export format issue occurs. The fix needs to be applied at line 49 where chunks are exported.

## Step by Step Tasks

### 1. Add Format Mapping Dictionary
- Add a constant dictionary `EXPORT_FORMAT_MAP` near the top of `scripts/transcribe.py` (after line 12) that maps file extensions to their correct ffmpeg format names
- Include entries for: `m4a` -> `ipod`, `mpga` -> `mp3`
- Other extensions (mp3, mp4, mpeg, wav, webm) map to themselves

### 2. Update split_audio_into_chunks Function
- Modify line 49 in `split_audio_into_chunks` to use the format mapping
- Replace `format=ext.lstrip(".")` with a lookup that uses the mapping dictionary
- The lookup should default to the extension itself for formats not in the map

### 3. Test with m4a File
- Run the transcribe script on an existing m4a file in the input directory
- Verify the file is chunked correctly (if over 8 minutes) or transcribed directly
- Confirm no ffmpeg export errors occur

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

- `cd /Users/conner/dev/whisper_tool && python3 -c "from pydub import AudioSegment; import tempfile; import os; audio = AudioSegment.from_file('input/melissa_sprint.m4a')[:10000]; tf = tempfile.NamedTemporaryFile(suffix='.m4a', delete=False); tf.close(); audio.export(tf.name, format='ipod'); print('Direct pydub test: OK'); os.unlink(tf.name)"` - Verify the ipod format fix works directly with pydub
- `cd /Users/conner/dev/whisper_tool && python3 -c "import sys; sys.path.insert(0, 'scripts'); from transcribe import split_audio_into_chunks, EXPORT_FORMAT_MAP; print('EXPORT_FORMAT_MAP:', EXPORT_FORMAT_MAP); assert EXPORT_FORMAT_MAP.get('m4a') == 'ipod', 'Missing m4a mapping'"` - Verify the format mapping is correctly defined
- `cd /Users/conner/dev/whisper_tool && python3 -c "from pydub import AudioSegment; import tempfile; import os; audio = AudioSegment.silent(duration=1000); formats = [('mp3','mp3'),('mp4','mp4'),('m4a','ipod'),('wav','wav'),('webm','webm')]; [audio.export(tempfile.NamedTemporaryFile(suffix=f'.{e}', delete=True).name, format=f) for e,f in formats]; print('All format exports: OK')"` - Verify all supported formats export correctly with the mapping

## Notes
- No new dependencies required - the fix uses pydub's existing export functionality with the correct format parameter
- The `ipod` format name is ffmpeg's standard name for m4a/AAC-in-MP4-container files
- This fix is backwards compatible - it only changes the export format name, not the file extension or any other behavior
- iPhone Voice Memos typically use AAC codec in m4a container, which is fully supported by this fix
