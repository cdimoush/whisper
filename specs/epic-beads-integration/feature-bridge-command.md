# Feature: Bridge Command for Epic-to-Beads Conversion

## Feature Description

Create `/beads-from-epic` slash command that reads epic README files and automatically generates a matching Beads task graph. This command parses the "Execution Order" section of epic specs, creates Beads tasks for each spec file, sets up dependency relationships based on documented ordering, and links tasks to their source specs via notes. This bridges Whisper's existing planning documents with Beads execution tracking.

## User Story

As an AI agent working on a Whisper epic
I want to automatically convert epic specs into a Beads task graph
So that I can track execution status and dependencies without manually recreating the plan in Beads

## Problem

Whisper epics exist as markdown documents with ordered specs, but this structure isn't machine-readable for task tracking. Agents must manually create corresponding Beads tasks, risking errors in:
- Task titles not matching spec names
- Dependencies not matching documented order
- Missing links between Beads tasks and spec files
- Duplication of effort (epic already defines structure)

Manual conversion is tedious, error-prone, and creates friction in adopting Beads.

## Solution

Automated parsing of epic README files to generate Beads task graph:

1. **Parse epic README**: Extract specs from "Execution Order" sections
2. **Create Beads tasks**: One task per spec file with matching title
3. **Set dependencies**: Based on "Execute in order" and phase relationships
4. **Link to specs**: Add spec file path to task notes for reference
5. **Preserve phases**: Use task notes to indicate phase grouping

The command validates epic structure, creates tasks with proper blocking relationships, and outputs summary showing what was created.

## Relevant Files

### Files to Modify
- None (new command, doesn't modify existing code)

### New Files
- `.claude/commands/beads-from-epic.md` - Command definition and implementation
- `.claude/agents/beads-bridge.md` (optional) - Specialized agent for complex parsing

## Step by Step Tasks

### 1. Create Command Definition File

Create `.claude/commands/beads-from-epic.md`:

```markdown
# Epic to Beads Bridge

Parse epic README and create matching Beads task graph.

## Usage

/beads-from-epic <epic-directory>

## Example

/beads-from-epic specs/epic-beads-integration

## Implementation

[Parsing logic and Beads task creation]
```

### 2. Implement Epic README Parsing

**Parse structure**:
- Read `<epic-dir>/README.md`
- Extract "Execution Order" sections
- For each phase:
  - Extract spec file links (e.g., `[Chore: Name](./file.md)`)
  - Extract execution order (numbered lists)
  - Extract phase goals and success criteria

**Data structure**:
```python
{
    "phases": [
        {
            "name": "Phase 1: Foundation",
            "goal": "Experience Beads firsthand...",
            "specs": [
                {"type": "chore", "title": "Install and Initialize Beads", "file": "./chore-install-initialize-beads.md", "order": 1},
                {"type": "chore", "title": "Manual Beads Experience", "file": "./chore-manual-beads-experience.md", "order": 2}
            ]
        },
        ...
    ]
}
```

### 3. Implement Beads Task Creation

**For each spec**:
```bash
bd create "Chore: Install and Initialize Beads"
```

**Add notes with context**:
```bash
bd edit <task-id>
# In editor, add:
# Phase: Phase 1 - Foundation
# Type: chore
# Spec: specs/epic-beads-integration/chore-install-initialize-beads.md
# Goal: Install bd CLI and initialize .beads/ directory
```

**Track created task IDs** for dependency setup

### 4. Implement Dependency Logic

**Within-phase dependencies**:
- Specs in same phase execute in numbered order
- Task N depends on Task N-1

```bash
bd dep add <task-2-id> <task-1-id>  # Task 2 depends on Task 1
bd dep add <task-3-id> <task-2-id>  # Task 3 depends on Task 2
```

**Cross-phase dependencies**:
- All tasks in Phase N depend on last task of Phase N-1
- Creates "breakpoint" effect (finish phase before next starts)

```bash
bd dep add <phase-2-first-task> <phase-1-last-task>
```

### 5. Implement Validation and Output

**Validate before creating**:
- Epic README exists and is readable
- "Execution Order" sections present
- Spec files referenced actually exist
- No duplicate task titles

**Create summary output**:
```
📊 Epic to Beads Bridge Results

Epic: Beads Integration with Whisper
Location: specs/epic-beads-integration/README.md

Created Tasks:
  Phase 1: Foundation & Discovery (3 tasks)
    ✓ Task 1: Chore: Install and Initialize Beads
    ✓ Task 2: Chore: Manual Beads Experience (depends on 1)
    ✓ Task 3: Chore: Create AGENTS.md (depends on 2)

  Phase 2: Bridge & Integration (2 tasks)
    ✓ Task 4: Feature: Bridge Command (depends on 3)
    ✓ Task 5: Feature: Workflow Integration (depends on 4)

  ...

Next steps:
  - Run `bd ready` to see available tasks
  - Run `bd show <id>` to view task details
  - Start with task 1 using `bd start 1`
```

### 6. Add Error Handling

**Handle edge cases**:
- Epic directory doesn't exist → clear error message
- README.md missing → clear error message
- Malformed structure → parse errors with line numbers
- Beads not installed → suggest installation
- `.beads/` not initialized → suggest `bd init`

**Graceful degradation**:
- If Beads not available, command explains requirement
- If epic structure unexpected, show what was found

### 7. Run Validation Commands

After implementation:
```bash
# Test command exists
cat .claude/commands/beads-from-epic.md

# Test on this epic (meta!)
/beads-from-epic specs/epic-beads-integration

# Verify tasks created
bd list

# Verify dependencies
bd show 2  # Should depend on 1
bd show 4  # Should depend on 3

# Verify ready tasks
bd ready  # Should show only task 1 (no deps)
```

## Acceptance Criteria

- [ ] `/beads-from-epic` command parses epic README correctly
- [ ] Creates one Beads task per spec with matching title
- [ ] Sets up dependencies based on execution order
- [ ] Within-phase dependencies enforce sequential order
- [ ] Cross-phase dependencies enforce phase boundaries
- [ ] Task notes include phase, type, spec file path, and goal
- [ ] Command validates epic structure before creating tasks
- [ ] Clear summary output showing created tasks and dependencies
- [ ] Error handling for missing files, malformed structure, Beads not installed
- [ ] Works on `specs/epic-beads-integration/` (this epic itself)

## Validation Commands

```bash
# Verify command file exists
ls -la .claude/commands/beads-from-epic.md

# Test parsing (dry run mode if implemented)
/beads-from-epic specs/epic-beads-integration

# Verify Beads tasks created
bd list | wc -l  # Should show 9 tasks (or expected count)

# Verify first task has no deps
bd show 1 | grep "Depends on" | wc -l  # Should be 0

# Verify second task depends on first
bd show 2 | grep "Depends on"  # Should mention task 1

# Verify ready tasks (only first should be ready initially)
bd ready | wc -l  # Should show 1 task

# Mark first task done and check unblocking
bd done 1
bd ready | wc -l  # Should show 1 task (second task now ready)
```

## Notes

**Parsing strategy**:
- Use regex or markdown parsing library
- Look for heading patterns: `### Phase N: Name`
- Extract numbered lists: `1. [Type: Title](./file.md)`
- Be lenient with variations in formatting

**Alternative: Python script**:
Could implement as Python script called by slash command:
```bash
python scripts/beads_bridge.py specs/epic-beads-integration
```
This would allow more robust parsing and testing.

**Future enhancements**:
- Support for breakpoint markers (🔄) - create special "review" tasks
- Bi-directional sync (update epic when Beads changes)
- Support for updating existing task graph (not just creation)
- Tag propagation (epic tags → task tags if Beads supports)

**Testing approach**:
- Test on this epic (meta testing)
- Test on malformed epic (error handling)
- Test on epic with single phase (simple case)
- Test on epic with complex dependencies (stress test)
