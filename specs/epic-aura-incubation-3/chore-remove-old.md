# Chore: Remove Old Templates

## Overview

Delete `src/aura/templates/` directory now that templates live at repo root.

## Prerequisites

- Phase 3 validation complete (dogfood and tron tests pass)
- User has confirmed both test passes

## Implementation

```bash
cd aura/

# Verify templates still exist
ls src/aura/templates/

# Remove the old templates directory
rm -rf src/aura/templates/

# Verify removal
ls src/aura/
# Should show: __init__.py, cli.py, init.py (no templates/)
```

## Files Being Removed

```
src/aura/templates/
├── aura/
│   ├── scripts/
│   │   ├── transcribe.py
│   │   ├── generate_title.py
│   │   └── requirements.txt
│   ├── .gitignore
│   └── .env.example
└── claude/
    ├── aura.act.md
    ├── aura.epic.md
    ├── aura.feature.md
    ├── aura.implement.md
    ├── aura.prime.md
    ├── aura.record.md
    ├── aura.tickets.md
    ├── aura.transcribe.md
    ├── beads.done.md
    ├── beads.ready.md
    ├── beads.start.md
    └── beads.status.md
```

## Post-Removal Verification

```bash
# Init should still work (uses root .aura/ and .claude/)
cd tests/tron/
rm -rf .aura .claude .beads
uv run aura init
ls .aura/scripts/  # Should still work
```

## Acceptance Criteria

- [ ] `src/aura/templates/` directory deleted
- [ ] `aura init` still works after deletion
- [ ] No broken imports or path errors
- [ ] Git status shows deletion of templates/

## Rollback

If something breaks:
```bash
git checkout -- src/aura/templates/
```

Only remove after confirming all tests pass.
