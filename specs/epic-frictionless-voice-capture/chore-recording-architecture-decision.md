# Chore: Document Recording Architecture Decision

## Chore Description

Document the architectural decision for how voice recording integrates with the system. The vision document recommends a **standalone + Claude integration** approach where recording works both as a system-wide hotkey (independent of Claude) and as an optional Claude command for in-session recording.

This chore creates the architecture document that will guide all subsequent implementation decisions in Path 1 (Queue System) and Path 2 (Hotkey Layer). The document clarifies that both recording paths (hotkey and Claude command) feed into the same queue directory and are processed by the same pipeline.

## Relevant Files

Create these files to document the architecture decision:

### New Files
- `docs/architecture/recording-system.md` - Core architecture document explaining the standalone + Claude integration approach, including:
  - System design overview (hotkey → queue → processor → archive)
  - Recording capture mechanisms (sox-based standalone script + Claude `/record_memo` command)
  - Queue processing pipeline architecture
  - Directory structure and data flow
  - Trade-offs and rationale for this approach

## Step by Step Tasks

IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create docs directory structure
- Create `docs/architecture/` directory for architecture documentation
- This becomes the canonical location for architectural decisions

### Step 2: Create recording system architecture document
- Write `docs/architecture/recording-system.md` with the following sections:
  - **System Overview**: High-level diagram of the complete workflow (capture → queue → process → archive)
  - **Recording Capture Layer**: Two independent paths to capture audio
    - System-wide hotkey (via `scripts/record_memo.sh`) - works even when Claude isn't running
    - Claude command (via `/record_memo`) - convenient for in-session voice capture
    - Both save to `queue/` directory with auto-generated filenames
  - **Queue Processing Layer**: How audio files flow through the system
    - Files land in `queue/` directory
    - `/process_queue` command discovers and processes all files
    - Parallel processing via Claude's Task tool (multiple sub-agents)
    - Intelligent title generation for each transcription
    - Processed files move to `archive/`, outputs to `output/`
  - **Directory Structure**: Explain the three-directory system
    - `queue/` - Unprocessed audio files waiting for transcription
    - `archive/` - Processed audio files (preserved for reference)
    - `output/` - Transcription results in `TITLE_YYYY-MM-DD_HH-MM-SS/` directories
  - **Technology Choices**: Document key technical decisions
    - sox for cross-platform audio recording (macOS/Ubuntu compatible)
    - OpenAI Whisper API for transcription (existing `scripts/transcribe.py`)
    - Python for queue processor and title generation
    - Bash script for recording (portable, simple)
  - **Trade-offs & Rationale**: Why this approach over alternatives
    - ✅ System-wide hotkey works independently (no Claude dependency for capture)
    - ✅ Claude integration provides convenience for in-session recording
    - ✅ Shared queue means both paths benefit from same processing pipeline
    - ✅ User has maximum flexibility (use hotkey OR Claude command OR both)
    - ❌ Requires one-time platform-specific hotkey setup (not zero-config)
    - ❌ sox must be installed separately (not pure Python)
  - **Alternative Approaches Considered**:
    - Claude-only recording (rejected: only works when Claude is running)
    - Commercial tool integration like Wispr Flow (rejected: goal is DIY control)
    - Python-based recording (rejected: sox is more mature and cross-platform)

### Step 3: Add architecture diagram
- Create a simple text-based architecture diagram showing:
  ```
  User Input (Voice)
      ↓
  ┌─────────────────────────────────────────┐
  │  Recording Capture Layer                │
  │  ┌──────────────┐   ┌─────────────────┐ │
  │  │ Hotkey       │   │ Claude Command  │ │
  │  │ (anywhere)   │   │ (/record_memo)  │ │
  │  └──────┬───────┘   └────────┬────────┘ │
  └─────────┼──────────────────────┼─────────┘
            └──────────┬───────────┘
                       ↓
              queue/ directory
                  (*.m4a files)
                       ↓
  ┌─────────────────────────────────────────┐
  │  Queue Processing Layer                 │
  │  ┌─────────────────────────────────────┐│
  │  │ /process_queue command              ││
  │  │  - Discovers all audio in queue/    ││
  │  │  - Spawns parallel sub-agents       ││
  │  │  - Transcribes via Whisper API      ││
  │  │  - Generates intelligent titles     ││
  │  │  - Moves to archive/                ││
  │  └─────────────────────────────────────┘│
  └─────────────────────────────────────────┘
                       ↓
         ┌─────────────┴─────────────┐
         ↓                           ↓
    archive/                    output/
  (processed audio)    (TITLE_YYYY-MM-DD_HH-MM-SS/)
  ```

### Step 4: Document future considerations
- Add a "Future Considerations" section covering:
  - Automatic queue processing (file watcher or cron job)
  - Real-time transcription streaming
  - Local Whisper models for privacy-sensitive recordings
  - Mobile integration (iOS/Android apps saving to synced queue/)
  - Voice command detection and auto-tagging

### Step 5: Link architecture doc from main README
- Add a reference to the architecture document in the main README.md
- Create a new "## Architecture" section that links to `docs/architecture/recording-system.md`
- Brief 1-sentence description: "See [Recording System Architecture](docs/architecture/recording-system.md) for design decisions."

## Validation Commands

Execute every command to validate the chore is complete.

```bash
# Verify architecture document exists and has substantial content
cat docs/architecture/recording-system.md
wc -l docs/architecture/recording-system.md  # Should be 150+ lines

# Verify main README links to architecture doc
grep -i "architecture" README.md

# Verify directory structure is created
ls -la docs/architecture/
```

## Notes

- This architecture document serves as the "source of truth" for all implementation work in this epic
- Keep the document concise but comprehensive - it should answer "why this approach?" for future contributors
- The diagram should be simple enough to understand at a glance but detailed enough to show data flow
- This is the foundation for Phase 1 and Phase 2 - get stakeholder buy-in on this document before proceeding to implementation
- Consider this document "living" - update it as implementation reveals new insights or needed adjustments
