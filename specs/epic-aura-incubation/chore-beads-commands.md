# Chore: Beads Commands

## Description

Create thin wrapper commands for beads task management: beads.status, beads.ready, beads.start, beads.done. These call the `bd` CLI with formatted output.

## Tasks

### 1. Create beads.status.md

Copy and adapt from `whisper/.claude/commands/beads-status.md`:

**Location**: `aura/src/aura/templates/claude/beads.status.md`

Functionality:
- Show task counts by status (open, in_progress, closed)
- Display progress metrics
- Show currently active work

### 2. Create beads.ready.md

New command:

**Location**: `aura/src/aura/templates/claude/beads.ready.md`

```markdown
# Show Ready Tasks

Display beads tasks that are ready to work on (no blocking dependencies).

## Usage

```
/beads.ready
```

## Instructions

```bash
bd ready
```

Display results as:
```
➡️  Ready to Work On:
  ○ [task-id]: [Title]
  ○ [task-id]: [Title]
```

Or if none: "No tasks ready (all blocked or completed)"
```

### 3. Create beads.start.md

New command:

**Location**: `aura/src/aura/templates/claude/beads.start.md`

```markdown
# Start Working on Task

Mark a beads task as in_progress.

## Usage

```
/beads.start <task-id>
```

## Instructions

```bash
bd update $ARGUMENTS --status in_progress
```

Confirm the update and show the task details.
```

### 4. Create beads.done.md

New command:

**Location**: `aura/src/aura/templates/claude/beads.done.md`

```markdown
# Complete Task

Mark a beads task as closed.

## Usage

```
/beads.done <task-id>
```

## Instructions

```bash
bd update $ARGUMENTS --status closed
```

Confirm the update and show what tasks are now unblocked.
```

## Acceptance Criteria

- [ ] `aura/src/aura/templates/claude/beads.status.md` exists
- [ ] `aura/src/aura/templates/claude/beads.ready.md` exists
- [ ] `aura/src/aura/templates/claude/beads.start.md` exists
- [ ] `aura/src/aura/templates/claude/beads.done.md` exists
- [ ] All commands are thin wrappers around `bd` CLI
- [ ] Commands handle missing beads gracefully (error message if bd not found)

## Notes

- These are intentionally thin wrappers
- No reimplementation of beads functionality
- Beads must be installed separately (`bd` CLI available)
- If beads not initialized, commands should suggest `bd init`
