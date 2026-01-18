# Chore: Update Documentation

## Overview

Update README.md and CLAUDE.md to reflect the new dogfood-friendly structure.

## README.md Updates

### Project Structure Section

**Before**:
```markdown
aura/
├── src/aura/
│   ├── templates/
│   │   ├── aura/
│   │   └── claude/
```

**After**:
```markdown
aura/
├── .aura/                  # Working copy (used for development AND as template source)
│   └── scripts/
├── .claude/commands/       # Working copy (used for development AND as template source)
├── src/aura/
│   ├── cli.py
│   └── init.py
```

### Add Dogfooding Section

```markdown
## Development

Aura uses itself for development. The `.aura/` and `.claude/commands/` at the repo root are:

1. **Working copies** - Used when developing aura with Claude Code
2. **Template sources** - Copied to target repos by `aura init`

This means changes to commands are immediately testable without running init.
```

## CLAUDE.md Updates

### Architecture Section

Update the project structure diagram to show:
- `.aura/` at root (not in src/aura/templates/)
- `.claude/commands/` at root
- Explanation that these are both working copies and template sources

### Development Workflow Section

**Before**:
```markdown
1. Make changes to templates in `src/aura/templates/`
2. Test in the tron fixture
```

**After**:
```markdown
1. Make changes to `.aura/` or `.claude/commands/` at repo root
2. Test immediately - changes are live for aura development
3. Optionally verify with tron fixture for init testing
```

### Add Dogfooding Section

```markdown
## Dogfooding

Aura is developed using aura. The commands and scripts at the repo root are the same ones copied to target repos.

**Benefits**:
- Changes are immediately testable
- No template drift between development and distribution
- Aura's own repo demonstrates expected structure
- If it works for us, it works for users

**Workflow**:
1. Edit `.claude/commands/aura.act.md`
2. Run `/aura.act` to test
3. Fix issues, repeat
4. Once working, `aura init` in tron to verify distribution
```

## Acceptance Criteria

- [ ] README.md shows correct project structure
- [ ] README.md explains dogfooding approach
- [ ] CLAUDE.md architecture section updated
- [ ] CLAUDE.md development workflow updated
- [ ] No references to `src/aura/templates/` in docs

## Files to Update

1. `aura/README.md`
2. `aura/CLAUDE.md`
