# Chore: Tron Test Fixture

## Description

Create the tron test fixture - a minimal light bike game stub that serves as the target for end-to-end aura workflow testing.

## Tasks

### 1. Create Directory Structure

```
aura/tests/tron/
├── README.md
├── pyproject.toml
└── src/
    └── tron/
        └── __init__.py
```

### 2. Create README.md

**Location**: `aura/tests/tron/README.md`

```markdown
# Tron: Light Bike Game

A minimal light bike game for testing the Aura workflow.

## Game Concept

Tron is a classic arcade game where players control light bikes that leave
trails behind them. The objective is to survive longer than opponents by
avoiding walls and trails.

## Current State

This is a stub project for testing Aura. It contains:
- Basic project structure
- No actual game implementation (yet!)

## Testing Aura

This project is used to validate the full Aura workflow:

1. Initialize Aura: `aura init`
2. Create an epic: `/aura.epic Add player movement`
3. Generate tickets: `/aura.tickets specs/epic-player-movement/`
4. Implement tickets: `/aura.implement <ticket-id>`

## Future Game Features (for testing)

Ideas for features to implement via Aura:
- Player movement (arrow keys)
- Trail rendering
- Collision detection
- Game over screen
- Score tracking
```

### 3. Create pyproject.toml

**Location**: `aura/tests/tron/pyproject.toml`

```toml
[project]
name = "tron"
version = "0.1.0"
description = "Light bike game - Aura test fixture"
requires-python = ">=3.12"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### 4. Create __init__.py

**Location**: `aura/tests/tron/src/tron/__init__.py`

```python
"""Tron: Light Bike Game - Aura test fixture."""

__version__ = "0.1.0"


def main():
    """Placeholder main function."""
    print("Tron game not yet implemented!")
    print("Use Aura to build features for this game.")


if __name__ == "__main__":
    main()
```

## Acceptance Criteria

- [ ] `aura/tests/tron/` directory exists with all files
- [ ] README.md explains the game and testing purpose
- [ ] pyproject.toml is valid Python project config
- [ ] `cd aura/tests/tron && python -m tron` runs without error
- [ ] Fixture is minimal - just enough for testing

## Notes

- This is NOT a real game implementation
- Purpose is to have a target directory for `aura init` testing
- Game features will be "implemented" during the test workflow
- Keep it minimal - the test is about aura, not tron
