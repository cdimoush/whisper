# Tasks: Aura - Agentic Workflow Layer

**Input**: Design documents from `/specs/001-aura-workflow-layer/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: No explicit test tasks requested. Focus on implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US6)
- Include exact file paths in descriptions

## Path Conventions

- **Repository**: `aura/` (new GitHub repo)
- **Source**: `src/aura/`
- **Templates**: `src/aura/templates/`
- **Tests**: `tests/`
- **Fixture**: `tests/tron/`

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create new aura repository and basic structure

- [ ] T001 Create new GitHub repository `aura`
- [ ] T002 Initialize Python project with pyproject.toml (uv, click, openai dependencies)
- [ ] T003 [P] Create src/aura/__init__.py with version
- [ ] T004 [P] Create README.md with project overview
- [ ] T005 [P] Create CLAUDE.md with agent instructions
- [ ] T006 [P] Create .gitignore (Python, audio files, .env)
- [ ] T007 Configure pyproject.toml [project.scripts] entry point for `aura` CLI

**Checkpoint**: `uv sync` works, `aura --version` runs

---

## Phase 2: Foundational (Core CLI Framework)

**Purpose**: CLI structure that all commands depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T008 Create src/aura/cli.py with Click app structure (--version, --help)
- [ ] T009 [P] Create src/aura/templates/ directory structure
- [ ] T010 [P] Create src/aura/templates/aura/ with config.md template
- [ ] T011 [P] Create src/aura/templates/claude/ directory for command templates
- [ ] T012 Port transcription code from whisper to src/aura/transcribe.py
- [ ] T013 Create src/aura/init.py with scaffolding logic skeleton

**Checkpoint**: `aura --help` shows init and check commands

---

## Phase 3: User Story 1 - Initialize Aura in Codebase (Priority: P1) 🎯 MVP

**Goal**: Developer can run `aura init` to scaffold .aura/, .beads/, .claude/commands/

**Independent Test**: Run `aura init` in empty directory, verify all directories and files created

### Implementation for User Story 1

- [ ] T014 [US1] Implement `aura init` command in src/aura/cli.py
- [ ] T015 [US1] Implement directory creation logic in src/aura/init.py (create .aura/, .claude/commands/)
- [ ] T016 [P] [US1] Create src/aura/templates/aura/config.md with default configuration
- [ ] T017 [US1] Implement file copy/template rendering in src/aura/init.py
- [ ] T018 [US1] Implement merge logic for existing .claude/commands/ (don't overwrite)
- [ ] T019 [US1] Implement beads integration (call `bd init` if available)
- [ ] T020 [US1] Implement `aura check` command to verify prerequisites
- [ ] T021 [US1] Add --force, --no-beads, --dry-run flags to init command
- [ ] T022 [US1] Add init output reporting (what was created/skipped)

**Checkpoint**: `aura init` creates full structure, `aura check` reports status

---

## Phase 4: User Story 2 - Voice Memo to Transcription (Priority: P1)

**Goal**: Developer can record audio and transcribe it via /aura.act

**Independent Test**: Record 30-second memo, run /aura.act, verify transcription output

### Implementation for User Story 2

- [ ] T023 [P] [US2] Create src/aura/templates/claude/aura.record.md command template
- [ ] T024 [P] [US2] Create src/aura/templates/claude/aura.transcribe.md command template
- [ ] T025 [P] [US2] Create src/aura/templates/claude/aura.act.md command template
- [ ] T026 [US2] Implement audio chunking logic in src/aura/transcribe.py (for files >8min)
- [ ] T027 [US2] Implement OpenAI whisper API integration in src/aura/transcribe.py
- [ ] T028 [US2] Add audio format validation (mp3, m4a, wav, webm) in src/aura/transcribe.py
- [ ] T029 [US2] Implement queue directory management in aura.record.md template
- [ ] T030 [US2] Implement output directory creation in aura.act.md template

**Checkpoint**: /aura.record saves to .aura/queue/, /aura.act transcribes and creates output

---

## Phase 5: User Story 3 - Epic and Ticket Planning (Priority: P2)

**Goal**: Developer can create epic documents and convert them to beads tickets

**Independent Test**: Run /aura.epic with description, verify epic created in specs/

### Implementation for User Story 3

- [ ] T031 [P] [US3] Create src/aura/templates/claude/aura.epic.md command template
- [ ] T032 [P] [US3] Create src/aura/templates/claude/aura.feature.md command template
- [ ] T033 [P] [US3] Create src/aura/templates/claude/aura.tickets.md command template
- [ ] T034 [US3] Define epic document structure in aura.epic.md (phases, specs, dependencies)
- [ ] T035 [US3] Define feature plan structure in aura.feature.md
- [ ] T036 [US3] Implement beads task creation logic in aura.tickets.md (parse epic, call bd create)

**Checkpoint**: /aura.epic creates structured doc, /aura.tickets creates beads tasks

---

## Phase 6: User Story 4 - Task Execution with Beads (Priority: P2)

**Goal**: Developer can manage tasks through beads.* commands

**Independent Test**: Create tasks manually, cycle through status with beads.* commands

### Implementation for User Story 4

- [ ] T037 [P] [US4] Create src/aura/templates/claude/beads.status.md command template
- [ ] T038 [P] [US4] Create src/aura/templates/claude/beads.ready.md command template
- [ ] T039 [P] [US4] Create src/aura/templates/claude/beads.start.md command template
- [ ] T040 [P] [US4] Create src/aura/templates/claude/beads.done.md command template
- [ ] T041 [US4] Implement bd CLI wrapper logic in beads.status.md (bd list formatting)
- [ ] T042 [US4] Implement task state transitions in beads.start.md and beads.done.md

**Checkpoint**: All beads.* commands work, full task lifecycle functional

---

## Phase 7: User Story 5 - Implementation from Ticket (Priority: P3)

**Goal**: Developer can run /aura.implement to execute work from a ticket

**Independent Test**: Create simple ticket, run /aura.implement, verify work done

### Implementation for User Story 5

- [ ] T043 [P] [US5] Create src/aura/templates/claude/aura.implement.md command template
- [ ] T044 [P] [US5] Create src/aura/templates/claude/aura.prime.md command template
- [ ] T045 [US5] Implement ticket reading logic in aura.implement.md (parse bd show output)
- [ ] T046 [US5] Implement implementation planning in aura.implement.md
- [ ] T047 [US5] Implement project context loading in aura.prime.md

**Checkpoint**: /aura.implement reads ticket and helps execute, /aura.prime loads context

---

## Phase 8: User Story 6 - Test Fixture Validation (Priority: P3)

**Goal**: Tron test fixture validates full workflow end-to-end

**Independent Test**: Clone tron, run aura init, process sample transcript through full workflow

### Implementation for User Story 6

- [ ] T048 [P] [US6] Create tests/tron/README.md with light bike game description
- [ ] T049 [P] [US6] Create tests/tron/pyproject.toml with minimal Python setup
- [ ] T050 [P] [US6] Create tests/tron/src/tron/__init__.py placeholder
- [ ] T051 [P] [US6] Create examples/sample_transcript.txt with example feature request
- [ ] T052 [US6] Create examples/expected_epic.md showing expected epic output
- [ ] T053 [US6] Document validation workflow in tests/tron/README.md

**Checkpoint**: Tron fixture can demonstrate full aura workflow

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and documentation

- [ ] T054 [P] Update README.md with complete installation and usage guide
- [ ] T055 [P] Update CLAUDE.md with all command documentation
- [ ] T056 Add error handling for missing prerequisites in all commands
- [ ] T057 Add --help text to all CLI commands
- [ ] T058 Validate pyproject.toml allows `uv tool install aura`
- [ ] T059 Run full workflow validation with tron fixture

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - MVP target
- **User Story 2 (Phase 4)**: Depends on Foundational, benefits from US1 templates
- **User Stories 3-6**: Depend on Foundational, can proceed in parallel
- **Polish (Phase 9)**: Depends on desired user stories being complete

### User Story Dependencies

| Story | Depends On | Can Parallel With |
|-------|------------|-------------------|
| US1 (Init) | Foundational only | - |
| US2 (Voice) | Foundational only | US1 |
| US3 (Planning) | Foundational only | US1, US2 |
| US4 (Beads) | Foundational only | US1, US2, US3 |
| US5 (Implement) | US3, US4 | - |
| US6 (Fixture) | US1 | US2, US3, US4 |

### Within Each User Story

- Template files marked [P] can be created in parallel
- Logic implementation follows template creation
- Integration tasks come last

### Parallel Opportunities

**Phase 1 (Setup)**:
```
T003, T004, T005, T006 can run in parallel
```

**Phase 2 (Foundational)**:
```
T009, T010, T011 can run in parallel
```

**Phase 4 (US2 Voice)**:
```
T023, T024, T025 can run in parallel (template files)
```

**Phase 6 (US4 Beads)**:
```
T037, T038, T039, T040 can run in parallel (all template files)
```

**Phase 8 (US6 Fixture)**:
```
T048, T049, T050, T051 can run in parallel (independent files)
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Init)
4. **VALIDATE**: `aura init` works in empty directory
5. Complete Phase 4: User Story 2 (Voice)
6. **VALIDATE**: Record → transcribe → act cycle works
7. Deploy/demo MVP

### Incremental Delivery

1. Setup + Foundational → Base CLI ready
2. US1 (Init) → Can scaffold into any codebase
3. US2 (Voice) → Core voice workflow functional
4. US3 (Planning) → Epic/ticket creation
5. US4 (Beads) → Full task management
6. US5 (Implement) → Automated execution
7. US6 (Fixture) → Validation and demo

### Afternoon Sprint Target

Given time constraint, focus on:
1. **Must have**: Setup + Foundational + US1 (Init)
2. **Should have**: US2 (Voice transcription)
3. **Nice to have**: US3-US4 (Planning + Beads)
4. **Defer**: US5-US6 (Implement + Fixture)

---

## Notes

- Total tasks: 59
- Tasks per story: US1=9, US2=8, US3=6, US4=6, US5=5, US6=6
- Parallel opportunities: 22 tasks marked [P]
- MVP scope: Phases 1-4 (Setup through Voice) = 30 tasks
- Template files are the bulk of work - most are copy/adapt from whisper
