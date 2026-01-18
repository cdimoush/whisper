# Whisper - Claude Code Agent Guide

This document provides context for Claude Code agents working on the Whisper project.

---

## Project Overview

Whisper is a voice memo transcription and processing system that captures thoughts at speech speed and transforms them into actionable outputs using AI agents. It's evolving from a simple transcription tool into a comprehensive second brain with knowledge management, task tracking, and autonomous development capabilities.

**Core Philosophy**: Remove friction from thought capture. Ideas move faster than typing - voice memos bridge that gap.

---

## System Architecture

```
Recording → Queue → Transcription → Agent Processing → Output
                                                     → Brain
```

### Components

1. **Recording Layer**
   - System hotkeys (Raycast on macOS, GNOME on Ubuntu)
   - CLI scripts (`scripts/record_memo.sh`, `scripts/instant_memo.sh`)
   - Instant capture to queue or clipboard

2. **Queue System** (`queue/`)
   - Unprocessed audio files waiting for transcription
   - Cloud-synced via Syncthing (iCloud/Google Drive compatible)
   - Batch processing via `/process_queue`

3. **Transcription**
   - OpenAI Whisper API (`gpt-4o-mini-transcribe` default)
   - Automatic chunking for files >8 minutes
   - Supports: mp3, m4a, wav, webm (max 25MB)

4. **Agent Processing**
   - Interprets spoken request
   - Creates deliverables (summaries, research, code, plans)
   - Generates intelligent output directory names

5. **Output** (`output/`)
   - Organized by: `intelligent-title_YYYY-MM-DD_HH-MM-SS/`
   - Contains: original audio, transcription, deliverables
   - **Not committed to git** (add to .gitignore)

6. **Brain** (`brain/`)
   - Persistent knowledge base for context across memos
   - See "Brain System" section below
   - **Not committed to git** (personal context files)

---

## Brain System

The `brain/` directory is Whisper's memory - persistent context that agents access across all voice memos.

### Structure

```
brain/
├── summary.md              # Chronological summary of all memos to date
├── claudes_wants_this.md   # Strategic roadmap and time allocation
├── active_projects.md      # Current projects, priorities, blockers
├── people.md               # Team members, executives, communication context
├── technical_systems.md    # Architecture docs for Design Lab, Isaac Sim, etc.
├── glossary.md            # Technical terms, acronyms, project names
└── tags.md                # Tagging strategy and tag reference
```

### Purpose

**Problem**: Each new voice memo starts from scratch. Agents don't remember previous conversations, team context, or technical architecture.

**Solution**: Brain files provide persistent context. Instead of re-explaining "What's Design Lab?" or "Who's Nick?" every time, point agents to brain files.

### Usage Pattern

**Without brain** (inefficient):
```
User: "Help me with Design Lab"
Agent: "What's Design Lab?"
User: [Explains for 5 minutes]
[Next day]
User: "More Design Lab work"
Agent: "Remind me about Design Lab?"
```

**With brain** (efficient):
```
User: "Design Lab work - check brain/technical_systems.md"
Agent: [Reads once, has full context, gets to work immediately]
[Next day]
User: "More Design Lab - same context"
Agent: [Already has context from brain files]
```

### When Agents Should Read Brain Files

**Always include** in context for voice memo processing:
- `brain/active_projects.md` - Know current priorities
- `brain/glossary.md` - Understand terminology

**Include based on memo content**:
- Mentions "Design Lab" or "Simulation Mandate" → `brain/technical_systems.md`
- Mentions "Nick" or "Shiva" → `brain/people.md`
- Strategic planning topics → `brain/claudes_wants_this.md`

**Future**: Automatic context injection based on project tags (see `brain/tags.md`)

### Maintaining Brain Files

**When to update**:
- New project starts → Add to `active_projects.md`
- Project status changes → Update `active_projects.md`
- New team member → Add to `people.md`
- New technical system → Add to `technical_systems.md`
- Process quarterly memos → Update `summary.md`

**How to update**:
- Read existing file first (understand current state)
- Make targeted updates (don't rewrite everything)
- Keep summaries concise (agents will read these frequently)
- Use tags consistently (see `brain/tags.md`)

---

## Tagging Strategy

Tags organize memos and brain files for quick context retrieval.

### Tag Categories

- **Project tags**: `design-lab`, `simulation-mandate`, `whisper`, `hologram`, `apollo-3`
- **Technology tags**: `isaac-sim`, `ros2`, `artemis`, `airlab`, `beads`
- **People tags**: `nick-cto`, `shiva-vp`, `melissa`, `ravi`
- **Process tags**: `strategic-planning`, `meta-work`, `delegation`, `automation`

### Tag Format

- Lowercase with hyphens (kebab-case): `simulation-mandate` not `Simulation_Mandate`
- Multiple tags allowed and encouraged
- Placed at bottom of markdown files in code blocks

**Example**:
```markdown
---

## Tags

`design-lab` `isaac-sim` `architecture` `strategic-planning`
```

### Context Injection via Tags

**Future capability**: Slash commands will support project tags:
```bash
/act audio.m4a --project=simulation-mandate
```

Agent automatically receives:
- Audio transcription
- Relevant brain files (technical_systems.md, people.md, glossary.md)
- Previous memo summaries with same tags

See `brain/tags.md` for complete tagging documentation.

---

## Key Slash Commands

### Core Commands

**`/act <audio-path>`**
Full processing pipeline for a single voice memo:
1. Transcribe audio via Whisper API
2. Generate intelligent title from content
3. Interpret spoken request
4. Create deliverables (summaries, research, code, plans)
5. Move audio to organized output directory

**`/process_queue`**
Batch process all audio files in `queue/`:
- Processes files in parallel (3-5x faster than sequential)
- Each file goes through full `/act` pipeline
- Reports success/failure for each file

**`/queue_status`**
Show pending audio files in queue with duration estimates.

**`/record_memo`**
Start recording from within Claude Code session. Saves to queue when stopped.

### Development Commands

**`/vision <topic>`**
Create high-level strategic vision document with multiple implementation paths.

**`/epic <vision>`**
Break a vision into ordered specs with dependencies.

**`/feature <description>`**
Plan and implement a single feature.

**`/chore <description>`**
Plan and implement maintenance/infrastructure work.

**`/implement <plan>`**
Execute an existing plan (from vision/epic/feature).

### Utility Commands

**`/transcribe <audio-path>`**
Simple transcription only (no processing or deliverables).

**`/tools`**
List all available slash commands.

**`/prime`**
Initialize agent with project context (reads brain files).

**`/install`**
Setup guide for installing Whisper and dependencies.

---

## Development Workflow

### For Voice Memo Processing

1. **Read brain context first**
   ```
   Read brain/active_projects.md to understand current priorities
   Read brain/glossary.md to understand terminology
   ```

2. **Transcribe audio**
   ```
   Use OpenAI Whisper API to transcribe
   Chunk if >8 minutes
   ```

3. **Interpret request**
   ```
   What is user asking for?
   What deliverables make sense? (summary, research, code, plan, etc.)
   What project does this relate to? (check brain/active_projects.md)
   ```

4. **Create deliverables**
   ```
   Write README.md with transcription
   Create additional files as needed (research.md, plan.md, code files, etc.)
   Include references to relevant brain files
   ```

5. **Organize output**
   ```
   Generate intelligent title (kebab-case)
   Create directory: output/title_YYYY-MM-DD_HH-MM-SS/
   Move audio file to output directory
   Write all deliverables to output directory
   ```

6. **Tag appropriately**
   ```
   Add tags to README (see brain/tags.md)
   Use project, technology, and process tags
   ```

### For Feature Development

1. **Use planning commands first**
   ```
   /vision for strategic planning
   /epic for breaking down visions
   /feature for specific implementations
   ```

2. **Check existing code**
   ```
   Read relevant Python files in src/
   Understand current architecture
   Follow existing patterns
   ```

3. **Write tests**
   ```
   Add tests for new functionality
   Run existing tests to ensure no regression
   ```

4. **Update documentation**
   ```
   Update README.md if adding user-facing features
   Update this file (CLAUDE.md) if adding agent-facing changes
   Update brain files if affecting workflows
   ```

---

## Critical Context

### What This Tool Is For

**Primary use case**: Capturing and processing voice memos for a developer working on robotics simulation (Design Lab, Simulation Mandate projects).

**Secondary use case**: Building meta-infrastructure (Whisper itself) to enable faster development through AI agents.

**Not for**: General-purpose transcription, podcast processing, or public-facing applications (yet).

### User's Work Context

The user (Conner) works on:
- **Design Lab**: Robot simulation tool (Isaac Lab wrapper)
- **Simulation Mandate**: Company-wide Isaac Sim platform vision
- **Whisper**: This tool (meta work)
- **Hologram/Mirage**: Learning project for Isaac Sim extensions

Key people:
- **Nick** (CTO): Direct manager, loves mechanical engineering
- **Shiva** (VP Software): Needs to escalate Simulation Mandate
- **Melissa**: Junior dev, learning Design Lab

See `brain/people.md` and `brain/active_projects.md` for complete context.

### User's Goals

1. **Immediate**: Remove friction from voice memo workflow
   - Cloud sync (✅ done via Syncthing)
   - Brain system for persistent context (⏳ in progress)
   - Context injection for slash commands (⏳ next)

2. **Short-term** (2 weeks): Foundation infrastructure
   - Beads task management integration
   - Automated greenfield project workflows
   - Hologram/Mirage learning project

3. **Medium-term** (1 month): Strategic projects
   - Simulation Mandate architecture
   - Whisper as second brain
   - Design Lab delegation

4. **Long-term** (3+ months): Scaling
   - Multi-agent orchestration
   - 24/7 background processing
   - Cross-repository integration

See `brain/claudes_wants_this.md` for complete strategic roadmap.

### Time Allocation Philosophy

User is transitioning from **tactical developer** (writes all code) to **strategic architect** (enables others, builds multipliers).

Time split:
- 40% Simulation Mandate (strategic work)
- 30% Whisper infrastructure (force multiplier)
- 20% Design Lab (delegate tactical, do architecture)
- 10% Embodiment leadership (strategic guidance)

**Implication for agents**: Prioritize work that multiplies user's effectiveness (tools, automation, delegation) over tactical implementation.

---

## File Organization

### What Gets Committed to Git

**Committed**:
- Source code (`src/`, `scripts/`)
- Documentation (`README.md`, `CLAUDE.md`, `docs/`)
- Slash commands (`.claude/commands/`, `.claude/agents/`)
- Configuration (`pyproject.toml`, `.gitignore`)

**NOT committed** (in `.gitignore`):
- `queue/` - Unprocessed audio files
- `output/` - Processed memos with transcriptions
- `brain/` - Personal context files
- `archive/` - Old or completed memos
- `*.env` - Environment variables
- `*.m4a`, `*.mp3`, `*.wav` - Audio files

### Why Brain Isn't Committed

Brain files contain:
- Personal work context (team dynamics, meeting notes)
- Company-specific project details
- Strategic planning documents
- Private reflections

These are user-specific and shouldn't be in public repo. Each user should build their own brain.

---

## Common Patterns

### Pattern: Processing a Voice Memo

```python
# 1. Read brain context
context_files = [
    "brain/active_projects.md",
    "brain/glossary.md",
    "brain/technical_systems.md"  # if technical content
]

# 2. Transcribe
transcription = whisper_api.transcribe(audio_path)

# 3. Interpret
# What is user asking for?
# What project does this relate to?
# What deliverables are needed?

# 4. Create output directory
title = generate_intelligent_title(transcription)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_dir = f"output/{title}_{timestamp}"

# 5. Create deliverables
create_readme(output_dir, transcription, tags)
create_additional_files(output_dir, request_type)

# 6. Move audio
move(audio_path, f"{output_dir}/{original_filename}")
```

### Pattern: Context Injection

```python
# Determine relevant context based on content
def get_relevant_context(content: str) -> list[str]:
    context_files = [
        "brain/active_projects.md",  # Always include
        "brain/glossary.md"           # Always include
    ]

    # Add based on content
    if any(term in content.lower() for term in ["design lab", "workbench", "gantry"]):
        context_files.append("brain/technical_systems.md")

    if any(term in content.lower() for term in ["nick", "shiva", "melissa"]):
        context_files.append("brain/people.md")

    if any(term in content.lower() for term in ["strategy", "planning", "priority"]):
        context_files.append("brain/claudes_wants_this.md")

    return context_files
```

### Pattern: Intelligent Title Generation

```python
# Good titles are:
# - Descriptive of content
# - Kebab-case (lowercase with hyphens)
# - 3-5 words ideal
# - Scannable in directory listing

# Examples:
# ✅ "simulation-mandate-ros2-architecture"
# ✅ "design-lab-contact-sensors"
# ✅ "strategic-planning-q1-priorities"
# ❌ "memo-2026-01-17"
# ❌ "VoiceMemo_001.m4a"
```

---

## Technical Details

### Transcription Service

```python
# Default model: gpt-4o-mini-transcribe (fast, cheap)
# Alternative: gpt-4o-transcribe (higher quality)
# Alternative: whisper-1 (supports timestamps)

# Chunking for long audio
# Files >8 minutes are automatically split into 5-minute chunks
# Transcriptions are concatenated with smooth transitions
```

### Recording System

```bash
# Uses sox for audio capture
# macOS: brew install sox
# Ubuntu: sudo apt-get install sox libsox-fmt-all

# Recording formats:
# - Queue: saves .wav to queue/ for later processing
# - Instant: transcribes immediately, copies to clipboard, no file saved
```

### Cloud Sync

```
# User has Syncthing configured
# queue/ and output/ are synced across devices
# Phone → Syncthing → Mac/Ubuntu → Whisper processing
# No additional cloud sync setup needed
```

---

## Future Enhancements

### Near-term (Weeks)

1. **Context injection via project tags**
   - `--project=simulation-mandate` flag for commands
   - Automatic inclusion of relevant brain files
   - Previous memo retrieval by tag

2. **Beads integration**
   - Git-backed task management
   - Replace markdown planning with version-controlled tasks
   - Agent memory across sessions

3. **Automated greenfield workflows**
   - Voice memo → new project initialization
   - Docker environment, Git repo, CI/CD
   - Agents work autonomously, report back

### Medium-term (Months)

1. **Second brain features**
   - Note dependencies and relationships
   - Graph view of memo connections
   - Smart search across all outputs
   - Auto-summarization of related memos

2. **Multi-agent orchestration**
   - Multiple agents working simultaneously
   - Gastown-style coordination
   - Task distribution and result synthesis

3. **Cross-repository integration**
   - `.claude/` framework across multiple repos
   - Agents access relevant codebases for context
   - Unified knowledge graph

### Long-term (Quarters)

1. **24/7 autonomous processing**
   - Cloud compute for background agents
   - Voice memo → overnight development → morning review
   - Quality gates (tests pass before review)

2. **Automated PR generation**
   - Voice memo describing feature
   - Agent implements and tests
   - Creates PR with description and code

3. **Cross-device unified brain**
   - Sync brain/ across all machines
   - Phone, laptop, desktop, cloud
   - Always-available context

---

## Troubleshooting

### Agent Best Practices

**DO**:
- Read brain files before processing memos
- Use consistent tagging (check `brain/tags.md`)
- Generate descriptive output directory names
- Include transcription in README.md
- Tag deliverables appropriately
- Reference brain files in output

**DON'T**:
- Assume context without reading brain files
- Create generic output names like "memo1", "audio-transcription"
- Skip tagging
- Forget to move audio to output directory
- Re-explain concepts that exist in brain files

### Common Issues

**"What's Design Lab?"**
→ Read `brain/technical_systems.md` first

**"Who should I talk to about X?"**
→ Read `brain/people.md` first

**"What are current priorities?"**
→ Read `brain/active_projects.md` first

**"What does this term mean?"**
→ Read `brain/glossary.md` first

**"Where should I focus effort?"**
→ Read `brain/claudes_wants_this.md` first

---

## Quick Reference

### Essential Files
- `README.md` - User-facing documentation
- `CLAUDE.md` - This file (agent guide)
- `brain/` - Persistent context (read first!)
- `.claude/commands/` - Slash commands

### Key Commands
- `/act` - Full memo processing
- `/process_queue` - Batch processing
- `/queue_status` - Check queue
- `/vision`, `/epic`, `/feature` - Planning

### Brain Files
- `summary.md` - All memos to date
- `active_projects.md` - Current work
- `people.md` - Team context
- `technical_systems.md` - Architecture
- `glossary.md` - Terminology
- `tags.md` - Tagging strategy

### Directories
- `queue/` - Unprocessed audio
- `output/` - Processed memos (not committed)
- `brain/` - Context files (not committed)
- `scripts/` - Recording scripts
- `src/` - Python source

### Development
- Language: Python 3.12+
- Package manager: uv (or pip)
- Dependencies: openai, pydub, python-dotenv
- External: ffmpeg, sox

---

## Contact & Feedback

For issues or questions about Whisper development:
- Check `brain/active_projects.md` for current priorities
- Check `brain/claudes_wants_this.md` for strategic direction
- Create GitHub issue (if public repo)
- Voice memo describing the issue (dogfooding!)

---

*Last updated: 2026-01-17*

**Tags**: `whisper` `documentation` `agent-guide` `brain` `context-injection` `workflow` `reference`
