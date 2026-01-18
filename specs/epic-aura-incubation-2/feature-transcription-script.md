# Feature: Transcription Script

## Feature Description

Port whisper's `scripts/transcribe.py` to `.aura/scripts/transcribe.py` with adaptations for portability.

## User Story

As a developer using aura
I want transcription to work out of the box
So that `/aura.transcribe` and `/aura.act` function correctly

## Source

Copy from: `whisper/scripts/transcribe.py` (167 lines)

## Adaptations Required

### 1. Remove whisper-specific paths
- No references to whisper directories
- Work from any working directory

### 2. Make standalone
- All imports should be standard library or from requirements.txt
- No imports from aura package

### 3. Improve error messages
- Clear guidance when OPENAI_API_KEY missing
- Point to `.aura/scripts/requirements.txt` for missing deps

## Target File

**Location**: `aura/src/aura/templates/aura/scripts/transcribe.py`

The script should:
1. Accept audio file path as argument
2. Validate file format and size
3. Split long files into chunks (>8 minutes)
4. Call OpenAI Whisper API
5. Output transcription to stdout

## Key Functions to Preserve

```python
def get_audio_duration_ms(path: str) -> int
def split_audio_into_chunks(path: str, chunk_duration_ms: int) -> list[str]
def transcribe_audio(path: str, model: str) -> str
def transcribe_chunks(chunk_paths: list[str], original_path: str, model: str) -> str
def main()
```

## Usage After Init

```bash
# From any aura-initialized repo
python .aura/scripts/transcribe.py path/to/audio.m4a
```

## Acceptance Criteria

- [ ] Script exists at `aura/src/aura/templates/aura/scripts/transcribe.py`
- [ ] `aura init` copies it to `.aura/scripts/transcribe.py`
- [ ] `python .aura/scripts/transcribe.py audio.m4a` outputs transcription
- [ ] Handles files >8 minutes by chunking
- [ ] Clear error when OPENAI_API_KEY not set
- [ ] Works without any aura/whisper imports

## Notes

- Requires `openai` and `pydub` from requirements.txt
- pydub requires ffmpeg installed on system
- Model default: `gpt-4o-mini-transcribe`
