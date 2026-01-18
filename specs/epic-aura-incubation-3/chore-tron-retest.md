# Chore: Tron Re-test

## Overview

Verify that `aura init` still works correctly for target repositories after the init.py refactor.

## Test Setup

```bash
cd aura/tests/tron/

# Clean previous init
rm -rf .aura .claude .beads

# Run fresh init
uv run aura init
```

## Verification Checks

### Check 1: Directory Structure

```bash
ls -la .aura/
# Should show:
# scripts/
# .gitignore
# .env.example

ls -la .aura/scripts/
# Should show:
# transcribe.py
# generate_title.py
# requirements.txt

ls -la .claude/commands/
# Should show all 12 command files
```

### Check 2: File Contents Match Source

```bash
diff .aura/scripts/transcribe.py ../../.aura/scripts/transcribe.py
# Should be identical

diff .claude/commands/aura.act.md ../../.claude/commands/aura.act.md
# Should be identical
```

### Check 3: Scripts Work

```bash
cd tests/tron/

# Test title generation (doesn't need audio)
python .aura/scripts/generate_title.py --text "Testing tron fixture initialization"
# Should output a kebab-case title
```

### Check 4: Commands Reference Correct Paths

```bash
grep "\.aura/scripts/" .claude/commands/aura.act.md
# Should find references to .aura/scripts/transcribe.py
# Should find references to .aura/scripts/generate_title.py
```

### Check 5: Dry Run Shows Correct Sources

```bash
cd tests/tron/
rm -rf .aura .claude .beads
uv run aura init --dry-run

# Should show files being copied FROM aura root .aura/ and .claude/
# NOT from src/aura/templates/
```

## Acceptance Criteria

- [ ] `aura init` completes without errors
- [ ] `.aura/scripts/` contains all three files
- [ ] `.claude/commands/` contains all 12 command files
- [ ] File contents match source files exactly
- [ ] Scripts are executable and work
- [ ] No references to `src/aura/templates/` anywhere

## Edge Cases

- [ ] `aura init --force` overwrites existing files
- [ ] `aura init --no-beads` skips beads initialization
- [ ] `aura init --dry-run` shows correct output without creating files
