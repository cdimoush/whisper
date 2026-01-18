# Beads Workflow for AI Agents

This project uses **bd** (Beads) for AI-native issue tracking and agent memory across sessions.

## Overview

Beads provides persistent task tracking that solves the "agent amnesia" problem. Instead of starting each session from scratch, agents can:
- Check what work is ready via `bd ready`
- Resume in-progress work without re-explaining context
- File discovered subtasks during implementation
- Hand off cleanly at session end

**Quick Start**: Run `bd onboard` to get oriented with current project state.

## Core Concepts

### Task Handles
Each task gets a unique ID like `whisper-k8r`. Use handles in all commands:
```bash
bd show whisper-k8r
bd update whisper-k8r --status in_progress
bd close whisper-k8r
```

### Dependencies
Tasks can depend on other tasks. A task is "ready" only when all its dependencies are complete.
```bash
bd dep add <task> <blocks>   # task depends on blocks
bd dep rm <task> <blocks>    # Remove dependency
```

### Status Lifecycle
- **open**: Created but not started
- **in_progress**: Currently being worked on
- **blocked**: Has incomplete dependencies (derived, not set directly)
- **closed**: Completed

### Git-Backed Storage
- Tasks stored in `.beads/issues.jsonl` (committed to git)
- Local SQLite cache in `.beads/beads.db` (gitignored)
- Sync with `bd sync` after mutations

## When to Use Beads

**Always use Beads for**:
- Multi-step feature implementations
- Work spanning multiple sessions
- Tasks with dependencies
- Anything you'd want to resume later

**Skip Beads for**:
- Quick one-off queries
- Research/exploration (not actionable tasks)
- Trivial single-step changes

## Command Reference

### View Tasks
```bash
bd ready              # Tasks with no blockers (START HERE)
bd list               # All open tasks
bd list --all         # Include closed tasks
bd show <id>          # Full task details including deps
```

### Create/Modify
```bash
bd create "Task title"                    # Create new task
bd create "Task" --description "Details"  # With description
bd update <id> --status in_progress       # Claim work
bd close <id>                             # Complete task
```

### Dependencies
```bash
bd dep add <task> <blocks>   # task depends on blocks
bd dep rm <task> <blocks>    # Remove dependency
```

### Sync
```bash
bd sync               # Sync with git remote
```

## Session Workflow

### Starting a Session

**Always begin by checking task status:**
```bash
bd ready              # "What should I work on?"
```

If resuming previous work:
```bash
bd list --status in_progress  # "What was I working on?"
bd show <active-id>           # "What's the context?"
```

### During Implementation

**Mark work as active:**
```bash
bd update <id> --status in_progress  # Signal you're working on this
```

**File discoveries as you go:**
```bash
bd create "Discovered subtask: add error handling"
bd dep add <new-id> <current-id>  # Optional: block on current work
```

### Ending a Session

**Complete finished work:**
```bash
bd close <id>         # Mark task complete
```

**Ensure changes are pushed (CRITICAL):**
```bash
git pull --rebase
bd sync
git push
git status            # MUST show "up to date with origin"
```

**Work is NOT complete until `git push` succeeds.**

## Best Practices

### DO
- Check `bd ready` at start of every session
- File discoveries immediately (don't let subtasks get forgotten)
- Use `bd update --status in_progress` to signal active work
- Complete tasks promptly (unblocks dependent work)
- Always push changes at session end

### DON'T
- Work on blocked tasks (defeats purpose of dependencies)
- Leave tasks in_progress if not actively working
- Create overly fine-grained tasks (overhead without value)
- Forget to close finished tasks
- End session without pushing (strands work locally)

## Integration with Whisper Commands

### Standard Workflow
Before implementing a spec, check Beads:
```bash
bd ready                              # Find next ready task
bd show <id>                          # Verify matches your intent
bd update <id> --status in_progress   # Mark as active
# ... do implementation ...
bd close <id>                         # Mark complete
```

### Related Slash Commands
- `/implement` - Implements a spec (should check Beads first)
- `/beads-from-epic` - Converts epic README to Beads task graph (Phase 2)
- `/beads-status` - Shows project status (Phase 2)
- `/land` - Session-end cleanup (Phase 2)

## Troubleshooting

### Task doesn't appear in `bd ready`
- Check if it has incomplete dependencies: `bd show <id>`
- Look for "DEPENDS ON" section
- Complete blocking tasks first, or remove dependency if incorrect

### Changes not showing up
- Beads uses local DB cache - should update automatically
- If stale, check `.beads/issues.jsonl` for truth
- Can rebuild: `rm .beads/beads.db && bd list` (regenerates from JSONL)

### `bd` command not found
- Ensure Beads is installed: see README.md installation section
- Check PATH includes `/Users/<you>/.local/bin`
- May need to restart shell or source profile

### Merge conflicts in `.beads/issues.jsonl`
- JSONL is append-only, conflicts should be rare
- Beads has built-in merge driver configured via `.gitattributes`
- If conflicts occur, they typically auto-resolve

## Multi-Agent Coordination

When multiple agents work in parallel (e.g., `/process_queue`):

- Each agent should claim different tasks via `bd update --status in_progress`
- Agents can see each other's active work via `bd list --status in_progress`
- Dependencies prevent agents from working on blocked tasks
- JSONL append-only format minimizes merge conflicts

## Quick Reference

```bash
# Session start
bd ready                              # What's available?

# During work
bd update <id> --status in_progress   # Claim task
bd create "Discovery: ..."            # File subtask

# Session end
bd close <id>                         # Complete task
bd sync && git push                   # Push changes
```

---

*Beads: Issue tracking that moves at the speed of thought*
