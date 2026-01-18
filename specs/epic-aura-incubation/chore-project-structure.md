# Chore: Aura Project Structure

## Description

Create the `aura/` directory structure inside whisper for incubation. This establishes the foundation for the init CLI and template files.

## Tasks

### 1. Create Directory Structure

```
aura/
├── pyproject.toml
├── src/
│   └── aura/
│       ├── __init__.py
│       ├── cli.py
│       └── templates/
│           ├── aura/
│           │   └── .gitkeep
│           └── claude/
│               └── .gitkeep
└── tests/
    └── tron/
        └── .gitkeep
```

### 2. Create pyproject.toml

```toml
[project]
name = "aura"
version = "0.1.0"
description = "Agentic workflow layer for codebases"
requires-python = ">=3.12"
dependencies = [
    "click>=8.0",
]

[project.scripts]
aura = "aura.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/aura"]
```

### 3. Create __init__.py

```python
"""Aura - Agentic workflow layer for codebases."""

__version__ = "0.1.0"
```

### 4. Create Placeholder cli.py

```python
"""Aura CLI entry point."""

import click


@click.group()
@click.version_option()
def main():
    """Aura - Agentic workflow layer for codebases."""
    pass


if __name__ == "__main__":
    main()
```

## Acceptance Criteria

- [ ] `aura/` directory exists in whisper root
- [ ] `cd aura && uv sync` succeeds
- [ ] `cd aura && python -m aura.cli --version` outputs "0.1.0"
- [ ] `cd aura && python -m aura.cli --help` shows usage

## Notes

- This is infrastructure setup, no user-facing functionality yet
- pyproject.toml configured for future `uv tool install` support
- Template directories created empty, populated in Phase 2
