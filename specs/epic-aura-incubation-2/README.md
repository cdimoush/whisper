# Epic: Aura Incubation Phase 2 - Scripts & Polish

## Epic Overview

The first incubation phase built the scaffolding: `aura init` CLI and 12 command templates. But the commands reference functionality that doesn't exist in wrapped repos - specifically the transcription scripts that make `/aura.act` and `/aura.transcribe` actually work.

This phase completes the extraction by:
1. Creating `.aura/scripts/` with Python scripts copied during init
2. Updating command templates to reference `.aura/scripts/`
3. Adding essential documentation (README.md, CLAUDE.md)
4. Preparing for standalone repo extraction

After this phase, Aura will be fully functional and ready to move to its own repository.

## Gap Analysis

### What Was Built (Phase 1)
- `aura init` CLI command
- 12 command templates (aura.*, beads.*)
- Tron test fixture
- Basic project structure

### What's Missing (This Phase)

| Gap | Impact | Solution |
|-----|--------|----------|
| No transcription scripts | `/aura.act` and `/aura.transcribe` can't work | Add `.aura/scripts/transcribe.py` |
| No title generation | Output directories have generic names | Add `.aura/scripts/generate_title.py` |
| Commands point to wrong paths | Templates reference whisper paths | Update templates to use `.aura/scripts/` |
| No README.md | Users don't know how to use aura | Create comprehensive README |
| No CLAUDE.md | Agents lack context for aura development | Create CLAUDE.md |
| No .env.example | Users don't know required env vars | Create .env.example |

### Whisper Scripts to Port

```
whisper/scripts/
├── transcribe.py      → .aura/scripts/transcribe.py
├── generate_title.py  → .aura/scripts/generate_title.py
└── queue_status.py    → .aura/scripts/queue_status.py (optional)
```

## New Directory Structure

After `aura init`, target repos will have:

```
.aura/
├── config.md              # Aura configuration
├── queue/                 # Audio queue (gitignored)
├── output/                # Processed output (gitignored)
└── scripts/               # NEW: Portable Python scripts
    ├── transcribe.py      # OpenAI Whisper transcription
    ├── generate_title.py  # Intelligent title generation
    └── requirements.txt   # Script dependencies

.beads/                    # Task tracking

.claude/commands/
├── aura.*.md              # Updated to reference .aura/scripts/
└── beads.*.md
```

## Specs in This Epic

### Phase 1: Scripts Extraction
- [ ] [Chore: Scripts Directory](./chore-scripts-directory.md) - Create .aura/scripts/ structure
- [ ] [Feature: Transcription Script](./feature-transcription-script.md) - Port transcribe.py with adaptations
- [ ] [Feature: Title Generation](./feature-title-generation.md) - Port generate_title.py

### Phase 2: Template Updates
- [ ] [Chore: Update Voice Commands](./chore-update-voice-commands.md) - Fix aura.act, aura.transcribe, aura.record paths
- [ ] [Chore: Update Planning Commands](./chore-update-planning-commands.md) - Fix output directory references

### Phase 3: Documentation
- [ ] [Chore: Aura README](./chore-aura-readme.md) - Create comprehensive README.md
- [ ] [Chore: Aura CLAUDE.md](./chore-aura-claude.md) - Create agent instructions
- [ ] [Chore: Environment Setup](./chore-env-setup.md) - Create .env.example and setup docs

### Phase 4: Extraction Prep
- [ ] [Chore: Repo Extraction](./chore-repo-extraction.md) - Prepare for move to standalone repo

## Execution Order

### Phase 1: Scripts Extraction (~45 minutes)
**Goal**: `.aura/scripts/` with working transcription

Execute in order:
1. [Chore: Scripts Directory](./chore-scripts-directory.md) - Create structure
2. [Feature: Transcription Script](./feature-transcription-script.md) - Core functionality
3. [Feature: Title Generation](./feature-title-generation.md) - Supporting functionality

**Success Criteria**:
- `aura init` creates `.aura/scripts/` with all scripts
- `python .aura/scripts/transcribe.py audio.m4a` works
- `python .aura/scripts/generate_title.py "text"` works

**🔄 USER BREAKPOINT #1**: Verify scripts work standalone

---

### Phase 2: Template Updates (~30 minutes)
**Goal**: Commands reference `.aura/scripts/` correctly

Execute in order:
1. [Chore: Update Voice Commands](./chore-update-voice-commands.md)
2. [Chore: Update Planning Commands](./chore-update-planning-commands.md)

**Success Criteria**:
- `/aura.transcribe` calls `.aura/scripts/transcribe.py`
- `/aura.act` uses correct output paths
- All templates are self-contained (no whisper references)

**🔄 USER BREAKPOINT #2**: Test `/aura.transcribe` with real audio

---

### Phase 3: Documentation (~30 minutes)
**Goal**: Aura is documented for users and agents

Execute in parallel:
1. [Chore: Aura README](./chore-aura-readme.md)
2. [Chore: Aura CLAUDE.md](./chore-aura-claude.md)
3. [Chore: Environment Setup](./chore-env-setup.md)

**Success Criteria**:
- README explains installation and usage
- CLAUDE.md provides agent context
- .env.example lists required variables

**🔄 USER BREAKPOINT #3**: Review documentation for completeness

---

### Phase 4: Extraction Prep (~15 minutes)
**Goal**: Aura ready to move to own repository

Execute:
1. [Chore: Repo Extraction](./chore-repo-extraction.md)

**Success Criteria**:
- All whisper-specific references removed
- pyproject.toml ready for `uv tool install`
- Clear instructions for extraction

**🔄 USER BREAKPOINT #4**: Decide to extract or continue incubating

---

## Path Dependencies Diagram

```
Phase 1: Scripts
├── chore-scripts-directory ────┐
│                               ├──► feature-transcription-script
└───────────────────────────────┴──► feature-title-generation
                                          │
                                          ▼
Phase 2: Template Updates
├── chore-update-voice-commands
└── chore-update-planning-commands
        │
        ▼
Phase 3: Documentation (parallel)
├── chore-aura-readme
├── chore-aura-claude
└── chore-env-setup
        │
        ▼
Phase 4: Extraction
└── chore-repo-extraction

Critical Path:
scripts-directory → transcription-script → update-voice-commands → README
```

## Implementation Notes

### Script Portability

Scripts in `.aura/scripts/` must be:
- **Self-contained**: No imports from whisper or aura package
- **Dependency-documented**: requirements.txt lists what's needed
- **Path-agnostic**: Work from any directory when called with full paths

### Template Updates Pattern

Commands should call scripts like:
```bash
python .aura/scripts/transcribe.py "$AUDIO_PATH"
```

Not like:
```bash
python scripts/transcribe.py "$AUDIO_PATH"  # whisper path
python -m aura.transcribe "$AUDIO_PATH"     # package import
```

### Dependencies

Scripts require (documented in `.aura/scripts/requirements.txt`):
```
openai>=1.0
pydub>=0.25
python-dotenv>=1.0
```

Users install with:
```bash
pip install -r .aura/scripts/requirements.txt
# or
uv pip install -r .aura/scripts/requirements.txt
```

## Success Metrics

- [ ] `aura init` creates complete `.aura/scripts/` directory
- [ ] `/aura.transcribe` works end-to-end with real audio
- [ ] `/aura.act` creates properly-named output directories
- [ ] README.md is comprehensive enough for new users
- [ ] CLAUDE.md enables agents to work on aura
- [ ] No references to whisper remain in aura codebase
- [ ] Aura can be `cp -r` to new repo and work immediately

## Future Work (After Extraction)

1. **uv tool install**: Configure for global installation
2. **CI/CD**: GitHub Actions for testing
3. **Brain system**: Port whisper's brain/ concept (optional)
4. **Multiple agents**: Support for cursor, copilot, etc.
5. **Plugin system**: Allow custom commands beyond defaults

## Relation to Original Specs

This epic addresses gaps from:
- `specs/001-aura-workflow-layer/spec.md` - FR-007 through FR-010 (voice input)
- `specs/001-aura-workflow-layer/data-model.md` - AudioMemo, Transcription entities
- `specs/epic-aura-incubation/` - Transcription code not actually ported

The original spec said "port transcription code from whisper" but only the command templates were created, not the underlying scripts.
