# Aura - Claude Code Agent Guide

This document provides context for Claude Code agents working on the Aura project itself (not repos wrapped by Aura).

## Project Overview

Aura is an agentic workflow layer that scaffolds repositories with Claude Code slash commands for voice-driven development. It enables a workflow where developers speak ideas into voice memos, which are transcribed and turned into structured plans and implementations.

**Core Philosophy**: Remove friction between ideas and code. Voice is faster than typing.

## Architecture

### Project Structure

```
aura/
├── src/aura/
│   ├── __init__.py          # Package init
│   ├── cli.py               # Click CLI entry point
│   └── init.py              # Scaffolding logic
├── src/aura/templates/
│   ├── aura/                # Files copied to .aura/
│   │   ├── .gitignore       # Ignores queue/, output/, .env
│   │   └── scripts/
│   │       ├── transcribe.py
│   │       ├── generate_title.py
│   │       └── requirements.txt
│   └── claude/              # Files copied to .claude/commands/
│       ├── aura.*.md        # Aura slash commands
│       └── beads.*.md       # Beads slash commands
├── tests/
│   └── tron/                # Test fixture for init
├── pyproject.toml           # Package metadata
└── README.md                # User documentation
```

### Core Components

#### CLI (`src/aura/cli.py`)

Entry point for `aura init` and `aura check` commands:

```python
@click.group()
def cli(): ...

@cli.command()
@click.option("--force", is_flag=True)
@click.option("--dry-run", is_flag=True)
@click.option("--no-beads", is_flag=True)
def init(force, dry_run, no_beads): ...

@cli.command()
def check(): ...
```

#### Init Logic (`src/aura/init.py`)

Handles template file discovery and copying:

```python
def get_template_files() -> list[tuple[Path, Path]]:
    """Returns (src, dst) pairs for all template files."""

def init_aura(force=False, dry_run=False, no_beads=False) -> dict:
    """Copies templates to current directory, returns results."""
```

The init process:
1. Globs all files in `templates/aura/**/*` → copies to `.aura/`
2. Globs all files in `templates/claude/*.md` → copies to `.claude/commands/`
3. Runs `bd init` if beads CLI available and not skipped

#### Templates

**Aura templates** (`templates/aura/`):
- Copied to `.aura/` in target repository
- Contains scripts and configuration
- Scripts are self-contained (no aura/whisper imports)

**Claude templates** (`templates/claude/`):
- Copied to `.claude/commands/` in target repository
- Markdown files with frontmatter for Claude Code
- Define slash commands available in Claude Code sessions

### Template Anatomy

Claude Code command templates have this structure:

```markdown
---
allowed-tools: Bash(python:*), Read, Write
description: Short description for command listing
argument-hint: <required> [optional]
---

# Command Name

Instructions for the agent...

## Steps

1. Do this
2. Then this
```

The frontmatter controls:
- `allowed-tools`: Which tools the command can use
- `description`: Shows in `/help` listing
- `argument-hint`: Shows expected arguments

## Development Workflow

### Testing Changes

1. Make changes to templates in `src/aura/templates/`
2. Test in the tron fixture:
   ```bash
   cd tests/tron
   uv run aura init --force
   ```
3. Verify files were created:
   ```bash
   ls -la .aura/scripts/
   cat .claude/commands/aura.act.md
   ```

### Adding a New Command

1. Create template in `src/aura/templates/claude/`:
   ```bash
   # Naming convention: aura.<name>.md or beads.<name>.md
   touch src/aura/templates/claude/aura.newcommand.md
   ```

2. Add frontmatter and instructions:
   ```markdown
   ---
   allowed-tools: Read, Glob
   description: What this command does
   argument-hint: <required-arg>
   ---

   # Command Title

   Instructions...
   ```

3. Update README.md command reference

4. Test with `aura init --force` in tron

### Adding a New Script

1. Create script in `src/aura/templates/aura/scripts/`:
   ```bash
   touch src/aura/templates/aura/scripts/newscript.py
   ```

2. Ensure script is self-contained:
   - No imports from `aura` or `whisper` packages
   - All dependencies in `requirements.txt`
   - Works from any working directory
   - Outputs to stdout, errors to stderr

3. Update `requirements.txt` if new dependencies needed

4. Update relevant command templates to call the script

### Running Tests

```bash
# From aura directory
cd tests/tron

# Clean and reinitialize
rm -rf .aura .claude .beads
uv run aura init

# Verify structure
ls -la .aura/scripts/
cat .aura/scripts/requirements.txt

# Test transcription script (requires audio file and API key)
OPENAI_API_KEY=sk-xxx python .aura/scripts/transcribe.py test.m4a
```

## Key Files

| File | Purpose |
|------|---------|
| `src/aura/cli.py` | CLI commands (`init`, `check`) |
| `src/aura/init.py` | Scaffolding logic |
| `templates/claude/*.md` | Slash command templates |
| `templates/aura/scripts/*.py` | Portable Python scripts |
| `tests/tron/` | Test fixture for initialization |
| `README.md` | User documentation |
| `CLAUDE.md` | This file - agent guide |

## Common Tasks

### Modify a Slash Command

1. Edit the template in `src/aura/templates/claude/`
2. Test: `cd tests/tron && uv run aura init --force`
3. Verify: `cat .claude/commands/<command>.md`

### Change Script Behavior

1. Edit the script in `src/aura/templates/aura/scripts/`
2. Test: `cd tests/tron && uv run aura init --force`
3. Run script directly to verify:
   ```bash
   python .aura/scripts/transcribe.py test.m4a
   ```

### Add Template File

1. Create file in appropriate templates directory
2. The init logic auto-discovers files via glob patterns
3. No code changes needed in init.py
4. Test with `aura init --force`

### Debug Init Issues

Check dry-run output:
```bash
uv run aura init --dry-run
```

This shows all files that would be created without creating them.

## Design Decisions

### Why Self-Contained Scripts?

Scripts in `.aura/scripts/` don't import from aura or whisper packages because:
1. Target repos don't have aura installed as a package
2. Simpler dependency management (just requirements.txt)
3. Users can modify scripts without understanding the full package

### Why Copy vs Symlink?

Templates are copied (not symlinked) because:
1. Target repos shouldn't depend on aura installation location
2. Users can customize their copies
3. Works across different machines/environments

### Why Beads Integration?

Beads provides dependency-aware task management that pairs well with epic/feature planning. It's optional - aura works without it, but the workflow is enhanced with it.

## Future Work

- `aura check` command to validate setup
- `.aura/config.md` for project-specific configuration
- Plugin system for custom commands
- `uv tool install` support for global installation
- Multi-agent tool support (Cursor, Copilot, etc.)

## Troubleshooting

### Templates Not Copying

Check that files exist in templates directory:
```bash
ls -la src/aura/templates/aura/scripts/
ls -la src/aura/templates/claude/
```

### Init Fails Silently

Run with verbose output:
```bash
uv run aura init --dry-run
```

### Script Dependencies Missing

Ensure requirements.txt is complete:
```bash
cat src/aura/templates/aura/scripts/requirements.txt
```

---

*Last updated: 2026-01-18*
