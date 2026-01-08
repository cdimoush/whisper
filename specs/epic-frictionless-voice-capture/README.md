# Epic: Frictionless Voice Capture Workflow

## Epic Overview

Transform the whisper tool from a manual, one-at-a-time audio transcription system into an instant brain-dump workflow. This epic implements the core vision of "vibe coding" efficiency where users can record voice memos from anywhere, have them automatically queued, batch-processed with parallel sub-agents, intelligently titled with memorable names, and organized for easy discovery.

This epic follows a strategic three-phase approach: **Path 3 (Architecture Decision) → Path 1 (Queue System) → Path 2 (Hotkey Capture)**. Each phase includes clear user testing breakpoints to validate assumptions and course-correct before investing in the next phase.

The result: reduce friction from ~2 minutes of manual file management down to ~2 seconds of instant capture, matching the efficiency demonstrated by top AI-assisted developers like Andrej Karpathy.

## Vision Context

**Source Vision**: [Vision: Frictionless Voice Memo Workflow](../vision-frictionless-voice-memo-workflow.md)

### Key Vision Points

**Current Pain Points Addressed:**
- High friction to start recording (must open app, save to disk, get path, run command)
- Sequential processing bottleneck (must point at one audio file at a time)
- Poor discoverability (datetime stamps make it hard to find "that memo about the API refactor")
- No automated intake (audio files don't flow into a processing pipeline)

**Vision Goals:**
1. Instant capture from anywhere with global hotkey (Path 2)
2. Zero-friction intake with automatic queue management (Path 1)
3. Batch processing with parallel sub-agents (Path 1)
4. Intelligent titling for discoverability (Path 1)
5. Auto-archiving of processed audio (Path 1)

**Architecture Decision (Path 3):**
Based on vision research, the recommended approach is **standalone recording with optional Claude integration**:
- Recording hotkey is system-wide and independent of Claude (works even when Claude isn't running)
- Claude can also trigger recording via `/record_memo` command for voice capture during coding sessions
- Both approaches save to the same `queue/` directory, processed by the same pipeline
- Maximum flexibility: brain-dump at any time, or voice-command while actively working with Claude

## Specs in This Epic

### Phase 1: Architecture Decision (Path 3)
- [ ] [Chore: Document Recording Architecture Decision](./chore-recording-architecture-decision.md) - Document the standalone + Claude integration approach

### Phase 1: Foundation (Path 1 - Queue System)
- [ ] [Chore: Setup Queue Directory Structure](./chore-setup-queue-directories.md) - Create queue/, archive/, output/ directories with .gitignore
- [ ] [Feature: Queue Processor with Parallel Sub-agents](./feature-queue-processor.md) - Batch process all audio files in queue/ using Task tool parallelization
- [ ] [Feature: Intelligent Title Generation](./feature-intelligent-titling.md) - Generate memorable human-readable titles for each transcription
- [ ] [Feature: Queue Status Command](./feature-queue-status.md) - View pending audio files and estimated processing time
- [ ] [Chore: Update Documentation for Queue Workflow](./chore-update-docs-queue-workflow.md) - Update README with queue-based workflow instructions

### Phase 2: Instant Capture (Path 2 - Hotkey Layer)
- [ ] [Chore: Install sox Audio Capture Tool](./chore-install-sox.md) - Add sox to dependencies for cross-platform audio recording
- [ ] [Feature: Recording Script with Auto-Queue](./feature-recording-script.md) - Bash script using sox to record and auto-save to queue/
- [ ] [Feature: Claude-Integrated Record Command](./feature-claude-record-command.md) - `/record_memo` slash command to trigger recording from within Claude
- [ ] [Chore: Platform-Specific Hotkey Setup Guides](./chore-hotkey-setup-guides.md) - Document macOS and Ubuntu global hotkey configuration

## Execution Order

### Phase 1A: Architecture Decision (Immediate - 15 minutes)
**Goal**: Document and commit to the standalone + Claude integration architecture before building anything.

Execute in order:
1. [Chore: Document Recording Architecture Decision](./chore-recording-architecture-decision.md) - Creates `docs/architecture/recording-system.md` documenting the standalone approach with optional Claude integration

**Success Criteria**: Architecture document exists and clearly explains the dual-path approach (system hotkey + Claude command)

**🔄 USER BREAKPOINT #1**: Review architecture decision document. Confirm this is the right approach before proceeding to queue system implementation.

---

### Phase 1B: Queue Foundation (1-2 hours)
**Goal**: Build the queue infrastructure that makes batch processing and intelligent titling possible. This phase delivers immediate value even with manual file placement.

Execute in order:
1. [Chore: Setup Queue Directory Structure](./chore-setup-queue-directories.md) - Sets up the three-directory system (queue/, archive/, output/) with clear READMEs and .gitignore entries
2. [Feature: Intelligent Title Generation](./feature-intelligent-titling.md) - Implements LLM-based title generation in a new `scripts/generate_title.py` module (must exist before queue processor can use it)

**Success Criteria**:
- Directories exist with explanatory READMEs
- `generate_title.py` can generate memorable titles from transcription text
- .gitignore prevents committing voice memos

**🔄 USER BREAKPOINT #2**: Test title generation manually with a sample transcription. Verify titles are memorable and useful. If titles are too generic or too verbose, adjust the prompt before integrating into queue processor.

---

### Phase 1C: Queue Processing (1-2 hours)
**Goal**: Implement batch processing with parallel sub-agents and integrate intelligent titling.

Execute in order:
1. [Feature: Queue Processor with Parallel Sub-agents](./feature-queue-processor.md) - Builds `/process_queue` command that uses Task tool to process multiple audio files in parallel
2. [Feature: Queue Status Command](./feature-queue-status.md) - Adds `/queue_status` command to inspect pending files

**Success Criteria**:
- `/process_queue` successfully processes multiple audio files in queue/
- Transcriptions appear in `output/TITLE_YYYY-MM-DD_HH-MM-SS/` directories
- Processed audio moves to `archive/`
- `/queue_status` shows accurate file count and details

**🔄 USER BREAKPOINT #3**: Drop 3-5 audio files into `queue/` and run `/process_queue`. Verify:
- All files are processed (check for errors)
- Titles are useful and memorable
- Output directories are well-organized
- Archived audio files are preserved

This is the most critical breakpoint - if queue processing works well with manual file placement, the system already delivers 10x value over the current workflow.

---

### Phase 1D: Documentation & Polish (30 minutes)
**Goal**: Update documentation so users understand the new queue-based workflow.

Execute in order:
1. [Chore: Update Documentation for Queue Workflow](./chore-update-docs-queue-workflow.md) - Updates main README.md with queue workflow instructions and examples

**Success Criteria**: README clearly explains how to use the queue system for batch processing

**🔄 USER BREAKPOINT #4**: Use the queue system daily for 1-2 weeks. Validate:
- The queue workflow feels natural
- Batch processing saves significant time
- Titles help you find past memos
- You're ready to invest in instant capture (hotkey layer)

If queue system isn't delivering value, hotkeys won't help. Fix queue UX before proceeding to Phase 2.

---

### Phase 2A: Audio Capture Foundation (1 hour)
**Goal**: Set up cross-platform audio recording infrastructure with sox.

Execute in order:
1. [Chore: Install sox Audio Capture Tool](./chore-install-sox.md) - Adds sox to dependencies and documents installation for macOS/Ubuntu
2. [Feature: Recording Script with Auto-Queue](./feature-recording-script.md) - Creates `scripts/record_memo.sh` that records audio and auto-saves to queue/

**Success Criteria**:
- sox is installed and documented
- `scripts/record_memo.sh` can record audio from terminal
- Recorded audio automatically appears in `queue/`

**🔄 USER BREAKPOINT #5**: Test recording from terminal:
```bash
./scripts/record_memo.sh
# [speak for 10 seconds]
# [press Ctrl+C to stop]
# [verify audio file appears in queue/]
# [run /process_queue to verify it transcribes correctly]
```

Validate audio quality is acceptable before investing in hotkey setup.

---

### Phase 2B: Instant Capture Integration (1-2 hours)
**Goal**: Enable instant voice capture from anywhere on the system.

Can be done in parallel (for users managing multiple machines):
- [Chore: Platform-Specific Hotkey Setup Guides](./chore-hotkey-setup-guides.md) - macOS section
- [Chore: Platform-Specific Hotkey Setup Guides](./chore-hotkey-setup-guides.md) - Ubuntu section

Must be done after recording script exists:
1. [Feature: Claude-Integrated Record Command](./feature-claude-record-command.md) - Creates `/record_memo` slash command for in-session recording

**Success Criteria**:
- Pressing a global hotkey starts/stops recording (system-wide)
- `/record_memo` command works from within Claude Code sessions
- Both paths save audio to queue/ automatically
- Recording indicator provides clear feedback

**🔄 USER BREAKPOINT #6**: Use the hotkey system for 3-5 days. Validate:
- Instant capture feels natural and fast
- You're capturing more thoughts than before
- The queue is processing smoothly
- The workflow feels "frictionless"

---

## Path Dependencies Diagram

```
Phase 1A: Architecture Decision
    ↓
Phase 1B: Queue Foundation
    ├─ Setup Directories (must exist first)
    └─ Title Generation (must exist before processor uses it)
    ↓
Phase 1C: Queue Processing
    ├─ Queue Processor (uses title generation)
    └─ Queue Status (reads from queue/)
    ↓
Phase 1D: Documentation
    ↓
🔄 USER VALIDATION: Use queue system for 1-2 weeks
    ↓
Phase 2A: Audio Capture Foundation
    ├─ Install sox
    └─ Recording Script (depends on sox)
    ↓
Phase 2B: Instant Capture Integration
    ├─ Hotkey Setup Guides (documents how to use recording script)
    └─ Claude Record Command (calls recording script)

Critical Path:
- Architecture Decision → Queue Directories → Title Generation → Queue Processor
- Queue Processor validated → sox → Recording Script → Hotkey Setup
```

## Implementation Notes

### Cross-Cutting Concerns

**Architecture Decisions:**
- **Standalone + Claude integration**: Recording works system-wide (hotkey) or from within Claude (`/record_memo`), both feed the same queue
- **Parallel sub-agents**: Use Claude's Task tool to process multiple audio files concurrently (Path 1 implementation detail)
- **Intelligent titling**: Generate titles during transcription for instant feedback (not batched at end)

**Shared Dependencies:**
- **sox**: Cross-platform audio recording (macOS via Homebrew, Ubuntu via apt)
- **OpenAI Whisper API**: Existing `scripts/transcribe.py` already handles this
- **Python pydub**: Already used for audio chunking, will be used by queue processor

**Testing Strategy:**
- **Phase 1 validation**: Manual testing with 3-5 audio files dropped into queue/
- **Phase 2 validation**: Real-world usage testing with hotkey capture for several days
- **Title quality**: Evaluate on diverse audio samples (code ideas, meeting notes, research thoughts, task lists)
- **Parallel processing**: Test with 10+ files to verify sub-agents work correctly

**Rollout Plan:**
- **Incremental adoption**: Each phase is independently useful
- **Breakpoints prevent waste**: User validates each phase before investing in the next
- **Fallback safety**: If hotkeys don't work out, queue system alone is still 10x better than current workflow

### User Testing Breakpoints

This epic includes **6 explicit user testing breakpoints** (marked with 🔄):
1. After architecture decision (review approach)
2. After title generation (test title quality)
3. After queue processor (validate batch processing works)
4. After 1-2 weeks of queue usage (confirm value before hotkey investment)
5. After recording script (verify audio quality)
6. After hotkey setup (validate frictionless capture workflow)

Each breakpoint is a decision point: proceed to next phase, iterate on current phase, or stop if goals are met.

## Success Metrics

- [ ] **Capture friction reduced**: Time from "thought" to "queued audio" drops from ~2 minutes to ~2 seconds
- [ ] **Batch processing works**: Can process 10+ audio files in queue/ without manual intervention
- [ ] **Discoverability improved**: Can find past memos by reading output directory titles (no grepping timestamps)
- [ ] **Parallel processing scales**: Multiple audio files process concurrently via sub-agents
- [ ] **Cross-platform support**: Works on both macOS and Ubuntu
- [ ] **Daily usage adoption**: User naturally reaches for voice capture multiple times per day

## Future Enhancements

Ideas that came up during vision planning but are out of scope for this epic:

1. **Real-time transcription**: Stream transcription results as audio is being processed
2. **Smart queue prioritization**: Process shorter memos first, or allow "urgent" tagging
3. **Voice command detection**: Auto-tag request type based on phrases like "urgent" or "research task"
4. **Output search & index**: Full-text search across all past transcriptions (SQLite-backed)
5. **Semantic titling**: Use embedding similarity to avoid duplicate titles and suggest related memos
6. **Audio playback links**: Keep original audio in archive with playback link in README
7. **Automatic queue processing**: File watcher or cron job instead of manual `/process_queue`
8. **Mobile integration**: iOS/Android apps that save directly to queue/ via file sync
9. **Privacy-focused local models**: Option to use local Whisper instead of OpenAI API
