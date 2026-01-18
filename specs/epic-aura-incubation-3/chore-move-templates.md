# Chore: Move Templates to Root

## Overview

Move `.aura/` and `.claude/commands/` from `src/aura/templates/` to the aura repo root so aura can dogfood itself.

## Current Location

```
aura/src/aura/templates/
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
    └── ... (12 files total)
```

## Target Location

```
aura/
├── .aura/
│   ├── scripts/
│   │   ├── transcribe.py
│   │   ├── generate_title.py
│   │   └── requirements.txt
│   ├── .gitignore
│   └── .env.example
└── .claude/
    └── commands/
        ├── aura.act.md
        ├── aura.epic.md
        └── ... (12 files total)
```

## Implementation

```bash
cd aura/

# Move .aura/ contents
mkdir -p .aura
cp -r src/aura/templates/aura/* .aura/

# Move .claude/commands/ contents
mkdir -p .claude/commands
cp src/aura/templates/claude/*.md .claude/commands/

# Verify
ls -la .aura/scripts/
ls -la .claude/commands/
```

## Acceptance Criteria

- [ ] `.aura/scripts/transcribe.py` exists at aura repo root
- [ ] `.aura/scripts/generate_title.py` exists at aura repo root
- [ ] `.aura/scripts/requirements.txt` exists at aura repo root
- [ ] `.aura/.gitignore` exists at aura repo root
- [ ] `.aura/.env.example` exists at aura repo root
- [ ] `.claude/commands/` contains all 12 command files
- [ ] Original templates still exist (removed in Phase 4)

## Notes

- Use `cp` not `mv` - we'll remove originals after validation
- Creates queue/ and output/ directories as needed by .gitignore
