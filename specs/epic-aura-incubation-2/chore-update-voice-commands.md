# Chore: Update Voice Commands

## Description

Update `aura.record.md`, `aura.transcribe.md`, and `aura.act.md` templates to reference `.aura/scripts/` instead of assuming whisper's structure.

## Files to Update

### 1. aura.transcribe.md

**Location**: `aura/src/aura/templates/claude/aura.transcribe.md`

**Change**: Update to call local script

```markdown
## Instructions

1. Validate the audio file exists
2. Run transcription:
   ```bash
   python .aura/scripts/transcribe.py "$ARGUMENTS"
   ```
3. Output the transcription
```

### 2. aura.act.md

**Location**: `aura/src/aura/templates/claude/aura.act.md`

**Changes**:
- Use `.aura/scripts/transcribe.py` for transcription
- Use `.aura/scripts/generate_title.py` for directory naming
- Output to `.aura/output/<title>_<timestamp>/`

```markdown
## Instructions

1. Transcribe the audio:
   ```bash
   TRANSCRIPT=$(python .aura/scripts/transcribe.py "$AUDIO_PATH")
   ```

2. Generate intelligent title:
   ```bash
   TITLE=$(python .aura/scripts/generate_title.py "$TRANSCRIPT")
   ```

3. Create output directory:
   ```bash
   TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
   OUTPUT_DIR=".aura/output/${TITLE}_${TIMESTAMP}"
   mkdir -p "$OUTPUT_DIR"
   ```

4. Save transcription and create deliverables
```

### 3. aura.record.md

**Location**: `aura/src/aura/templates/claude/aura.record.md`

**Changes**:
- Save to `.aura/queue/` not `queue/`
- Reference proper paths

```markdown
## Instructions

1. Start recording:
   ```bash
   FILENAME=".aura/queue/memo_$(date +%Y%m%d_%H%M%S).wav"
   mkdir -p .aura/queue
   sox -d "$FILENAME"
   ```

2. Report saved location
```

## Acceptance Criteria

- [ ] `aura.transcribe.md` calls `.aura/scripts/transcribe.py`
- [ ] `aura.act.md` calls both transcribe and generate_title scripts
- [ ] `aura.act.md` outputs to `.aura/output/`
- [ ] `aura.record.md` saves to `.aura/queue/`
- [ ] No whisper-specific paths remain
- [ ] Commands work in any aura-initialized repo

## Notes

- These templates are the "glue" between Claude and the scripts
- Scripts do the heavy lifting, templates orchestrate
