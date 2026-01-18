# Feature: Init Command

## Feature Description

Implement the `aura init` command that scaffolds .aura/, .beads/, and .claude/commands/ directories in any target codebase.

## User Story

As a developer
I want to run `aura init` in my project
So that I get all the aura workflow commands without manual setup

## Problem

Setting up aura manually requires creating multiple directories and copying 12+ command files. This is error-prone and tedious.

## Solution

A single `aura init` command that:
1. Creates .aura/ directory with config
2. Creates .claude/commands/ with all aura.* and beads.* templates
3. Optionally initializes beads (if `bd` is available)
4. Merges with existing .claude/commands/ (doesn't overwrite)

## Relevant Files

### Files to Modify
- `aura/src/aura/cli.py` - Add init command

### New Files
- `aura/src/aura/init.py` - Scaffolding logic

## Step by Step Tasks

### 1. Implement Core Init Logic

Create `aura/src/aura/init.py`:

```python
"""Aura initialization logic."""

import shutil
from pathlib import Path

TEMPLATES = Path(__file__).parent / "templates"


def get_template_files():
    """Return list of (src, dst) tuples for all template files."""
    files = []

    # .aura/ templates
    aura_templates = TEMPLATES / "aura"
    if aura_templates.exists():
        for src in aura_templates.glob("**/*"):
            if src.is_file():
                rel = src.relative_to(aura_templates)
                dst = Path(".aura") / rel
                files.append((src, dst))

    # .claude/commands/ templates
    claude_templates = TEMPLATES / "claude"
    if claude_templates.exists():
        for src in claude_templates.glob("*.md"):
            dst = Path(".claude/commands") / src.name
            files.append((src, dst))

    return files


def init_aura(force: bool = False, dry_run: bool = False, no_beads: bool = False):
    """Initialize Aura in current directory."""
    results = {"created": [], "skipped": [], "errors": []}

    for src, dst in get_template_files():
        if dry_run:
            if dst.exists() and not force:
                results["skipped"].append(str(dst))
            else:
                results["created"].append(str(dst))
            continue

        try:
            if dst.exists() and not force:
                results["skipped"].append(str(dst))
                continue

            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dst)
            results["created"].append(str(dst))
        except Exception as e:
            results["errors"].append(f"{dst}: {e}")

    # Initialize beads if available and not skipped
    if not no_beads and not dry_run:
        beads_dir = Path(".beads")
        if not beads_dir.exists():
            try:
                import subprocess
                subprocess.run(["bd", "init"], check=True, capture_output=True)
                results["created"].append(".beads/ (via bd init)")
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass  # bd not available, skip silently

    return results
```

### 2. Add Init Command to CLI

Update `aura/src/aura/cli.py`:

```python
"""Aura CLI entry point."""

import click
from aura.init import init_aura


@click.group()
@click.version_option()
def main():
    """Aura - Agentic workflow layer for codebases."""
    pass


@main.command()
@click.option("--force", is_flag=True, help="Overwrite existing files")
@click.option("--dry-run", is_flag=True, help="Show what would be created")
@click.option("--no-beads", is_flag=True, help="Skip beads initialization")
def init(force, dry_run, no_beads):
    """Initialize Aura in current directory."""
    if dry_run:
        click.echo("Dry run - no files will be created:\n")
    else:
        click.echo("Initializing Aura...\n")

    results = init_aura(force=force, dry_run=dry_run, no_beads=no_beads)

    for path in results["created"]:
        prefix = "Would create" if dry_run else "Created"
        click.echo(f"  {prefix} {path}")

    for path in results["skipped"]:
        click.echo(f"  Skipped {path} (already exists)")

    for error in results["errors"]:
        click.echo(f"  Error: {error}", err=True)

    if not dry_run:
        created = len(results["created"])
        skipped = len(results["skipped"])
        click.echo(f"\nAura initialized! ({created} created, {skipped} skipped)")
        click.echo("Run /aura.prime in Claude Code to get started.")


if __name__ == "__main__":
    main()
```

### 3. Add Check Command (Optional)

```python
@main.command()
def check():
    """Verify prerequisites are installed."""
    import subprocess
    import os

    checks = [
        ("Python 3.12+", lambda: True),  # We're running, so yes
        ("Claude Code", lambda: shutil.which("claude") is not None),
        ("OPENAI_API_KEY", lambda: os.environ.get("OPENAI_API_KEY") is not None),
        ("sox", lambda: shutil.which("sox") is not None),
        ("beads (bd)", lambda: shutil.which("bd") is not None),
    ]

    click.echo("Checking prerequisites...\n")
    issues = 0

    for name, check_fn in checks:
        try:
            if check_fn():
                click.echo(f"  ✓ {name}")
            else:
                click.echo(f"  ✗ {name}")
                issues += 1
        except Exception:
            click.echo(f"  ✗ {name}")
            issues += 1

    if issues:
        click.echo(f"\n{issues} issues found. Some features may not work.")
        raise SystemExit(1)
    else:
        click.echo("\nAll prerequisites met!")
```

## Acceptance Criteria

- [ ] `aura init --help` shows all options
- [ ] `aura init --dry-run` shows what would be created without writing
- [ ] `aura init` in empty dir creates .aura/ and .claude/commands/
- [ ] `aura init` with existing .claude/ merges without overwriting
- [ ] `aura init --force` overwrites existing files
- [ ] `aura init --no-beads` skips beads initialization
- [ ] `aura check` reports prerequisite status

## Validation Commands

```bash
# Test in a temp directory
cd /tmp && mkdir test-aura && cd test-aura
python -m aura.cli init --dry-run
python -m aura.cli init
ls -la .aura/ .claude/commands/
python -m aura.cli check
```

## Notes

- Templates directory must be populated (Phase 2) for init to copy files
- Beads initialization is optional and silent if bd not available
- Merge logic preserves user customizations in .claude/commands/
