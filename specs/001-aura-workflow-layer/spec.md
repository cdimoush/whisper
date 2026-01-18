# Feature Specification: Aura - Agentic Workflow Layer

**Feature Branch**: `001-aura-workflow-layer`
**Created**: 2026-01-18
**Status**: Draft
**Input**: User description: "Aura - An agentic workflow layer that wraps codebases. Install via uv tool or git clone, run aura init to scaffold .aura/, .beads/, .claude/ directories. Prefix commands with aura. and beads. namespaces. Core features: audio recording and transcription (from whisper), epic/ticket planning, beads task integration, implement commands. Includes tron/ test fixture (light bike game) as example codebase. Goal: voice memo to ticket planning to implementation workflow."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Initialize Aura in Existing Codebase (Priority: P1)

A developer has an existing codebase and wants to add agentic workflow capabilities. They clone or install Aura, then run `aura init` in their project root. The system scaffolds the necessary directories and files, making the codebase ready for voice-driven development.

**Why this priority**: This is the entry point for all other functionality. Without initialization, no other features work. Must be rock-solid and fast.

**Independent Test**: Can be fully tested by running `aura init` in an empty directory and verifying the scaffolded structure exists with all required files.

**Acceptance Scenarios**:

1. **Given** a codebase without Aura, **When** user runs `aura init`, **Then** the system creates `.aura/`, `.beads/`, and `.claude/commands/` directories with starter files
2. **Given** a codebase that already has `.claude/` directory, **When** user runs `aura init`, **Then** the system merges Aura commands without overwriting existing commands
3. **Given** a codebase with partial Aura setup, **When** user runs `aura init`, **Then** the system fills in missing components and reports what was added

---

### User Story 2 - Voice Memo to Transcription (Priority: P1)

A developer has an idea or task while away from keyboard. They record a voice memo using `/aura.record`. Later, they run `/aura.act` to transcribe the audio and have an AI agent interpret and execute the request.

**Why this priority**: This is the core input mechanism that enables hands-free workflow. The entire value proposition depends on voice capture working reliably.

**Independent Test**: Can be tested by recording a 30-second memo, running act, and verifying transcription output is accurate and actionable.

**Acceptance Scenarios**:

1. **Given** user is in a terminal, **When** they run `/aura.record`, **Then** audio recording starts and saves to a queue directory
2. **Given** an audio file exists, **When** user runs `/aura.act <file>`, **Then** the system transcribes and interprets the request
3. **Given** a transcribed request, **When** the request is actionable, **Then** the system creates appropriate deliverables (plans, code, docs)

---

### User Story 3 - Epic and Ticket Planning (Priority: P2)

A developer describes a large feature via voice memo. The system transcribes it, creates a high-level epic document, and breaks it down into individual tickets that can be tracked.

**Why this priority**: Planning is essential for larger work, but requires the voice capture (P1) to be working first.

**Independent Test**: Can be tested by providing a written feature description to `/aura.epic` and verifying it produces a structured epic with trackable tickets.

**Acceptance Scenarios**:

1. **Given** a feature description, **When** user runs `/aura.epic`, **Then** the system creates a structured epic document with phases and tickets
2. **Given** an epic document exists, **When** user runs `/aura.tickets`, **Then** the system creates individual tickets in the beads task system
3. **Given** tickets exist in beads, **When** user runs `/beads.status`, **Then** the system shows progress across all tickets

---

### User Story 4 - Task Execution with Beads (Priority: P2)

A developer wants to work through tickets systematically. They use beads commands to see what's ready, pick up work, and mark tasks complete. The system tracks dependencies and progress.

**Why this priority**: Task execution is the "output" side of the workflow. Valuable but requires planning (P2) to have tickets to execute.

**Independent Test**: Can be tested by creating sample tickets manually, then using beads commands to cycle through task states.

**Acceptance Scenarios**:

1. **Given** tickets exist, **When** user runs `/beads.ready`, **Then** the system shows tickets with no blocking dependencies
2. **Given** a ticket is ready, **When** user runs `/beads.start <id>`, **Then** the ticket moves to in_progress state
3. **Given** a ticket is in progress, **When** user runs `/beads.done <id>`, **Then** the ticket moves to closed state and dependents become unblocked

---

### User Story 5 - Implementation from Ticket (Priority: P3)

A developer has a ticket to implement. They run `/aura.implement <ticket-id>` and the system reads the ticket, plans the implementation, and executes the work with AI assistance.

**Why this priority**: This is the automation layer that ties everything together. Requires all prior stories to be working.

**Independent Test**: Can be tested by creating a simple ticket (e.g., "add a README file") and running implement to verify the work is done correctly.

**Acceptance Scenarios**:

1. **Given** a ticket ID, **When** user runs `/aura.implement <id>`, **Then** the system reads the ticket and creates an implementation plan
2. **Given** an implementation plan, **When** the plan is approved, **Then** the system executes the plan and creates/modifies files
3. **Given** implementation is complete, **When** the ticket is done, **Then** the system offers to mark the ticket as closed

---

### User Story 6 - Test Fixture Validation (Priority: P3)

The Aura project includes a test fixture called "tron" (a light bike game). A developer or test agent can use this fixture to validate the full workflow: init → epic → tickets → implement.

**Why this priority**: This is for validation and demonstration purposes. Useful but not core functionality.

**Independent Test**: Can be tested by cloning tron fixture, running aura init, providing a sample transcript, and verifying end-to-end workflow.

**Acceptance Scenarios**:

1. **Given** the tron test fixture, **When** user runs `aura init`, **Then** aura sets up around the existing game code
2. **Given** a written transcript describing a feature, **When** test agent processes it through aura, **Then** the full workflow executes: epic → tickets → implement
3. **Given** implementation is complete, **When** validation runs, **Then** the system confirms expected files were created/modified

---

### Edge Cases

- What happens when user runs `aura init` in a directory that's not a git repo?
- How does the system handle audio files that are too large (>25MB)?
- What happens when transcription fails due to API errors?
- How does the system handle tickets with circular dependencies?
- What happens when user tries to implement a ticket that's already closed?
- How does the system behave when `.claude/` exists but has conflicting command names?

## Requirements *(mandatory)*

### Functional Requirements

**Installation & Initialization**

- **FR-001**: System MUST be installable via `git clone` into any directory
- **FR-002**: System SHOULD be installable via `uv tool install` for global availability
- **FR-003**: System MUST provide an `aura init` command that scaffolds required directories
- **FR-004**: System MUST create `.aura/`, `.beads/`, and `.claude/commands/` during init
- **FR-005**: System MUST preserve existing `.claude/commands/` files during init (merge, not overwrite)
- **FR-006**: System MUST make all scaffolded files committable to the target repository

**Voice Input (aura. namespace)**

- **FR-007**: System MUST provide `/aura.record` command to capture audio
- **FR-008**: System MUST provide `/aura.act` command to transcribe and act on audio
- **FR-009**: System MUST provide `/aura.transcribe` command for transcription-only
- **FR-010**: System MUST support common audio formats (mp3, m4a, wav, webm)

**Planning (aura. namespace)**

- **FR-011**: System MUST provide `/aura.epic` command to create structured epic documents
- **FR-012**: System MUST provide `/aura.feature` command for single-feature planning
- **FR-013**: System MUST provide `/aura.tickets` command to convert plans into beads tasks

**Task Management (beads. namespace)**

- **FR-014**: System MUST provide `/beads.status` command to show project task status
- **FR-015**: System MUST provide `/beads.ready` command to show available tasks
- **FR-016**: System MUST provide `/beads.start` command to begin working on a task
- **FR-017**: System MUST provide `/beads.done` command to mark a task complete

**Execution (aura. namespace)**

- **FR-018**: System MUST provide `/aura.implement` command to execute work from a ticket
- **FR-019**: System MUST provide `/aura.prime` command to load project context

**Test Fixture**

- **FR-020**: System MUST include a `tests/tron/` directory with a minimal game codebase
- **FR-021**: Test fixture MUST include a README describing the game
- **FR-022**: Test fixture MUST be usable as a target for `aura init` demonstration

### Key Entities

- **Audio Memo**: A voice recording captured by the user, stored in queue for processing
- **Transcription**: Text output from processing an audio memo
- **Epic**: A high-level feature document with phases and grouped work items
- **Ticket**: A single unit of work tracked in the beads system, with status and dependencies
- **Task Graph**: The collection of tickets and their dependency relationships in beads

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: User can initialize Aura in a new codebase in under 30 seconds
- **SC-002**: Voice memo from recording to transcription completes in under 60 seconds for memos under 5 minutes
- **SC-003**: 100% of aura.* and beads.* commands are accessible after init
- **SC-004**: Test fixture demonstrates full workflow (init → epic → tickets → implement) with example transcript
- **SC-005**: User can go from voice idea to tracked tickets in under 5 minutes
- **SC-006**: All scaffolded files are git-friendly (no binary blobs, reasonable sizes)

## Assumptions

- User has Claude Code installed and configured
- User has access to OpenAI API for transcription (or alternative transcription service)
- User has `sox` installed for audio recording (or system provides alternative)
- User is working in a Unix-like environment (macOS, Linux)
- Beads CLI (`bd`) is available or will be installed alongside Aura
- Target codebases use git for version control (graceful degradation if not)

## Out of Scope

- Mobile app for voice recording (use system tools + sync)
- Multi-user collaboration features
- Cloud hosting or SaaS deployment
- GUI/web interface
- Windows support (may work but not tested)
- Integration with external project management tools (Jira, Linear, etc.)
