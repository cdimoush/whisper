# Chore: Voice Commands

## Description

Create the voice input command templates: aura.record, aura.act, aura.transcribe. These are copied from whisper's existing commands with namespace prefix.

## Tasks

### 1. Create aura.record.md

Copy and adapt from `whisper/.claude/commands/record_memo.md`:

**Location**: `aura/src/aura/templates/claude/aura.record.md`

Key changes:
- Update paths to use `.aura/queue/` instead of `queue/`
- Update command references to use `aura.` prefix

### 2. Create aura.transcribe.md

Copy and adapt from `whisper/.claude/commands/transcribe.md`:

**Location**: `aura/src/aura/templates/claude/aura.transcribe.md`

Key changes:
- Simple transcription-only command
- Output to stdout or specified file

### 3. Create aura.act.md

Copy and adapt from `whisper/.claude/commands/act.md`:

**Location**: `aura/src/aura/templates/claude/aura.act.md`

Key changes:
- Update paths to use `.aura/queue/` and `.aura/output/`
- Reference aura.transcribe for transcription step
- Update to use project's CLAUDE.md for context (not brain/)

## Source Files to Copy From

```
whisper/.claude/commands/record_memo.md → aura.record.md
whisper/.claude/commands/transcribe.md  → aura.transcribe.md
whisper/.claude/commands/act.md         → aura.act.md
```

## Acceptance Criteria

- [ ] `aura/src/aura/templates/claude/aura.record.md` exists
- [ ] `aura/src/aura/templates/claude/aura.transcribe.md` exists
- [ ] `aura/src/aura/templates/claude/aura.act.md` exists
- [ ] All templates reference `.aura/` paths
- [ ] After `aura init`, `/aura.record` is available in Claude Code

## Notes

- These are markdown templates, not Python code
- The actual transcription uses OpenAI API (requires OPENAI_API_KEY)
- Recording requires sox to be installed
- Focus on path updates, not feature changes
