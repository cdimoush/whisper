# Chore: Manual Beads Experience

## Overview

Use Beads manually to experience the workflow firsthand before building automation. Create tasks representing real current work, practice the core workflow (`bd ready` → `bd start` → `bd done`), set up dependencies, and observe how blocking works. This hands-on experience is critical—we need to understand what works and what doesn't before investing time in automation.

## Context

**Why this matters**: Automation without understanding leads to automated bad workflows. By using Beads manually, we'll discover friction points, understand the mental model, and validate that this approach actually helps before building tooling around it.

**Current state**: Beads installed but never used in practice.

**Desired state**: User has concrete hands-on experience with Beads workflow, understands core concepts (handles, dependencies, status), and can evaluate if this solves agent memory problems.

## Tasks

### 1. Create Initial Task Graph for Current Work

**Choose a real project** (not toy example):
- Option 1: Beads integration itself (meta!)
- Option 2: Another Whisper feature in progress
- Option 3: Design Lab work if applicable

**Create 5-10 tasks** representing actual work:
```bash
bd create "Install and initialize Beads infrastructure"
bd create "Experience Beads workflow manually"
bd create "Document Beads patterns in AGENTS.md"
bd create "Implement bridge command for epic-to-beads conversion"
bd create "Test multi-session workflow with real feature"
```

**Add descriptions/context**:
```bash
bd edit 1  # Opens editor to add notes about the task
```

**Best practices**:
- Use clear, actionable task titles
- Add context in notes (links to specs, dependencies, rationale)
- Start broad, refine as you go
- Don't over-plan—tasks can be added/modified

### 2. Set Up Dependencies

**Identify blocking relationships**:
- What must be done before what?
- What can be done in parallel?

**Add dependencies**:
```bash
bd dep add 2 1    # Task 2 depends on task 1 (1 blocks 2)
bd dep add 3 2    # Task 3 depends on task 2
bd dep add 4 2    # Task 4 depends on task 2
bd dep add 5 4    # Task 5 depends on task 4
```

**Verify dependency graph**:
```bash
bd show 2  # Should list task 1 as dependency
bd list    # Shows all tasks with indicators
```

**Test blocking**:
```bash
bd ready   # Should only show tasks with no incomplete dependencies
```

Expected: Task 1 appears (no deps), tasks 2-5 don't (blocked)

### 3. Practice Core Workflow

**Workflow pattern**:
```bash
bd ready                    # "What should I work on?"
bd start <id>               # "I'm working on this"
# ... do the work ...
bd done <id>                # "This is complete"
bd ready                    # "What's next?"
```

**Execute task 1**:
```bash
bd ready           # Shows task 1
bd start 1         # Marks as active
bd show 1          # Verify status
# Do the actual work (install Beads - already done)
bd done 1          # Mark complete
```

**Observe unblocking**:
```bash
bd ready           # Now task 2 should appear (was blocked on 1)
```

**Execute task 2**:
```bash
bd start 2
# Experience the workflow (this chore!)
bd done 2
```

**Continue pattern** for 3-4 tasks total

### 4. Experiment with Task Management

**Try different commands**:
```bash
bd list                    # All tasks
bd list --active           # Only active tasks
bd list --done             # Only completed tasks
bd list --ready            # Only ready tasks (same as `bd ready`)

bd show <id>               # Detailed view of single task
bd edit <id>               # Modify task
bd delete <id>             # Remove task (if needed)

bd dep add <task> <blocks> # Add dependency
bd dep rm <task> <blocks>  # Remove dependency
bd deps <id>               # Show task dependencies
```

**Discover what's useful**:
- Which commands would agent use most?
- What information is missing?
- What's confusing or cumbersome?

### 5. File a Discovery Task

**During work, notice something new**:
- Subtask that wasn't in original plan
- Blocker discovered
- Follow-up work needed

**File it immediately**:
```bash
bd create "Update README with Beads usage examples"
bd dep add <new-task-id> <current-task-id>  # Block on current work
```

**Why this matters**: Tests if Beads helps capture discoveries (key pain point from vision)

### 6. Simulate Session Break

**End of session workflow**:
```bash
bd list --active    # What's in-progress?
bd list --ready     # What's available next?
bd list             # Overall status
```

**Document state** (mentally or in notes):
- Where did you leave off?
- What's next?
- Any blockers?

**Leave session**, come back later (or simulate break)

**Resume session**:
```bash
bd ready            # "Where was I?"
bd list --active    # "What was I working on?"
bd show <active>    # "What's the context?"
```

**Evaluate**: Did this help resume context? Faster than reading spec files?

## Acceptance Criteria

- [ ] Created 5-10 tasks representing real work
- [ ] Set up dependencies with blocking relationships
- [ ] Practiced `bd ready` → `bd start` → `bd done` workflow for 3-4 tasks
- [ ] Observed dependency unblocking in action
- [ ] Filed at least one discovery task during work
- [ ] Simulated session break and resumption
- [ ] Documented observations: what felt good, what felt clunky

## Testing

**Workflow validation**:
1. Dependency blocking works (blocked tasks don't show in `bd ready`)
2. Status changes work (start → active, done → completed)
3. Task unblocking works (completing task unblocks dependents)
4. Discovery filing works (create task mid-session, set dependencies)

**User experience evaluation**:
- Is this faster than markdown specs alone?
- Does `bd ready` accurately show next work?
- Are dependencies helpful or annoying?
- Would this solve agent amnesia?

## Dependencies

**Requires**:
- [Chore: Install and Initialize Beads](./chore-install-initialize-beads.md) - Must be completed first

**Blocks**:
- [Chore: Create AGENTS.md](./chore-create-agents-md.md) - Need manual experience before documenting
- All Phase 2 specs - Don't automate what we don't understand

## Estimated Effort

**Time**: 2-3 hours

**Breakdown**:
- Creating initial task graph: 30 minutes
- Setting up dependencies: 15 minutes
- Practicing core workflow: 60 minutes (includes doing actual work)
- Experimenting with commands: 30 minutes
- Simulating session break/resume: 15 minutes
- Documenting observations: 15 minutes

## Implementation Notes

**Real work, not toy example**:
- Use this epic's tasks (meta approach)
- Or use actual Whisper feature work
- Don't create fake tasks just for testing

**Observation focus areas**:
- **Speed**: Faster to check `bd ready` than read spec files?
- **Clarity**: Does task status give clear picture of state?
- **Discovery**: Does filing tasks feel valuable or like overhead?
- **Dependencies**: Helpful enforcement or annoying restrictions?
- **Agent memory**: Would this solve session amnesia problem?

**Document friction points**:
- Commands that are confusing
- Missing information
- Cumbersome workflows
- Unexpected behavior

**Be honest about downsides**:
- Don't force this to work if it doesn't
- Breakpoint #1 decision depends on honest assessment
- It's OK to conclude Beads isn't right fit

## Success Metrics

- User understands core Beads concepts (handles, dependencies, status)
- User has practiced full workflow across multiple tasks
- User can articulate what works well and what doesn't
- User has informed opinion on whether Beads solves agent memory
- Documented observations provide data for Breakpoint #1 decision

## Related Files

- `.beads/issues.jsonl` - Task storage (will be populated)
- Epic specs - May be used as basis for creating tasks
- Notes/observations - Capture learnings for assessment

## Tags

`chore` `discovery` `manual-testing` `beads` `workflow` `hands-on` `phase-1` `user-experience`
