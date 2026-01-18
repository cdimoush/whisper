# Data Model: Aura

**Date**: 2026-01-18
**Branch**: `001-aura-workflow-layer`

## Overview

Aura uses file-based storage. All entities are markdown files or directories that can be committed to git.

## Entities

### AudioMemo

A voice recording captured by the user.

**Storage**: `.aura/queue/<filename>.<ext>`

**Attributes**:
| Field | Type | Description |
|-------|------|-------------|
| filename | string | Original filename |
| format | enum | mp3, m4a, wav, webm |
| duration | number | Length in seconds |
| created_at | timestamp | When recorded |
| status | enum | queued, processing, processed, failed |

**State Transitions**:
```
queued → processing → processed
                   → failed
```

**Notes**: Audio files are not committed to git (in .gitignore). Only metadata matters.

---

### Transcription

Text output from processing an audio memo.

**Storage**: `.aura/output/<title>_<timestamp>/transcription.md`

**Attributes**:
| Field | Type | Description |
|-------|------|-------------|
| source_file | string | Original audio filename |
| text | string | Full transcription text |
| duration | number | Audio length processed |
| model | string | Transcription model used |
| created_at | timestamp | When transcribed |

**Notes**: Stored in output directory alongside deliverables.

---

### Epic

A high-level feature document with phases and grouped work items.

**Storage**: `specs/<epic-name>/README.md`

**Attributes**:
| Field | Type | Description |
|-------|------|-------------|
| title | string | Epic name |
| description | string | What this epic achieves |
| phases | list | Ordered execution phases |
| specs | list | Related spec files |
| status | enum | draft, approved, in_progress, complete |

**Structure**:
```markdown
# Epic: <title>

## Overview
<description>

## Phases

### Phase 1: <name>
- [ ] Spec 1
- [ ] Spec 2

### Phase 2: <name>
- [ ] Spec 3
```

---

### Ticket

A single unit of work tracked in the beads system.

**Storage**: `.beads/tasks/<id>.md` (managed by beads CLI)

**Attributes**:
| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique task identifier |
| title | string | Brief description |
| description | string | Detailed requirements |
| status | enum | open, in_progress, closed |
| dependencies | list | IDs of blocking tasks |
| created_at | timestamp | When created |
| closed_at | timestamp | When completed |

**State Transitions**:
```
open → in_progress → closed
```

**Notes**: Managed by `bd` CLI. Aura commands are thin wrappers.

---

### TaskGraph

The collection of tickets and their dependency relationships.

**Storage**: `.beads/` directory (managed by beads CLI)

**Relationships**:
- Epic contains many Tickets (via `/aura.tickets`)
- Tickets have dependencies on other Tickets
- Task state changes cascade to dependents

---

### AuraConfig

Project-level Aura configuration.

**Storage**: `.aura/config.md`

**Attributes**:
| Field | Type | Description |
|-------|------|-------------|
| project_name | string | Name of the project |
| transcription_model | string | Default model (gpt-4o-mini-transcribe) |
| queue_dir | string | Where to store audio queue |
| output_dir | string | Where to store processed output |

**Notes**: Optional. Sensible defaults if not present.

## Directory Structure

After `aura init`, target codebase contains:

```
.aura/
├── config.md           # Project configuration
├── queue/              # Unprocessed audio (gitignored)
└── output/             # Processed memos (gitignored)

.beads/                 # Task tracking (created by bd init)
├── tasks/
└── ...

.claude/
└── commands/
    ├── aura.record.md
    ├── aura.act.md
    ├── aura.transcribe.md
    ├── aura.epic.md
    ├── aura.feature.md
    ├── aura.tickets.md
    ├── aura.implement.md
    ├── aura.prime.md
    ├── beads.status.md
    ├── beads.ready.md
    ├── beads.start.md
    └── beads.done.md
```

## Validation Rules

1. **Audio files**: Must be < 25MB, supported format
2. **Transcriptions**: Must have non-empty text
3. **Epics**: Must have at least one phase
4. **Tickets**: Must have unique ID within project
5. **Dependencies**: No circular references allowed
