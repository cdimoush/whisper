# Chore: Create AGENTS.md

## Overview

Create `AGENTS.md` documentation that captures the Beads workflow patterns learned from manual experience. This file serves as the reference guide for AI agents on how to use Beads effectively in the Whisper project. It should include when to use Beads, core command patterns, session workflows, and best practices discovered during manual testing.

## Context

**Why this matters**: Agents need explicit documentation on Beads workflow. Without it, agents will either ignore Beads or use it incorrectly. This file becomes the source of truth for "how agents should interact with Beads in Whisper."

**Current state**: No agent documentation for Beads workflow exists.

**Desired state**: `AGENTS.md` in project root with comprehensive Beads workflow guide, ready to be referenced by agents in future sessions.

## Tasks

### 1. Create AGENTS.md File Structure

**Location**: `/Users/conner/dev/whisper/AGENTS.md`

**Structure**:
```markdown
# Beads Workflow for AI Agents

## Overview
[What is Beads, why we use it in Whisper]

## Core Concepts
[Handles, dependencies, status, git-backed storage]

## When to Use Beads
[Session start, during work, session end, multi-agent scenarios]

## Command Reference
[Essential commands with examples]

## Session Workflow
[Start → Work → End patterns]

## Best Practices
[Dos and don'ts from manual experience]

## Integration with Existing Commands
[How Beads relates to /implement, /act, etc.]

## Troubleshooting
[Common issues and solutions]
```

### 2. Document Core Concepts

**Include**:
- **Handles**: Unique task IDs (1, 2, 3...)
- **Dependencies**: Tasks can block other tasks
- **Status**: pending → active → done
- **Git-backed**: Tasks stored in `.beads/issues.jsonl`
- **Ready tasks**: Tasks with no incomplete dependencies

**Example**:
```markdown
### Core Concepts

**Task Handles**: Each task gets a unique numeric ID. Use handles in commands: `bd show 42`

**Dependencies**: Tasks can depend on other tasks. A task is "ready" only when all its dependencies are complete. Use `bd dep add <task> <blocks>` to set up blocking relationships.

**Status Lifecycle**:
- pending: Created but not started
- active: Currently being worked on
- done: Completed
- blocked: Has incomplete dependencies (not a real status, derived)
```

### 3. Document Session Workflow Patterns

**Session Start Pattern**:
```markdown
### Starting a Session

Always begin by checking task status:

```bash
bd ready    # What tasks are available to work on?
bd show <id>  # Get context on specific task
```

If resuming previous work:
```bash
bd list --active  # What was I working on?
bd show <active-id>  # Review context
```
```

**During Work Pattern**:
```markdown
### During Implementation

Mark work as active:
```bash
bd start <id>  # Signal you're working on this
```

File discoveries as you go:
```bash
bd create "Discovered subtask: add error handling"
bd dep add <new-id> <current-id>  # Block on current work
```

Update task notes:
```bash
bd edit <id>  # Add findings, blockers, context
```
```

**Session End Pattern**:
```markdown
### Ending a Session

Complete finished work:
```bash
bd done <id>  # Mark task complete
```

Review state for next session:
```bash
bd list --active  # Any work left in-progress?
bd ready  # What's available next?
```

Optional: Add notes about where you left off:
```bash
bd edit <active-id>  # Add "Stopped at: implementing X"
```
```

### 4. Document Integration with Existing Commands

**How Beads relates to Whisper commands**:

```markdown
### Integration with Whisper Commands

**`/implement` command**: Before implementing a spec, check if Beads task exists:
```bash
bd ready  # Find next ready task
bd show <id>  # Verify matches spec you want to implement
bd start <id>  # Mark as active
# ... do implementation ...
bd done <id>  # Mark complete
```

**`/beads-from-epic` command** (Phase 2): Converts epic specs to Beads task graph. Run once per epic to set up tasks.

**`/act` processing** (future): May create Beads tasks for action items in voice memos.

**When NOT to use Beads**:
- Quick experiments (no tracking needed)
- Research queries (not actionable tasks)
- One-off scripts (ephemeral work)
```

### 5. Capture Best Practices from Manual Experience

**Based on manual testing discoveries**:
- What worked well?
- What was confusing?
- What should agents always/never do?

**Example best practices**:
```markdown
### Best Practices

**DO**:
- Check `bd ready` at start of every session (know what's available)
- File discoveries immediately (don't let subtasks get forgotten)
- Use `bd start` to signal active work (visible to other agents)
- Complete tasks promptly (unblocks dependent work)
- Add context to tasks via `bd edit` (help future sessions)

**DON'T**:
- Work on blocked tasks (defeats purpose of dependencies)
- Leave tasks in active state if not actually working (confuses state)
- Create overly fine-grained tasks (overhead without value)
- Forget to mark tasks done (stale active tasks)
- Skip `bd ready` check (miss important blocking relationships)
```

### 6. Add Command Reference

**Essential commands** with examples:

```markdown
### Command Reference

**View tasks**:
```bash
bd list              # All tasks
bd list --active     # Only active tasks
bd list --done       # Only completed
bd ready             # Tasks ready to work on (no incomplete deps)
```

**Task details**:
```bash
bd show <id>         # Full task info including dependencies, history, notes
```

**Create/modify**:
```bash
bd create "task title"   # Create new task
bd edit <id>             # Edit task (opens editor for notes)
bd delete <id>           # Remove task
```

**Status changes**:
```bash
bd start <id>        # Mark task as active
bd done <id>         # Mark task complete
```

**Dependencies**:
```bash
bd dep add <task> <blocks>   # Add dependency (blocks depends on task)
bd dep rm <task> <blocks>    # Remove dependency
bd deps <id>                 # Show task's dependencies
```
```

### 7. Add Troubleshooting Section

**Common issues**:

```markdown
### Troubleshooting

**Task doesn't appear in `bd ready`**:
- Check if it has incomplete dependencies: `bd show <id>`
- Look for "Depends on:" section
- Complete blocking tasks first, or remove dependency if incorrect

**Changes not showing up**:
- Beads uses local DB cache - should update automatically
- If stale, check `.beads/issues.jsonl` for truth
- Can rebuild: `rm .beads/beads.db && bd list` (regenerates from JSONL)

**Merge conflicts in `.beads/issues.jsonl`**:
- JSONL is append-only, conflicts should be rare
- If conflicts occur, resolve manually (each line is a task event)
- Beads rebuilds state from JSONL events

**`bd` command not found**:
- Ensure Beads is installed: see README.md installation section
- Check PATH includes Beads installation directory
```

## Acceptance Criteria

- [ ] `AGENTS.md` file created in project root
- [ ] Core concepts documented (handles, dependencies, status, git-backed)
- [ ] Session workflow patterns documented (start, during, end)
- [ ] Integration with existing Whisper commands explained
- [ ] Best practices from manual experience captured
- [ ] Command reference with examples included
- [ ] Troubleshooting section with common issues
- [ ] File is comprehensive enough for agent to use Beads without additional guidance

## Testing

**Validation methods**:
1. Read through AGENTS.md as if you're an agent encountering Beads for first time
2. Check: Can you understand workflow from doc alone?
3. Check: Are all essential commands covered?
4. Check: Are best practices actionable and specific?

**Quality criteria**:
- Clear, concise language
- Concrete examples (not abstract descriptions)
- Covers session lifecycle completely
- Addresses integration with Whisper
- Based on real manual experience (not theoretical)

## Dependencies

**Requires**:
- [Chore: Manual Beads Experience](./chore-manual-beads-experience.md) - Must complete manual testing first to know what to document

**Blocks**:
- All Phase 2+ specs - Agents need this reference to use Beads correctly

## Estimated Effort

**Time**: 1-1.5 hours

**Breakdown**:
- Creating file structure: 10 minutes
- Documenting core concepts: 15 minutes
- Writing session workflow patterns: 20 minutes
- Integration documentation: 15 minutes
- Best practices from experience: 15 minutes
- Command reference: 15 minutes
- Troubleshooting: 10 minutes
- Review and refinement: 10 minutes

## Implementation Notes

**Writing style**:
- Clear, direct language (agents interpret literally)
- Concrete examples over abstract concepts
- Step-by-step workflows
- Dos and don'ts explicitly stated

**Based on manual experience**:
- This should reflect what actually worked in manual testing
- If manual testing revealed Beads friction, document it honestly
- Include workarounds discovered during testing

**Living document**:
- This can be updated as we learn more (Phase 2, 3, 4)
- Initial version captures Phase 1 learnings
- Future phases may add sections (e.g., multi-agent patterns)

**Git commit**:
After completing:
```bash
git add AGENTS.md
git commit -m "Add Beads workflow documentation for AI agents"
```

## Success Metrics

- Agent can read AGENTS.md and correctly use Beads workflow
- All essential commands documented with examples
- Session patterns clear and actionable
- Best practices reflect real manual testing insights
- File serves as comprehensive reference (no need to guess)

## Related Files

- `AGENTS.md` - File created by this chore
- `README.md` - Should reference AGENTS.md for Beads workflow
- `.beads/issues.jsonl` - Task storage Beads uses
- Epic specs - Referenced as examples of work tracked in Beads

## Tags

`chore` `documentation` `agents` `beads` `workflow` `best-practices` `phase-1` `reference`
