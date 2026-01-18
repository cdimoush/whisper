# Chore: Update Init Logic

## Overview

Change `init.py` to copy from aura's root `.aura/` and `.claude/commands/` instead of `src/aura/templates/`.

## Current Logic (Broken)

```python
# src/aura/init.py
TEMPLATES = Path(__file__).parent / "templates"

def get_template_files():
    aura_templates = TEMPLATES / "aura"      # src/aura/templates/aura/
    claude_templates = TEMPLATES / "claude"  # src/aura/templates/claude/
```

## New Logic (Dogfood-Friendly)

```python
# src/aura/init.py
import importlib.resources

def get_aura_root() -> Path:
    """Find aura package root directory."""
    # When installed: use importlib.resources
    # When developing: traverse up from init.py
    init_path = Path(__file__).resolve()
    # init.py is at aura/src/aura/init.py
    # aura root is 3 levels up
    return init_path.parent.parent.parent

AURA_ROOT = get_aura_root()

def get_template_files():
    files = []

    # .aura/ contents (except queue/, output/)
    aura_source = AURA_ROOT / ".aura"
    for src in aura_source.glob("**/*"):
        if src.is_file():
            rel = src.relative_to(aura_source)
            # Skip queue and output directories
            if rel.parts[0] in ("queue", "output"):
                continue
            dst = Path(".aura") / rel
            files.append((src, dst))

    # .claude/commands/ contents
    claude_source = AURA_ROOT / ".claude" / "commands"
    for src in claude_source.glob("*.md"):
        dst = Path(".claude/commands") / src.name
        files.append((src, dst))

    return files
```

## Key Changes

1. **Path resolution**: Find aura root via file traversal
2. **Source directories**: `.aura/` and `.claude/commands/` at root
3. **Exclusions**: Skip `.aura/queue/` and `.aura/output/`

## Acceptance Criteria

- [ ] `init.py` updated with new path logic
- [ ] `aura init --dry-run` shows correct source paths
- [ ] Skips queue/ and output/ directories
- [ ] Works from aura directory (`uv run aura init --dry-run`)

## Edge Cases

- **Installed via pip/uv**: Path resolution must work
- **Editable install**: Path resolution must work
- **Run from any directory**: Must find aura root correctly

## Testing

```bash
cd aura/
uv run aura init --dry-run

# Should show:
# Would create: .aura/scripts/transcribe.py
# Would create: .aura/scripts/generate_title.py
# etc.
```
