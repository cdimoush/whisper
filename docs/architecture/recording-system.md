# Recording System Architecture

## System Overview

The Whisper Voice Memo Tool implements a **standalone + Claude integration** architecture that enables voice recording and transcription through two independent, complementary paths that converge on a unified processing pipeline.

This design philosophy prioritizes flexibility and user control: users can record voice memos via system-wide hotkey (works everywhere, no Claude dependency), via Claude commands (convenient during Claude sessions), or both. All recordings flow through the same queue-based processing system for consistent, parallel transcription and organization.

### High-Level Architecture Diagram

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

## Recording Capture Layer

The Recording Capture Layer provides two independent mechanisms for capturing voice memos. Both paths produce audio files in the `queue/` directory with auto-generated timestamps, ready for processing by the unified queue pipeline.

### System-Wide Hotkey Recording

**Path**: `scripts/record_memo.sh`

The standalone hotkey approach provides always-available voice capture:

- **Platform Agnostic**: Uses `sox` (Sound eXchange) for cross-platform audio recording compatibility
- **Independence**: Works everywhere—terminal, IDE, browser, system tray—without requiring Claude to be running
- **Zero Configuration After Setup**: Once hotkey is configured at the OS level (one-time setup per machine), recording is instant
- **Audio Format**: Records directly to `.m4a` format using AAC codec for quality and file size balance
- **Filename Convention**: Auto-generates timestamps like `2025-01-08_14-30-45.m4a`

The hotkey script handles:
1. Detecting audio capture device availability
2. Starting recording and providing user feedback (visual/audio cue)
3. Stopping on hotkey release or timeout
4. Saving to `queue/` directory with timestamped filename
5. Error handling for missing dependencies (sox)

### Claude Command Recording

**Path**: `.claude/commands/record_memo.md`

The Claude integration path provides in-session convenience:

- **Session Context**: Available as `/record_memo` slash command during Claude conversations
- **User Comfort**: Familiar Claude command interface for users already in a Claude session
- **Same Output**: Produces identical `.m4a` files in `queue/` directory
- **Simple Workflow**: `/record_memo` → record → save to queue
- **Optional**: Users can ignore this entirely and use hotkey exclusively

### Unified Output

Both paths produce files in `queue/` with identical structure:
- Location: `queue/YYYY-MM-DD_HH-MM-SS.m4a`
- Naming: Timestamp ensures unique filenames and chronological ordering
- Format: `.m4a` (AAC audio codec) for quality and compatibility

## Queue Processing Layer

The Queue Processing Layer implements a centralized, scalable pipeline for handling all recorded audio. It runs on-demand via the `/process_queue` command and handles discovery, processing, and organization of all recordings.

### Processing Workflow

1. **Discovery**: Scans `queue/` directory for all audio files
2. **Parallel Processing**: Spawns parallel sub-agents (via Claude Tasks) to handle multiple files simultaneously
3. **Transcription**: Each file is transcribed via OpenAI Whisper API using `scripts/transcribe.py`
4. **Title Generation**: Intelligent titles generated from transcription content (e.g., "Project Planning Discussion", "Grocery List")
5. **Archive**: Original audio files moved to `archive/` for reference
6. **Output**: Results written to `output/TITLE_YYYY-MM-DD_HH-MM-SS/` directory structure

### Key Properties

**Parallelization**: Multiple sub-agents run simultaneously via Claude's Task API, enabling efficient processing of batches. Instead of transcribing files sequentially (which could take minutes), parallel processing completes in seconds.

**Intelligent Titling**: Rather than storing results under generic "memo_001", titles are extracted from transcription content, making results immediately useful and searchable.

**Artifact Preservation**: Original audio files remain in `archive/` (not deleted) for reference, legal compliance, or re-processing with different parameters.

**Crash-Safe**: If processing fails, files remain in queue/ or archive/, never lost.

## Directory Structure

The three-directory system creates clear separation of concerns and enables efficient workflow:

```
whisper_zip/
├── queue/
│   ├── 2025-01-08_14-30-45.m4a
│   ├── 2025-01-08_14-31-22.m4a
│   └── 2025-01-08_14-32-00.m4a
│
├── archive/
│   ├── 2025-01-08_14-30-45.m4a
│   ├── 2025-01-08_14-31-22.m4a
│   └── 2025-01-08_14-32-00.m4a
│
└── output/
    ├── Project Planning Discussion_2025-01-08_14-30-45/
    │   ├── transcript.md
    │   └── metadata.json
    ├── Grocery List_2025-01-08_14-31-22/
    │   ├── transcript.md
    │   └── metadata.json
    └── Meeting Notes_2025-01-08_14-32-00/
        ├── transcript.md
        └── metadata.json
```

### `queue/` Directory

**Purpose**: Staging area for unprocessed audio files

- Contains raw `.m4a` files from both hotkey and Claude command recording
- Files wait here until `/process_queue` is invoked
- Any `.m4a` file in this directory will be processed
- Enables batching: users can record multiple memos and process them all at once

### `archive/` Directory

**Purpose**: Persistent storage of processed audio files

- Contains every audio file that has been processed
- Provides reference material for validation or re-processing
- Enables legal/compliance storage if needed
- Can be periodically archived to external storage
- Not deleted automatically (user retains full control)

### `output/` Directory

**Purpose**: Final transcription results and metadata

- Directory structure: `TITLE_YYYY-MM-DD_HH-MM-SS/`
- Title is generated from transcription content for human readability
- Timestamp ensures uniqueness even if titles duplicate
- Contains:
  - `transcript.md`: The full transcription in Markdown format
  - `metadata.json`: Timestamp, audio filename, Whisper model used, processing duration
  - Future: Additional files for summaries, extracted tasks, embeddings, etc.

## Technology Choices

### sox (Sound eXchange)

**For**: Audio recording in standalone hotkey script

**Why**:
- Cross-platform: Works on macOS, Linux, Windows (via WSL)
- Mature and stable: 30+ years of development
- Lightweight: Minimal dependencies
- Direct `.m4a` output: No intermediate file conversion needed
- Battle-tested: Used in production by major projects

**Alternatives Considered**: ALSA (Linux-only), Core Audio APIs (macOS-specific), Web Audio API (browser-only—doesn't solve hotkey requirement)

### OpenAI Whisper API

**For**: Audio transcription

**Why**:
- Accuracy: Production-grade speech recognition
- Language Support: 99 languages with automatic detection
- No GPU Required: API-based, works on any machine
- Existing Integration: Already used in `scripts/transcribe.py`
- Cost-Effective: $0.02/min (comparable to self-hosted models)
- Reliability: Managed service, no infrastructure concerns

**Note**: Document specifies migration path to local Whisper models (see Future Considerations) for privacy-sensitive use cases.

### Python Queue Processor

**For**: `/process_queue` command implementation

**Why**:
- Natural Integration: Whisper transcription already uses Python (`scripts/transcribe.py`)
- Parallel Processing: Easy to spawn sub-agents via Claude Tasks API
- File Operations: Built-in `pathlib`, `json`, `subprocess` modules
- Cross-Platform: No shell script portability concerns
- Development Speed: Rapid iteration on queue logic

### Bash Script for Recording

**For**: `scripts/record_memo.sh` hotkey integration

**Why**:
- System Integration: Hotkeys are configured at OS level via `.plist` (macOS) or `.desktop` (Linux)
- Simplicity: No Python runtime overhead for recording
- Portability: Bash runs everywhere
- User Feedback: Easy to add visual/audio cues during recording

## Trade-offs & Rationale

### Advantages of Standalone + Claude Integration Approach

**✅ System-wide hotkey works independently**
- Recording doesn't depend on Claude being open
- Users can capture ideas anywhere, anytime
- Solves the "rapid idea capture" use case that started this project

**✅ Claude integration provides session convenience**
- For users already in a Claude conversation, in-session recording is frictionless
- No need to switch context; record and continue chatting
- Optional enhancement, not required for functionality

**✅ Shared queue benefits both paths equally**
- One processing pipeline, two recording methods
- Users can mix hotkey + Claude commands for the same batch
- Consistent transcription quality and output format

**✅ Maximum user flexibility**
- Use hotkey exclusively (never touch Claude commands)
- Use Claude commands exclusively (for collaboration sessions)
- Use both (best of both worlds)
- User chooses their workflow, not vice versa

**✅ Queue-based processing enables batching**
- Record many memos, process once
- Parallel processing via sub-agents scales naturally
- Users don't wait for each memo to complete

### Trade-offs

**❌ Requires one-time platform-specific hotkey setup**
- macOS: Create `.plist` and add to System Preferences → Keyboard → Shortcuts
- Linux: Register `.desktop` file in appropriate location
- Not zero-config like a Claude-only approach
- Acceptable trade-off for independence and ubiquity

**❌ sox must be installed separately**
- Not pure Python; adds external dependency
- Most users have `sox` or can install via `brew`/`apt`
- Pure-Python alternatives exist but are less mature
- Acceptable trade-off for quality and cross-platform support

**❌ Processing only on-demand**
- Files don't auto-process when dropped in queue
- Requires explicit `/process_queue` invocation
- Could be addressed with file watcher or cron job (see Future Considerations)
- Deliberate choice to give users explicit control

## Alternative Approaches Considered

### Claude-Only Recording (Rejected)

**Approach**: Provide only `/record_memo` command, no hotkey

**Advantages**:
- Simpler implementation
- Zero platform-specific configuration
- Less dependency management

**Why Rejected**:
- Doesn't solve the original problem: users want to capture ideas anywhere, not just in Claude
- Claude sessions are ephemeral; users won't always have Claude open
- Creates dependency: recording functionality tied to another service
- Misses the core value proposition of rapid, ubiquitous capture

### Commercial Tool Integration (Wispr Flow, etc.)

**Approach**: Partner with existing commercial voice-to-text apps

**Advantages**:
- Proven UX/UI
- Already handles hotkeys, mobile sync, etc.
- No implementation work

**Why Rejected**:
- Violates "DIY control" principle
- Vendor lock-in: user data stored in their system
- Cost: $10-20/month for all users
- Integration complexity and API limitations
- Our goal is to build this capability, not outsource it

### Python-Based Recording (Rejected)

**Approach**: Use `pyaudio`, `sounddevice`, or similar to record in pure Python

**Advantages**:
- Single-language stack
- No external `sox` dependency
- Cross-platform in theory

**Why Rejected**:
- Audio device access is OS-specific (pyaudio uses PortAudio, which adds complexity)
- Less mature than `sox` for production use
- Higher dependency overhead
- Harder to debug audio issues
- Bash wrapper around `sox` is simpler and more reliable

## Future Considerations

This architecture is designed with extensibility in mind. The following enhancements are planned for future phases:

### Automatic Queue Processing

**Problem**: Currently requires explicit `/process_queue` command

**Solution Options**:
- **File Watcher**: Monitor `queue/` directory for new files, auto-trigger processing
- **Scheduled Cron Job**: Process queue every N minutes
- **Real-time Processing**: Transcribe files as soon as they land in queue/

**Trade-off**: Auto-processing reduces user control. Optional configuration allows users to choose.

### Real-Time Transcription Streaming

**Current**: Batch mode—record entire memo, then transcribe

**Future**: Stream audio to Whisper API while recording, see transcript appear in real-time

**Benefit**: Immediate feedback on recording quality, auto-stop when enough content captured

**Implementation**: Whisper API supports streaming; requires new integration point in recording script

### Local Whisper Models for Privacy

**Current**: All transcription goes to OpenAI API

**Future**: Option to run Whisper models locally (`openai-whisper` package, ~1GB)

**Benefit**: No audio data leaves machine; works offline

**Trade-off**: Requires GPU for reasonable speed; API-based is faster

**Implementation**: Add configuration option to switch between API and local models

### Mobile Integration

**Future**: iOS/Android apps that save recordings to synced `queue/` directory

**Mechanism**:
- Cloud storage (Dropbox, iCloud) syncs files to queue/
- Or mobile client directly writes to queue/ via network share
- Same pipeline processes mobile recordings

**Benefit**: Capture ideas on phone, transcribe on desktop

### Voice Command Detection & Auto-Tagging

**Future**: Detect voice commands embedded in recordings and auto-tag

**Example**: "Note: shopping list" → auto-tag as "shopping list"

**Mechanism**: Run specialized model on transcription to extract commands

**Benefit**: Richer metadata, better organization, potential for automation triggers

---

**Document Version**: 1.0
**Last Updated**: 2025-01-08
**Status**: Reference Architecture for Phase 1 & Phase 2 Implementation
