# Research: Aura - Agentic Workflow Layer

**Date**: 2026-01-18
**Branch**: `001-aura-workflow-layer`

## Research Questions Resolved

### Q1: How should Aura be installed?

**Decision**: Dual installation support
- `uv tool install aura` for global CLI availability
- `git clone` for local development/customization

**Rationale**:
- `uv tool install` is the modern Python CLI distribution method
- Provides clean `aura` command in PATH without environment activation
- Git clone allows forking and customization

**Implementation Notes**:
- pyproject.toml must define `[project.scripts]` entry point
- Package structure: `src/aura/` layout

### Q2: How should Beads integration work?

**Decision**: Thin wrapper commands that shell out to `bd` CLI

**Rationale**:
- Beads is a separate, maintained tool
- No need to duplicate functionality
- Easy to update beads independently
- `/beads.status` simply runs `bd list` with formatting

**Implementation Notes**:
- Commands check for `bd` availability first
- Graceful error if beads not installed
- Consider: should `aura init` also run `bd init`?

### Q3: How should transcription work?

**Decision**: Port whisper's transcription code directly into aura

**Rationale**:
- Already battle-tested in whisper project
- Handles audio chunking for long files
- Uses OpenAI's whisper API
- No additional dependency to install

**Implementation Notes**:
- Copy `src/whisper/transcribe.py` logic
- Keep same chunking behavior (8-minute threshold)
- Support same audio formats (mp3, m4a, wav, webm)

### Q4: What should the command namespace look like?

**Decision**: Two prefixes: `aura.*` and `beads.*`

**Commands**:
| Namespace | Command | Purpose |
|-----------|---------|---------|
| aura. | record | Capture audio to queue |
| aura. | act | Transcribe + execute request |
| aura. | transcribe | Transcription only |
| aura. | epic | Create epic document |
| aura. | feature | Create feature plan |
| aura. | tickets | Convert plan to beads tasks |
| aura. | implement | Execute ticket work |
| aura. | prime | Load project context |
| beads. | status | Show task overview |
| beads. | ready | Show available tasks |
| beads. | start | Begin working on task |
| beads. | done | Complete task |

**Rationale**:
- Clear ownership of commands
- Avoids collision with existing `.claude/commands/` in target repos
- Discoverable via tab completion (`/aura.<tab>`)

### Q5: What should the test fixture (tron) contain?

**Decision**: Minimal Python game stub

**Contents**:
```
tests/tron/
├── README.md           # Game description, rules
├── pyproject.toml      # Minimal Python project
└── src/tron/__init__.py  # Placeholder
```

**Rationale**:
- Just enough to demonstrate aura workflow
- Actual game implementation is out of scope
- README provides context for sample epic/tickets
- Validates full workflow: init → epic → tickets → implement

**Sample Epic for tron**:
"Add player movement - the light bike should respond to arrow keys and leave a trail behind it"

## Dependencies Research

### Required
- `openai` - Whisper API for transcription
- `click` - CLI framework
- `python-dotenv` - Environment variable loading

### Optional
- `sox` - Audio recording (system dependency)
- `beads` (`bd` CLI) - Task management

### Development
- `pytest` - Testing
- `pytest-tmp-files` - Filesystem fixtures

## Alternatives Considered

| Decision | Alternative | Why Rejected |
|----------|-------------|--------------|
| uv tool install | pip install | Less modern, requires venv activation |
| Thin beads wrapper | Direct library import | Tighter coupling, harder updates |
| Port transcription | Whisper as dependency | Extra install step, version conflicts |
| aura.* prefix | No prefix | Collision risk with existing commands |
| Minimal tron stub | Full game | Scope creep, not needed for validation |
