# Chore: Update Root .gitignore

## Overview

Update aura's root `.gitignore` to ignore `.aura/queue/`, `.aura/output/`, and `.env` so development artifacts aren't committed.

## Current State

Aura repo may have a `.gitignore` but it doesn't account for the new root-level `.aura/` directory.

## Required Ignores

```gitignore
# Aura development artifacts
.aura/queue/
.aura/output/
.env

# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/

# IDE
.idea/
.vscode/
*.swp
```

## Implementation

1. Check if aura has a root `.gitignore`
2. Add aura-specific ignores if missing
3. Verify `.aura/scripts/` is NOT ignored (we want to commit scripts)

## Acceptance Criteria

- [ ] `.aura/queue/` is gitignored
- [ ] `.aura/output/` is gitignored
- [ ] `.env` is gitignored
- [ ] `.aura/scripts/` is NOT gitignored
- [ ] `.claude/commands/` is NOT gitignored

## Verification

```bash
cd aura/
mkdir -p .aura/queue .aura/output
touch .aura/queue/test.wav .aura/output/test.md
git status  # Should NOT show queue/output files

touch .aura/scripts/test.py
git status  # SHOULD show scripts/test.py
rm .aura/scripts/test.py
```
