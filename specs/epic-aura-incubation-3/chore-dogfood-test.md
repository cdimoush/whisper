# Chore: Dogfood Test

## Overview

Verify that aura's commands work when run from the aura repo itself. This is the whole point of the refactor.

## Test Cases

### Test 1: Commands Are Discoverable

In a Claude Code session from aura repo root:
```
/aura.        # Should show autocomplete for all aura.* commands
/beads.       # Should show autocomplete for all beads.* commands
```

### Test 2: Transcription Script Works

```bash
# From aura repo root
cd aura/

# Set up environment
cp .aura/.env.example .env
# Edit .env to add real OPENAI_API_KEY

# Install dependencies
pip install -r .aura/scripts/requirements.txt

# Test transcription (need a test audio file)
python .aura/scripts/transcribe.py /path/to/test.m4a
```

### Test 3: Title Generation Works

```bash
python .aura/scripts/generate_title.py --text "This is a test memo about refactoring the aura project structure"
# Should output something like: aura-structure-refactor
```

### Test 4: /aura.transcribe Works

In Claude Code session:
```
/aura.transcribe /path/to/test.m4a
```

Should:
1. Find `.aura/scripts/transcribe.py`
2. Run transcription
3. Output text

### Test 5: /aura.act Works

In Claude Code session:
```
/aura.act /path/to/test.m4a
```

Should:
1. Transcribe audio
2. Generate title
3. Create `.aura/output/{title}_{timestamp}/`
4. Create README.md with transcription
5. Move audio to output directory

### Test 6: Planning Commands Work

```
/aura.epic "Test feature for dogfooding validation"
```

Should create `specs/epic-test-feature/README.md`

## Acceptance Criteria

- [ ] All `/aura.*` commands visible in Claude Code
- [ ] All `/beads.*` commands visible in Claude Code
- [ ] `python .aura/scripts/transcribe.py` works
- [ ] `python .aura/scripts/generate_title.py` works
- [ ] `/aura.transcribe` works end-to-end
- [ ] `/aura.act` creates output directory correctly
- [ ] `/aura.epic` creates specs correctly

## Notes

- Need a real audio file for full testing
- Need valid OPENAI_API_KEY in .env
- This is the critical validation - if this fails, the refactor isn't complete
