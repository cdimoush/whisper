# CLI Contract: Aura

**Version**: 1.0.0
**Date**: 2026-01-18

## Overview

Aura provides a single CLI entry point (`aura`) for installation and initialization. All other commands are Claude Code slash commands (`.claude/commands/*.md`).

## CLI Commands

### `aura --version`

Display version information.

**Output**:
```
aura 0.1.0
```

**Exit codes**:
- 0: Success

---

### `aura --help`

Display help information.

**Output**:
```
Usage: aura [OPTIONS] COMMAND [ARGS]...

  Aura - Agentic workflow layer for codebases

Options:
  --version  Show version and exit
  --help     Show this message and exit

Commands:
  init   Initialize Aura in current directory
  check  Verify prerequisites are installed
```

**Exit codes**:
- 0: Success

---

### `aura init`

Initialize Aura in the current directory.

**Options**:
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--force` | bool | false | Overwrite existing files |
| `--no-beads` | bool | false | Skip beads initialization |
| `--dry-run` | bool | false | Show what would be created |

**Behavior**:
1. Check if `.aura/` exists
   - If exists and no `--force`: warn and skip
   - If exists and `--force`: overwrite
2. Create `.aura/` directory structure
3. Create `.claude/commands/` with aura.* and beads.* commands
   - Merge with existing commands (don't overwrite)
4. If beads (`bd`) is available and not `--no-beads`:
   - Run `bd init` if `.beads/` doesn't exist
5. Report what was created

**Output** (success):
```
Initializing Aura...
  Created .aura/
  Created .aura/config.md
  Created .claude/commands/aura.record.md
  Created .claude/commands/aura.act.md
  Created .claude/commands/aura.transcribe.md
  Created .claude/commands/aura.epic.md
  Created .claude/commands/aura.feature.md
  Created .claude/commands/aura.tickets.md
  Created .claude/commands/aura.implement.md
  Created .claude/commands/aura.prime.md
  Created .claude/commands/beads.status.md
  Created .claude/commands/beads.ready.md
  Created .claude/commands/beads.start.md
  Created .claude/commands/beads.done.md
  Initialized beads task tracking

Aura initialized! Run /aura.prime in Claude Code to get started.
```

**Output** (merge with existing):
```
Initializing Aura...
  Created .aura/
  Skipped .claude/commands/aura.record.md (already exists)
  Created .claude/commands/aura.act.md
  ...

Aura initialized with 10 new commands (2 skipped).
```

**Output** (dry run):
```
Dry run - no files will be created:
  Would create .aura/
  Would create .aura/config.md
  Would create .claude/commands/aura.record.md
  ...
```

**Exit codes**:
- 0: Success
- 1: Error (missing permissions, etc.)

---

### `aura check`

Verify prerequisites are installed.

**Output** (all good):
```
Checking prerequisites...
  ✓ Python 3.12+
  ✓ Claude Code
  ✓ OpenAI API key (OPENAI_API_KEY)
  ✓ sox (audio recording)
  ✓ beads (bd CLI)

All prerequisites met!
```

**Output** (issues found):
```
Checking prerequisites...
  ✓ Python 3.12+
  ✓ Claude Code
  ✗ OpenAI API key (OPENAI_API_KEY not set)
  ✗ sox (brew install sox)
  ✓ beads (bd CLI)

2 issues found. Some features may not work.
```

**Exit codes**:
- 0: All prerequisites met
- 1: Some prerequisites missing (non-fatal warning)

## Slash Commands (Claude Code)

These are not CLI commands but markdown files in `.claude/commands/`. They're invoked via `/command` in Claude Code.

### `/aura.record`

**Input**: None (interactive)
**Output**: Audio file path
**Side effects**: Creates audio file in `.aura/queue/`

---

### `/aura.act <file>`

**Input**: Path to audio file
**Output**: Transcription + deliverables
**Side effects**: Creates output directory, moves audio

---

### `/aura.transcribe <file>`

**Input**: Path to audio file
**Output**: Transcription text only
**Side effects**: None

---

### `/aura.epic <description>`

**Input**: Feature description (text)
**Output**: Epic document
**Side effects**: Creates `specs/<epic-name>/README.md`

---

### `/aura.feature <description>`

**Input**: Feature description (text)
**Output**: Feature plan
**Side effects**: Creates `specs/<feature-name>.md`

---

### `/aura.tickets <epic-path>`

**Input**: Path to epic directory
**Output**: Task creation summary
**Side effects**: Creates beads tasks via `bd create`

---

### `/aura.implement <ticket-id>`

**Input**: Beads task ID
**Output**: Implementation plan + execution
**Side effects**: Modifies codebase per ticket requirements

---

### `/aura.prime`

**Input**: None
**Output**: Project context summary
**Side effects**: None (read-only)

---

### `/beads.status`

**Input**: None
**Output**: Project task overview
**Side effects**: None (calls `bd list`)

---

### `/beads.ready`

**Input**: None
**Output**: Available tasks list
**Side effects**: None (calls `bd ready`)

---

### `/beads.start <id>`

**Input**: Task ID
**Output**: Confirmation
**Side effects**: Updates task status (calls `bd update`)

---

### `/beads.done <id>`

**Input**: Task ID
**Output**: Confirmation
**Side effects**: Updates task status (calls `bd update`)

## Error Handling

All commands should:
1. Validate inputs before proceeding
2. Provide clear error messages
3. Exit with non-zero code on failure
4. Never leave partial state (atomic operations)

**Error format**:
```
Error: <brief description>

<detailed explanation if helpful>

Try: <suggested fix>
```
