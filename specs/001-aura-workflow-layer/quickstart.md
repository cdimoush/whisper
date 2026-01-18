# Quickstart: Aura

Get started with Aura in 5 minutes.

## Installation

### Option 1: UV Tool Install (Recommended)

```bash
uv tool install aura
```

This installs `aura` globally. Verify:

```bash
aura --version
```

### Option 2: Git Clone

```bash
git clone https://github.com/yourusername/aura.git
cd aura
uv sync
```

## Initialize a Project

Navigate to any codebase and run:

```bash
aura init
```

This creates:
- `.aura/` - Aura configuration and queue
- `.beads/` - Task tracking (via beads)
- `.claude/commands/` - Slash commands for Claude Code

## Basic Workflow

### 1. Record a Voice Memo

In Claude Code, run:

```
/aura.record
```

Speak your idea, then stop recording. The audio is saved to `.aura/queue/`.

### 2. Act on the Memo

```
/aura.act path/to/audio.m4a
```

This:
1. Transcribes the audio
2. Interprets your request
3. Creates appropriate deliverables

### 3. Create an Epic

For larger features:

```
/aura.epic Add user authentication with OAuth support
```

Creates a structured epic document in `specs/`.

### 4. Generate Tickets

```
/aura.tickets specs/user-auth-epic/
```

Converts the epic into beads tasks with dependencies.

### 5. Work Through Tasks

```
/beads.status     # See project overview
/beads.ready      # See available tasks
/beads.start 001  # Start working on task 001
/beads.done 001   # Mark task 001 complete
```

### 6. Implement from Ticket

```
/aura.implement 002
```

Reads ticket 002 and helps you implement it.

## Command Reference

| Command | Purpose |
|---------|---------|
| `/aura.record` | Record voice memo |
| `/aura.act <file>` | Transcribe and act on audio |
| `/aura.transcribe <file>` | Transcription only |
| `/aura.epic <desc>` | Create epic document |
| `/aura.feature <desc>` | Create feature plan |
| `/aura.tickets <epic>` | Convert plan to tasks |
| `/aura.implement <id>` | Execute task work |
| `/aura.prime` | Load project context |
| `/beads.status` | Task overview |
| `/beads.ready` | Available tasks |
| `/beads.start <id>` | Begin task |
| `/beads.done <id>` | Complete task |

## Prerequisites

- Claude Code installed
- OpenAI API key (for transcription)
- `sox` installed (for recording): `brew install sox`
- Beads CLI (optional): `uv tool install beads`

## Example: Full Workflow

```bash
# 1. Initialize in your project
cd my-project
aura init

# 2. Open Claude Code
claude

# 3. Record your idea
> /aura.record
# "I want to add a dark mode toggle to the settings page..."

# 4. Create an epic from recording
> /aura.act .aura/queue/latest.m4a

# 5. Generate tasks
> /aura.tickets specs/dark-mode-epic/

# 6. See what's ready
> /beads.ready

# 7. Start implementing
> /aura.implement 001
```

## Next Steps

- Read [spec.md](./spec.md) for full requirements
- Read [plan.md](./plan.md) for implementation details
- Check [data-model.md](./data-model.md) for entity definitions
