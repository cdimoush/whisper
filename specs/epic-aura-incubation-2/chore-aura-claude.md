# Chore: Aura CLAUDE.md

## Description

Create CLAUDE.md for the aura project itself - agent instructions for developing aura.

## Target File

**Location**: `aura/CLAUDE.md`

## Purpose

When an agent works on the aura codebase (not a repo wrapped by aura), they need context about:
- How aura is structured
- What the commands do
- How to test changes
- Development workflow

## Structure

```markdown
# Aura - Claude Code Agent Guide

## Project Overview

Aura is an agentic workflow layer that wraps codebases...

## Architecture

### Core Components

1. **CLI** (`src/aura/cli.py`)
   - Entry point for `aura init` and `aura check`

2. **Init Logic** (`src/aura/init.py`)
   - Scaffolding logic for copying templates

3. **Templates** (`src/aura/templates/`)
   - Files copied during init
   - claude/ = slash commands
   - aura/ = .aura directory contents

### How Init Works

[Explanation of the scaffolding process]

## Development Workflow

### Testing Changes

1. Make changes to templates
2. Run `aura init --force` in tests/tron/
3. Test the commands

### Adding a New Command

1. Create template in `src/aura/templates/claude/`
2. Follow naming convention: `aura.<name>.md` or `beads.<name>.md`
3. Update README.md command reference

### Adding a New Script

1. Create script in `src/aura/templates/aura/scripts/`
2. Update requirements.txt if new deps
3. Update relevant command templates to call it

## Key Files

[List of important files with descriptions]

## Testing

[How to test aura changes]

## Common Tasks

[Patterns for common development tasks]
```

## Acceptance Criteria

- [ ] CLAUDE.md exists at `aura/CLAUDE.md`
- [ ] Explains aura's architecture
- [ ] Documents development workflow
- [ ] Lists key files
- [ ] Helps agents understand how to modify aura

## Notes

- This is for developing aura itself
- Different from the CLAUDE.md that might exist in wrapped repos
