# Implementation Plan: Aura - Agentic Workflow Layer

**Branch**: `001-aura-workflow-layer` | **Date**: 2026-01-18 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-aura-workflow-layer/spec.md`

## Summary

Aura is a portable agentic workflow layer that wraps any codebase with voice-driven development capabilities. It provides a CLI (`aura init`) that scaffolds `.aura/`, `.beads/`, and `.claude/commands/` directories. Core workflow: voice memo → transcription → epic/ticket planning → beads task execution → implementation. Includes a test fixture (tron light bike game) for end-to-end validation.

## Technical Context

**Language/Version**: Python 3.12+ (matching whisper, modern features)
**Primary Dependencies**: openai (transcription), click (CLI), shutil/pathlib (file operations)
**Storage**: File-based (markdown specs, .claude/ commands, .beads/ tasks)
**Testing**: pytest with tmp_path fixtures for filesystem tests
**Target Platform**: macOS/Linux CLI (Unix-like environments)
**Project Type**: Single CLI tool with installable package
**Performance Goals**: Init < 30s, transcription < 60s for 5min audio
**Constraints**: No binary blobs, git-friendly output, offline-capable for non-transcription features
**Scale/Scope**: Single developer workflow, local execution

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Since no project constitution exists yet, applying lean development principles:

| Principle | Status | Notes |
|-----------|--------|-------|
| Simplicity First | PASS | CLI + markdown files, no databases |
| File-based Storage | PASS | All state in .aura/, .beads/, .claude/ |
| Portable/Committable | PASS | Everything scaffolded is git-friendly |
| Thin Wrappers | PASS | beads.* commands wrap bd CLI |
| Reuse Existing Code | PASS | Transcription from whisper |

No violations. Proceeding to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/001-aura-workflow-layer/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (CLI interface specs)
├── checklists/          # Validation checklists
│   └── requirements.md
└── tasks.md             # Phase 2 output (from /speckit.tasks)
```

### Source Code (Aura repository root)

```text
aura/                           # Repository root (new GitHub repo)
├── pyproject.toml              # Package definition, uv/pip installable
├── README.md                   # User-facing documentation
├── CLAUDE.md                   # Agent instructions for aura development
│
├── src/
│   └── aura/
│       ├── __init__.py
│       ├── cli.py              # Click CLI entry point (aura init, etc.)
│       ├── init.py             # Scaffolding logic
│       ├── transcribe.py       # OpenAI whisper transcription (from whisper)
│       └── templates/          # Files to copy during init
│           ├── aura/           # .aura/ template files
│           │   └── config.md
│           ├── claude/         # .claude/commands/ templates
│           │   ├── aura.record.md
│           │   ├── aura.act.md
│           │   ├── aura.transcribe.md
│           │   ├── aura.epic.md
│           │   ├── aura.feature.md
│           │   ├── aura.tickets.md
│           │   ├── aura.implement.md
│           │   ├── aura.prime.md
│           │   ├── beads.status.md
│           │   ├── beads.ready.md
│           │   ├── beads.start.md
│           │   └── beads.done.md
│           └── beads/          # .beads/ template (or rely on bd init)
│
├── tests/
│   ├── unit/
│   │   ├── test_init.py
│   │   └── test_transcribe.py
│   ├── integration/
│   │   └── test_full_workflow.py
│   └── tron/                   # Test fixture: light bike game
│       ├── README.md           # Game description
│       ├── pyproject.toml      # Minimal Python setup
│       └── src/
│           └── tron/
│               └── __init__.py # Placeholder game code
│
└── examples/
    └── sample_transcript.txt   # Example voice memo transcript for testing
```

**Structure Decision**: Single project structure. Aura is a CLI tool that scaffolds files into target codebases. No backend/frontend split needed.

## Complexity Tracking

No complexity violations. Design is minimal:
- Single CLI entry point
- File copy operations for scaffolding
- Thin wrappers around existing tools (bd CLI, whisper transcription)
- Markdown templates for commands

## Phase 0: Research Summary

### Decision 1: Installation Method

**Decision**: Support both `git clone` and `uv tool install aura`
**Rationale**: uv tool install provides global CLI availability; git clone allows local customization
**Alternatives**: pip install (less modern), npm (wrong ecosystem)

### Decision 2: Beads Integration

**Decision**: Thin wrapper commands that shell out to `bd` CLI
**Rationale**: Beads already works well; no need to reimplement. Commands like `/beads.status` just call `bd list`
**Alternatives**: Direct beads library import (tighter coupling, harder to update)

### Decision 3: Transcription

**Decision**: Port whisper's transcription code directly into aura
**Rationale**: Already battle-tested, handles chunking, uses OpenAI API
**Alternatives**: Separate whisper dependency (extra install step)

### Decision 4: Command Namespace

**Decision**: Prefix all commands with `aura.` or `beads.`
**Rationale**: Clear ownership, avoids conflicts with existing commands in target repos
**Alternatives**: No prefix (collision risk), single `aura/` directory (less discoverable)

### Decision 5: Test Fixture (tron)

**Decision**: Minimal Python game stub with README
**Rationale**: Just enough to demonstrate aura workflow; actual game logic out of scope
**Alternatives**: Full game implementation (scope creep), no fixture (harder to validate)

## Phase 1: Design Artifacts

See companion files:
- [data-model.md](./data-model.md) - Entity definitions
- [quickstart.md](./quickstart.md) - Getting started guide
- [contracts/cli.md](./contracts/cli.md) - CLI interface specification

## Implementation Phases

### Phase 1: Core Init (P1 Stories)

1. Create aura repository structure
2. Implement `aura init` command
3. Create all `.claude/commands/` templates
4. Port transcription code from whisper
5. Test: run `aura init` in empty directory

### Phase 2: Voice Workflow (P1 Stories)

1. Implement `/aura.record` command
2. Implement `/aura.act` command
3. Implement `/aura.transcribe` command
4. Test: record → transcribe → act cycle

### Phase 3: Planning Commands (P2 Stories)

1. Implement `/aura.epic` command
2. Implement `/aura.feature` command
3. Implement `/aura.tickets` command
4. Test: description → epic → tickets

### Phase 4: Beads Integration (P2 Stories)

1. Implement `/beads.status` command
2. Implement `/beads.ready` command
3. Implement `/beads.start` command
4. Implement `/beads.done` command
5. Test: full task lifecycle

### Phase 5: Execution & Validation (P3 Stories)

1. Implement `/aura.implement` command
2. Implement `/aura.prime` command
3. Create tron test fixture
4. Create sample transcript
5. Test: end-to-end workflow validation

## Next Steps

Run `/speckit.tasks` to break this plan into executable tasks with dependencies.
