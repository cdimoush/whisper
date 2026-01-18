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
            if src.is_file() and src.name != ".gitkeep":
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
