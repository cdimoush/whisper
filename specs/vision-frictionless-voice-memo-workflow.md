# Vision: Frictionless Voice Memo Workflow

## Vision Statement
Transform voice memo capture from a manual, multi-step process into an instant brain-dump workflow where you can sit down at your computer, hit a few keystrokes from anywhere, record your thoughts, and have them automatically queued, transcribed, intelligently titled, and organized for processing—matching the "vibe coding" efficiency demonstrated by Andrej Karpathy and top AI-assisted developers.

## Current State Analysis

### What Exists Today
- **Solid transcription core**: `scripts/transcribe.py` handles audio files with chunking for long recordings
- **Manual file handling**: Users must manually save Voice Memos to disk, navigate to the file, and run `/transcribe` or `/act_on_audio`
- **Single-file processing**: Each audio file must be individually specified; no queue system
- **Timestamp-based organization**: Output uses datetime stamps (e.g., `2025-01-03_18-30-00/`) which are hard to remember
- **Act-on-audio capability**: `/act_on_audio` command creates organized output with README, but requires manual invocation per file

### Current Pain Points
1. **High friction to start recording**: Must open Voice Memos app, record, save to disk, get path, run command
2. **Location-dependent**: Can only transcribe after navigating to the audio file location
3. **Sequential processing bottleneck**: Must point at one audio file at a time
4. **Poor discoverability**: Datetime stamps make it hard to find "that memo about the API refactor"
5. **No automated intake**: Audio files don't flow automatically into a processing pipeline

### The Gap
Top developers use voice-driven workflows with system-wide hotkeys (like Wispr Flow's "one hotkey, any app" approach) that capture thoughts instantly without breaking flow. Our current system requires 5-8 manual steps between having a thought and getting transcribed, actionable output. We need to go from ~2 minutes to ~2 seconds for capture.

## Vision Goals
1. **Instant capture**: From anywhere on macOS/Ubuntu, hit a global hotkey to start recording and auto-save to queue
2. **Zero-friction intake**: Audio automatically saved to queue directory with no manual file management
3. **Batch processing**: Process entire queue with sub-agents working in parallel, not one-at-a-time
4. **Intelligent titling**: Each output gets a memorable human-readable title in addition to timestamp
5. **Auto-archiving**: Processed audio moves from queue to archive directory automatically

## Implementation Paths

### Path 1: Queue System & Intelligent Titling (Foundation)
**Approach**: Build the queue infrastructure and intelligent output naming without changing capture mechanics yet. Users still manually add files to queue, but processing becomes automated and output becomes discoverable.

**Effort**: Low
**Impact**: Medium
**Risk**: Low

**Dependencies**: None (builds on existing transcribe.py and act_on_audio)

**High-Level Features**:
1. **Queue Directory Structure**: Create `queue/`, `archive/`, and `output/` directories with clear separation of unprocessed, processed audio, and transcription outputs
2. **Queue Processor Command**: New `/process_queue` command that finds all audio files in queue/, processes each with sub-agents (using Task tool), and moves completed files to archive/
3. **Intelligent Title Generation**: After transcription, use LLM to generate a short, memorable title (e.g., "api-refactor-discussion", "standup-ideas-jan-8") and create output directories as `output/TITLE_YYYY-MM-DD_HH-MM-SS/`
4. **Queue Status Command**: New `/queue_status` command to list pending files and their estimated processing time

**High-Level Chores**:
1. **Update .gitignore**: Add queue/, archive/, and output/ directories to prevent committing voice memos
2. **Create Directory Structure**: Initialize the three-directory system with README files explaining purpose
3. **Document Queue Workflow**: Update main README with queue-based workflow instructions

**Trade-offs**:
- ✅ Low risk, builds incrementally on existing code
- ✅ Immediate value: solves discoverability and batch processing problems
- ✅ Can be implemented entirely in Python/bash without system-level integrations
- ✅ Tests the queue concept before investing in hotkey infrastructure
- ❌ Still requires manual file placement in queue/ directory
- ❌ Doesn't solve the instant-capture problem
- ❌ Users still must save Voice Memos to disk manually

---

### Path 2: System-Wide Voice Capture (The Hotkey Layer)
**Approach**: Implement instant voice capture with global hotkeys for macOS and Ubuntu. This is the "game-changer" path that makes voice memos feel like thought capture instead of a multi-step process.

**Effort**: Medium-High
**Impact**: High
**Risk**: Medium

**Dependencies**: Path 1 should be complete (queue system must exist for captured audio to flow into)

**High-Level Features**:
1. **Cross-Platform Recording Script**: Bash script using `sox` (macOS/Ubuntu compatible) that records audio with one command, auto-generates filename, saves to queue/
2. **Global Hotkey Setup (macOS)**: Instructions and automation for setting up Keyboard Maestro, BetterTouchTool, or native Automator to bind hotkey to recording script
3. **Global Hotkey Setup (Ubuntu)**: Instructions for custom keyboard shortcuts calling the recording script via gsettings/xbindkeys
4. **Visual/Audio Feedback**: Recording indicator (terminal notification, sound, or system tray icon) so user knows recording is active
5. **Stop Recording Mechanism**: Second hotkey press stops recording and auto-queues the file

**High-Level Chores**:
1. **Install sox Dependency**: Add sox to setup instructions for both platforms (`brew install sox` / `apt install sox`)
2. **Create Recording Script**: Write `scripts/record_memo.sh` that handles audio capture and auto-queuing
3. **Platform-Specific Setup Guides**: Write detailed setup docs for macOS and Ubuntu hotkey configuration
4. **Test Audio Devices**: Validate default microphone detection works on both platforms

**Trade-offs**:
- ✅ Solves the instant-capture problem completely
- ✅ Brings workflow to "vibe coding" level efficiency
- ✅ sox works cross-platform (no proprietary dependencies)
- ✅ User controls everything (no cloud services, no paid tools required)
- ❌ Requires one-time platform-specific setup (not zero-config)
- ❌ Hotkey configuration varies by macOS version and Ubuntu desktop environment
- ❌ More surface area for support issues (audio driver problems, permission issues)
- ❌ May interfere with existing hotkeys users have configured

---

### Path 3: Claude-Integrated vs. Standalone Recording Decision
**Approach**: Evaluate whether recording should be tightly coupled with Claude Code or remain a standalone system that feeds into Claude. This is an architectural decision point that affects long-term maintainability.

**Effort**: Low (mostly research and decision-making)
**Impact**: Medium (affects architecture, not immediate UX)
**Risk**: Low

**Dependencies**: Should be decided before implementing Path 2

**High-Level Features**:
1. **Architecture Decision Document**: Research and document the trade-offs between Claude-integrated vs. standalone approaches
2. **Prototype Claude Integration**: Test whether `/record_memo` slash command could trigger system recording (via Bash tool executing recording script)
3. **Evaluate Hybrid Approach**: Recording script works standalone, but also callable via Claude command for flexibility

**High-Level Chores**:
1. **Research Claude Bash Tool Capabilities**: Test whether Claude can launch background processes that outlive the command (for recording)
2. **User Preference Survey**: Document what behavior users would expect (always-available hotkey vs. Claude-initiated recording)
3. **Document Recommendation**: Write clear guidance on recommended approach with rationale

**Trade-offs**:
- ✅ Prevents future architectural regret
- ✅ Low effort to evaluate before committing
- ✅ Informs implementation details of Path 2
- ❌ Doesn't deliver immediate user value
- ❌ May lead to analysis paralysis if overthought

**Recommendation: Standalone with Claude Integration**
Based on research, the optimal approach is:
- Recording hotkey is system-wide and independent of Claude (works even when Claude isn't running)
- Claude can also trigger recording via `/record_memo` command for voice capture from within a coding session
- Both approaches save to the same queue/, processed by the same pipeline
- This gives users maximum flexibility: brain-dump at any time, or voice-command while actively working with Claude

---

### Path 4: Premium Polish & Advanced Features (Future)
**Approach**: After core workflow is solid (Paths 1 & 2 complete), add quality-of-life features that elevate the experience from "working" to "delightful."

**Effort**: Medium
**Impact**: Medium
**Risk**: Low

**Dependencies**: Requires Path 1 and Path 2 to be stable and well-tested

**High-Level Features**:
1. **Real-Time Transcription**: Stream transcription results as audio is being processed (show progress)
2. **Smart Queue Prioritization**: Process shorter memos first, or allow user to tag memos as "urgent"
3. **Voice Commands in Recording**: Detect phrases like "urgent", "research task", "code request" during transcription and auto-tag the request type
4. **Output Search & Index**: Searchable index of all past transcriptions (full-text search across all memos)
5. **Semantic Titling**: Use embedding similarity to avoid duplicate titles, suggest related previous memos
6. **Audio Playback in Output**: Keep original audio in archive with playback link in README for verification

**High-Level Chores**:
1. **Add SQLite Index**: Create simple database of transcriptions for fast search
2. **Build Search Interface**: CLI search tool or simple web interface for browsing past memos
3. **Optimize Processing Speed**: Benchmark and optimize transcription throughput for queue processing

**Trade-offs**:
- ✅ Makes the system truly competitive with commercial tools (Wispr Flow, etc.)
- ✅ Adds "delight factor" that encourages daily use
- ✅ Search solves the "where did I say that?" problem
- ❌ Feature creep risk—could distract from core workflow stability
- ❌ Adds complexity and maintenance burden
- ❌ May require additional dependencies (SQLite, search libraries)

---

## Path Comparison Matrix

| Criteria | Path 1 (Queue) | Path 2 (Hotkey) | Path 3 (Architecture) | Path 4 (Polish) |
|----------|----------------|-----------------|----------------------|-----------------|
| Time to Value | Fast | Medium | Fast | Slow |
| Technical Complexity | Low | Medium | Low | Medium |
| User Impact | Medium | High | Low | Medium |
| Maintenance Burden | Low | Medium | Low | High |
| Scalability | High | High | N/A | Medium |

## Recommended Approach

**Phase 1: Path 3 → Path 1** (Week 1-2)
Start with the architecture decision (Path 3) to avoid rework, then immediately implement the queue system (Path 1). This delivers tangible value quickly—users can manually drop files in `queue/` and run `/process_queue` to batch-process with intelligent titling. This is a 10x improvement over current manual one-at-a-time processing.

**Phase 2: Path 2** (Week 2-4)
Once queue system proves solid, tackle the hotkey layer (Path 2). Start with macOS (since you mentioned it first) using sox + one-time hotkey setup guide. Test extensively with real usage. Then adapt for Ubuntu. This completes the instant-capture vision.

**Phase 3: Path 4** (Future, on-demand)
After 2-4 weeks of real usage with Paths 1 & 2, evaluate which Path 4 features would have the highest impact. Implement selectively based on actual pain points, not speculation. Search/index is likely the first high-value add.

**Why This Order:**
1. **Architectural clarity first** prevents building the wrong thing
2. **Queue system first** proves the concept and delivers immediate value with minimal risk
3. **Hotkey layer second** builds on proven queue foundation
4. **Polish last** ensures we're polishing something people actually use

## Path Dependencies Diagram

```
Path 3 (Architecture Decision)
    ↓
Path 1 (Queue System + Intelligent Titling)
    ↓
Path 2 (System-Wide Hotkey Capture)
    ↓
Path 4 (Premium Polish & Advanced Features)

Note: Path 3 must complete before Path 1
      Path 1 must be stable before Path 2
      Path 2 should be well-tested before Path 4
```

## Next Steps

1. **Make Architecture Decision** (Path 3): Decide on standalone vs. Claude-integrated recording approach. **Recommendation**: Standalone hotkey + optional Claude command integration.

2. **Implement Queue System** (Path 1):
   - Create `/feature queue-system-intelligent-titling` plan
   - Build queue processing with sub-agent parallelization
   - Implement intelligent title generation
   - Test with 5-10 sample audio files

3. **Document Queue Workflow**: Update README with clear instructions on how to use queue-based processing

4. **Plan Hotkey Implementation** (Path 2): Once queue is proven, create `/feature system-wide-voice-capture` plan

5. **User Testing**: After Path 1 is complete, use it daily for 1-2 weeks to validate the queue workflow before investing in hotkey infrastructure

## Open Questions

1. **Hotkey preference**: Do you prefer a system-level hotkey (works everywhere) or Claude-integrated recording only? **Recommendation**: Both—hotkey for instant capture, Claude command for in-session recording.

2. **Transcription model**: Should we stick with `gpt-4o-mini-transcribe` (fast, cheap) or upgrade to `gpt-4o-transcribe` (higher quality) for queue processing? **Impact**: Cost increases ~4x for higher quality.

3. **Queue processing trigger**: Should queue processing be:
   - Manual (`/process_queue` command)
   - Automatic on schedule (cron job every 10 minutes)
   - Automatic on file add (file watcher)

   **Recommendation**: Start with manual for control, add auto-processing later as opt-in.

4. **Title generation strategy**: Should titles be:
   - Generated immediately during transcription (requires extra LLM call)
   - Generated at end of processing (all titles created together, potential rate limit issues)

   **Recommendation**: Generate during transcription for instant feedback.

5. **macOS vs. Ubuntu priority**: Which platform should we optimize for first? (You mentioned both, but macOS Voice Memos suggests macOS is primary.)

6. **Commercial tool integration**: Would you consider Wispr Flow or similar paid tools for capture, using this system only for queue processing and organization? Or is the goal full DIY control?

## Future Considerations

1. **Multi-modal capture**: Extend to screenshots, photos, PDFs—any input that benefits from AI processing and organization
2. **Collaborative queues**: Share queue directories via Dropbox/sync for team voice memo processing
3. **Mobile integration**: iOS/Android apps that save directly to queue directory via file sync
4. **Real-time streaming**: Live transcription during recording (harder but possible with Whisper streaming)
5. **Custom processing pipelines**: User-defined actions based on voice commands or keywords ("email this to myself", "add to calendar")
6. **Integration with note-taking apps**: Auto-export to Obsidian, Notion, Roam Research
7. **Voice authentication**: Different processing pipelines per user (for shared computers)
8. **Privacy-focused local models**: Option to use local Whisper instead of OpenAI API for sensitive recordings

---

## Research Sources

### Vibe Coding & Developer Workflows
- [Vibe Coding: AI + Voice = The New Developer Workflow](https://wisprflow.ai/vibe-coding)
- [Andrej Karpathy on Software 3.0: Software in the Age of AI](https://www.latent.space/p/s3)
- [A weekend 'vibe code' hack by Andrej Karpathy quietly sketches the missing layer of enterprise AI orchestration](https://venturebeat.com/ai/a-weekend-vibe-code-hack-by-andrej-karpathy-quietly-sketches-the-missing)
- [AI Guru Andrej Karpathy Unveils 2025 Annual Summary: LLMs Step into New Era of "Ghost Intelligence" and "Ambient Programming"](https://eu.36kr.com/en/p/3606454820996104)

### Voice-to-Text Tools for Developers
- [Wispr Flow Review (2026): AI Dictation for Developers](https://vibecoding.app/blog/wispr-flow-review)
- [Best Voice-to-Text for Developers in 2025: My Tested Recommendations](https://zackproser.com/blog/best-voice-to-text-for-developers)
- [voice-to-text-tools-developers-coding](https://willowvoice.com/blog/voice-to-text-tools-developers-coding)

### Terminal Recording & Automation
- [Using sox to record audio on OS X](https://support.moonpoint.com/os/os-x/audio/sox.php)
- [Using SOX on macOS](https://chrisrosser.medium.com/using-sox-on-macos-48f25014d1e3)
- [Support sox for macOS · Issue #1 · synesthesiam/voice-recorder](https://github.com/synesthesiam/voice-recorder/issues/1)
