# Epic: Aura Incubation (Option C)

## Epic Overview

Aura is a portable agentic workflow layer that wraps codebases with voice-driven development capabilities. Rather than building Aura as a separate project from scratch, we'll incubate it inside the existing whisper repository—leveraging working code and battle-tested commands.

The incubation approach is pragmatic: create an `aura/` directory inside whisper, build the minimal init CLI and templates there, then validate by testing against a real fixture (tron light bike game). Once validated, Aura can be extracted to its own repository.

The key innovation in this epic is the **test-driven validation using Beads**: we'll use Aura's own workflow (voice → epic → tickets → implement) to build a feature for tron, proving the system works end-to-end. Git branching keeps test implementation isolated from Aura development.

## Vision Context

**Source Vision**: Option C from Aura planning discussion (not a formal vision doc)

### Key Vision Points

**Current Pain Points Addressed:**
- Whisper has grown complex with speckit, beads, brain system, custom commands
- Need a clean, portable layer that can be installed in any codebase
- Current commands work but aren't namespaced or portable

**Vision Goals:**
1. Portable `aura init` command that scaffolds any codebase
2. Namespaced commands (aura.*, beads.*) that don't conflict with existing commands
3. Validated workflow from voice memo → implementation
4. Clean extraction path to standalone repository

**Architecture Decision:**
- Incubate inside whisper (Option C) rather than new repo (slower) or rename-in-place (messy)
- Minimal Python CLI (~15 lines) + copied template files
- Thin wrappers around beads CLI, not reimplementation

## Git Branching Strategy

```
main
  └── 001-aura-workflow-layer (current spec work)
        └── aura-incubation (this epic's development)
              └── aura-tron-test (isolated test implementation)
```

**Branch Rules:**
- `aura-incubation`: All Aura development happens here
- `aura-tron-test`: Branched from aura-incubation for testing
- Test implementation (building tron features) stays in test branch
- Only Aura code (not tron features) merges back to aura-incubation
- When Aura is validated, aura-incubation merges to 001-aura-workflow-layer

## Specs in This Epic

### Phase 1: Aura Core
- [ ] [Chore: Project Structure](./chore-project-structure.md) - Create aura/ directory and pyproject.toml
- [ ] [Feature: Init Command](./feature-init-command.md) - Implement `aura init` CLI

### Phase 2: Command Templates
- [ ] [Chore: Voice Commands](./chore-voice-commands.md) - Create aura.record, aura.act, aura.transcribe templates
- [ ] [Chore: Planning Commands](./chore-planning-commands.md) - Create aura.epic, aura.feature, aura.tickets templates
- [ ] [Chore: Beads Commands](./chore-beads-commands.md) - Create beads.status, beads.ready, beads.start, beads.done templates
- [ ] [Chore: Execution Commands](./chore-execution-commands.md) - Create aura.implement, aura.prime templates

### Phase 3: Test Fixture Setup
- [ ] [Chore: Tron Fixture](./chore-tron-fixture.md) - Create minimal tron game structure
- [ ] [Feature: Sample Workflow](./feature-sample-workflow.md) - Define the test scenario and expected outputs

### Phase 4: End-to-End Validation
- [ ] [Feature: Beads Test Workflow](./feature-beads-test-workflow.md) - Full aura workflow test using beads

## Execution Order

### Phase 1: Aura Core (~30 minutes)
**Goal**: Working `aura init` command that copies templates to target directory

**Git**: Work on `aura-incubation` branch

Execute in order:
1. [Chore: Project Structure](./chore-project-structure.md) - Need directory structure before CLI
2. [Feature: Init Command](./feature-init-command.md) - Core functionality depends on structure

**Success Criteria**:
- `python -m aura.cli init --help` shows usage
- `python -m aura.cli init --dry-run` shows what would be created
- Running in empty test dir creates .aura/, .claude/commands/

**🔄 USER BREAKPOINT #1**: Verify `aura init` works in a scratch directory before proceeding

---

### Phase 2: Command Templates (~45 minutes)
**Goal**: All 12 aura.* and beads.* command templates exist and are copied by init

**Git**: Continue on `aura-incubation` branch

Execute in order (can parallelize within groups):
1. [Chore: Voice Commands](./chore-voice-commands.md) - Core input mechanism
2. [Chore: Planning Commands](./chore-planning-commands.md) - Depends on voice for context
3. [Chore: Beads Commands](./chore-beads-commands.md) - Independent, can parallel with planning
4. [Chore: Execution Commands](./chore-execution-commands.md) - Depends on planning + beads

**Success Criteria**:
- `aura init` copies all 12 command files
- Each command has valid markdown structure
- Commands reference correct paths (.aura/queue/, etc.)

**🔄 USER BREAKPOINT #2**: Run `aura init` and manually test one command (e.g., /aura.prime) works

---

### Phase 3: Test Fixture Setup (~20 minutes)
**Goal**: Tron fixture ready for aura workflow testing

**Git**: Continue on `aura-incubation` branch

Execute in order:
1. [Chore: Tron Fixture](./chore-tron-fixture.md) - Create game stub
2. [Feature: Sample Workflow](./feature-sample-workflow.md) - Define what we'll test

**Success Criteria**:
- `aura/tests/tron/` directory exists with README.md, pyproject.toml
- Sample voice transcript defined (written text simulating voice request)
- Expected epic/ticket output documented

**🔄 USER BREAKPOINT #3**: Review sample workflow definition before executing test

---

### Phase 4: End-to-End Validation (~45 minutes)
**Goal**: Prove aura works by using it to build a tron feature with beads tracking

**Git**:
1. Create `aura-tron-test` branch from `aura-incubation`
2. All test implementation stays in this branch
3. Validation results documented, then branch can be deleted or archived

Execute in order:
1. [Feature: Beads Test Workflow](./feature-beads-test-workflow.md) - Full workflow execution

**The Test Workflow (in detail):**

```
Step 1: Initialize Aura in Tron
─────────────────────────────────
cd aura/tests/tron
python -m aura.cli init
# Verify: .aura/, .claude/commands/ created

Step 2: Create Epic from Sample Transcript
─────────────────────────────────────────
# Using Claude Code in tron directory:
/aura.epic Add player movement - arrow keys control light bike, leaves trail

# Verify: specs/epic-player-movement/README.md created

Step 3: Convert Epic to Beads Tickets
─────────────────────────────────────
/aura.tickets specs/epic-player-movement/

# Verify: bd list shows tasks created
# Verify: Tasks have proper dependencies

Step 4: Work Through Tickets with Beads
───────────────────────────────────────
/beads.status          # See overview
/beads.ready           # See first available task
/beads.start <id>      # Start working
/aura.implement <id>   # Implement the ticket
/beads.done <id>       # Mark complete

# Repeat for 2-3 tickets to validate flow

Step 5: Validate Results
────────────────────────
- Tron has new files/changes from implementation
- Beads shows task progression
- Workflow is smooth and commands work together
```

**Success Criteria**:
- Aura init works in tron directory
- Epic created from written "transcript"
- Tickets created in beads with dependencies
- At least 2 tickets implemented using aura.implement
- Full workflow documented with screenshots/output

**🔄 USER BREAKPOINT #4**: Decide if Aura is ready for extraction to own repo

---

## Path Dependencies Diagram

```
Phase 1: Aura Core
├── chore-project-structure
└── feature-init-command (depends on structure)
    ↓
Phase 2: Command Templates
├── chore-voice-commands ──────────┐
├── chore-planning-commands ───────┼─ All can parallel after init works
├── chore-beads-commands ──────────┤
└── chore-execution-commands ──────┘
    ↓
Phase 3: Test Fixture Setup
├── chore-tron-fixture
└── feature-sample-workflow
    ↓
Phase 4: End-to-End Validation
└── feature-beads-test-workflow
    ↓
[Extract to own repo - future epic]

Critical Path:
project-structure → init-command → voice-commands → tron-fixture → beads-test-workflow
```

## Implementation Notes

### Cross-Cutting Concerns

**Architecture Decisions:**
- Aura lives in `aura/` subdirectory of whisper during incubation
- Templates are copied, not symlinked (portable)
- Beads commands are thin wrappers around `bd` CLI
- No new dependencies beyond click (already in whisper)

**Shared Dependencies:**
- click (CLI framework)
- openai (transcription - already in whisper)
- shutil/pathlib (file operations - stdlib)
- beads (`bd` CLI) - external, optional

**Testing Strategy:**
- Unit test: `aura init` in tmp directory
- Integration test: Full workflow on tron fixture
- Validation: Human review of generated epic/tickets/implementation

**Rollout Plan:**
1. Complete incubation in whisper
2. Validate with tron test
3. Extract to `github.com/username/aura` repository
4. Update README with installation instructions
5. Deprecate whisper's individual commands in favor of aura namespace

### Git Workflow Details

**Development (aura-incubation branch):**
```bash
# Start from current spec branch
git checkout 001-aura-workflow-layer
git checkout -b aura-incubation

# All aura development happens here
# Commits: "aura: add init command", "aura: add voice templates", etc.
```

**Testing (aura-tron-test branch):**
```bash
# Branch for test implementation
git checkout aura-incubation
git checkout -b aura-tron-test

# Test workflow here - commits like:
# "tron: init aura"
# "tron: create player movement epic"
# "tron: implement movement ticket"

# These commits are TEST ARTIFACTS, not aura code
# Branch can be deleted after validation
```

**Merging Back:**
```bash
# Only aura code merges back, NOT tron implementation
git checkout aura-incubation
# No merge from aura-tron-test (it's a test, not code)

# When ready to finalize:
git checkout 001-aura-workflow-layer
git merge aura-incubation
```

### User Testing Breakpoints

This epic includes **4 explicit user testing breakpoints** (marked with 🔄):

1. **After Phase 1**: Verify `aura init` works in scratch directory
2. **After Phase 2**: Test one command manually (/aura.prime)
3. **After Phase 3**: Review sample workflow before executing
4. **After Phase 4**: Decide if ready for extraction

Each breakpoint is a decision point: proceed to next phase, iterate on current phase, or stop if goals are met.

## Success Metrics

- [ ] `aura init` successfully scaffolds .aura/, .claude/commands/ in any directory
- [ ] All 12 command templates work (aura.* and beads.*)
- [ ] Tron test completes full workflow: init → epic → tickets → implement
- [ ] At least 2 beads tickets created and completed using aura commands
- [ ] Workflow is documented with enough detail for another developer to repeat

## Future Enhancements

Ideas that came up during planning but are out of scope for this epic:

1. **Extract to own repo**: After validation, move aura/ to github.com/username/aura
2. **uv tool install support**: Configure pyproject.toml for global installation
3. **Brain system integration**: Port whisper's brain/ concept to aura
4. **Audio recording**: Currently templates only; actual recording needs sox integration
5. **Transcription porting**: Copy whisper's transcribe.py into aura
6. **CI/CD**: GitHub Actions for testing aura init
7. **Multiple AI agent support**: Templates for cursor, copilot, etc. (like speckit)

## Beads Integration for This Epic

Before starting implementation, convert this epic to beads tasks:

```bash
# In whisper root, on aura-incubation branch
bd init  # If not already initialized
/beads-from-epic specs/epic-aura-incubation
```

This creates tasks for each spec with proper dependencies, enabling:
- `/beads.status` to track epic progress
- `/beads.ready` to see next available work
- Parallel work on independent specs
