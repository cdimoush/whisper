# Chore: Fix Template Paths

## Overview

Audit all command templates to ensure paths are correct after the move. Most should already be correct since they reference `.aura/scripts/` which is the target location.

## Files to Audit

```
.claude/commands/
├── aura.act.md         # Uses .aura/scripts/, .aura/output/
├── aura.transcribe.md  # Uses .aura/scripts/
├── aura.record.md      # Uses .aura/queue/
├── aura.epic.md        # Uses specs/
├── aura.feature.md     # Uses specs/
├── aura.tickets.md     # Uses specs/, beads
├── aura.implement.md   # Uses beads
├── aura.prime.md       # Reads project files
├── beads.status.md     # Uses bd CLI
├── beads.ready.md      # Uses bd CLI
├── beads.start.md      # Uses bd CLI
└── beads.done.md       # Uses bd CLI
```

## Expected Paths (Should Already Be Correct)

| Reference | Expected Value |
|-----------|---------------|
| Transcription script | `.aura/scripts/transcribe.py` |
| Title generation | `.aura/scripts/generate_title.py` |
| Requirements | `.aura/scripts/requirements.txt` |
| Audio queue | `.aura/queue/` |
| Output directory | `.aura/output/` |
| Specs directory | `specs/` |

## Audit Process

1. Grep for any `src/aura/templates` references (should be zero)
2. Grep for any `templates/` references (should be zero)
3. Verify all `.aura/` paths are relative (not absolute)

```bash
cd aura/
grep -r "src/aura/templates" .claude/commands/
grep -r "templates/" .claude/commands/
grep -r "/Users/" .claude/commands/  # No absolute paths
```

## Acceptance Criteria

- [ ] No references to `src/aura/templates/` in any command
- [ ] No absolute paths in any command
- [ ] All `.aura/scripts/` references are correct
- [ ] All `.aura/queue/` references are correct
- [ ] All `.aura/output/` references are correct

## Notes

This is likely a no-op since templates were written with target paths in mind. But we must verify.
