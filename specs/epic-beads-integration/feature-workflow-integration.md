# Feature: Workflow Integration Commands

## Feature Description

Integrate Beads into existing Whisper agent workflows by modifying `/implement` to check Beads first, and creating new `/land` and `/beads-status` commands. This makes Beads the default source of truth for "what's next" while maintaining backward compatibility for non-Beads workflows. Agents will naturally check `bd ready` at session start, update status during work, and cleanly land tasks at session end.

## User Story

As an AI agent implementing Whisper features
I want Beads to be integrated into my natural workflow
So that I automatically benefit from task tracking and agent memory without explicit instructions

## Problem

Even with Beads installed and tasks created, agents won't use it unless explicitly told. Current workflow:
1. Agent reads epic spec to understand what to implement
2. Agent implements without status tracking
3. Session ends with no memory of progress

Agents need workflow commands that make Beads checking automatic and natural:
- **Session start**: "What should I work on?" → check Beads
- **During work**: Status updates happen automatically
- **Session end**: Clean handoff for next session

Without integration commands, Beads remains a parallel system that agents forget to use.

## Solution

Three-part integration:

1. **Modify `/implement`**: Check `bd ready` before implementation, mark tasks active, mark done upon completion
2. **Create `/land`**: Session-end cleanup command (review active tasks, update status, prepare for next session)
3. **Create `/beads-status`**: Quick visibility into project status (what's done, in-progress, ready, blocked)

These commands make Beads usage natural and automatic rather than manual and remembered.

## Relevant Files

### Files to Modify
- `.claude/commands/implement.md` - Add Beads checking logic

### New Files
- `.claude/commands/land.md` - Session-end cleanup
- `.claude/commands/beads-status.md` - Project status overview

## Step by Step Tasks

### 1. Modify `/implement` Command

**Read current implementation**:
```bash
cat .claude/commands/implement.md
```

**Add Beads integration logic**:

```markdown
# Implement Feature/Chore

Before implementing, check if Beads task exists:

## Step 1: Check Beads (if available)

If `.beads/` directory exists:
```bash
bd ready
```

If task matches what you're implementing:
```bash
bd start <task-id>  # Mark as active
```

If no matching task, proceed without Beads (graceful degradation).

## Step 2: Implement as usual

[Existing implementation logic]

## Step 3: Update Beads (if used)

If you marked task active in Step 1:
```bash
bd done <task-id>  # Mark complete
```

Check what's next:
```bash
bd ready  # Show newly unblocked tasks
```
```

**Preserve backward compatibility**:
- Check if `.beads/` exists before running Beads commands
- If Beads not available, implement without it
- No errors or warnings if Beads missing

### 2. Create `/land` Command

**Purpose**: Clean session handoff

**Create `.claude/commands/land.md`**:

```markdown
# Land: Session End Cleanup

Cleanly end work session with Beads status update and context for next session.

## Usage

/land

## What This Does

1. **Review active work**: Show tasks currently marked active
2. **Update status**: Prompt to mark completed tasks as done
3. **File discoveries**: Capture any new tasks discovered during session
4. **Prepare handoff**: Show what's ready for next session

## Step-by-Step

### 1. Review Active Tasks

```bash
bd list --active
```

For each active task:
- Was it completed? → `bd done <id>`
- Still in progress? → Add notes: `bd edit <id>` (explain where you left off)
- Blocked? → File blocker as new task with dependency

### 2. File Discoveries

Did you discover new work during this session?
```bash
bd create "Discovered: add error handling to X"
bd dep add <new-id> <current-id>  # Set dependency
```

### 3. Show Next Session Context

```bash
bd ready              # What's available to work on?
bd list --active      # What's still in progress?
```

### 4. Summary Output

Output summary for user:
```
📋 Session Summary

Completed this session:
  ✓ Task 1: Install and Initialize Beads
  ✓ Task 2: Manual Beads Experience

Still in progress:
  ⏳ Task 4: Bridge Command Implementation
     Note: Completed parsing logic, need dependency setup

Discovered work filed:
  • Task 10: Add error handling for missing epic README

Ready for next session:
  → Task 3: Create AGENTS.md (now unblocked)
  → Task 5: Workflow Integration Commands

Blocked:
  🚫 Task 6: Multi-session test (depends on Task 5)
```
```

### 3. Create `/beads-status` Command

**Purpose**: Quick project visibility

**Create `.claude/commands/beads-status.md`**:

```markdown
# Beads Status: Project Overview

Show high-level project status via Beads task graph.

## Usage

/beads-status

## What This Shows

- Tasks by status (pending, active, done)
- Progress metrics (X of Y complete)
- Current bottlenecks (tasks blocking many others)
- Next available work

## Implementation

```bash
# Summary counts
echo "📊 Project Status"
echo ""
echo "Completed: $(bd list --done | wc -l) tasks"
echo "Active: $(bd list --active | wc -l) tasks"
echo "Ready: $(bd ready | wc -l) tasks"
echo "Pending: $(bd list | grep pending | wc -l) tasks"
echo ""

# Active work
echo "🔨 Currently Active:"
bd list --active

# Next steps
echo ""
echo "➡️  Ready to Work On:"
bd ready

# Recently completed
echo ""
echo "✅ Recently Completed:"
bd list --done | tail -5
```

Output example:
```
📊 Project Status

Completed: 2 tasks
Active: 1 task
Ready: 2 tasks
Pending: 4 tasks

🔨 Currently Active:
  4. Feature: Bridge Command Implementation

➡️  Ready to Work On:
  3. Chore: Create AGENTS.md
  5. Feature: Workflow Integration Commands

✅ Recently Completed:
  1. Chore: Install and Initialize Beads
  2. Chore: Manual Beads Experience
```
```

### 4. Update AGENTS.md

**Add integration commands** to AGENTS.md:

```markdown
### Workflow Integration Commands

**`/implement`**: Now Beads-aware
- Checks `bd ready` before implementing
- Marks tasks active during work
- Marks tasks done upon completion
- Gracefully degrades if Beads not available

**`/land`**: End-of-session cleanup
- Review and update active task status
- File discovered work
- Prepare context for next session
- Use at end of every work session

**`/beads-status`**: Project overview
- Quick visibility into task graph
- Shows what's done, active, ready, blocked
- Use to get oriented or check progress
```

### 5. Test Integration

**Test `/implement` modification**:
```bash
# Mark task 3 ready (deps complete)
bd done 1
bd done 2

# Try implementing task 3
/implement specs/epic-beads-integration/chore-create-agents-md.md

# Verify agent checks bd ready and starts task
bd list --active  # Should show task 3
```

**Test `/land` command**:
```bash
# After some work session
/land

# Verify produces summary and updates status
bd list --active  # Should be clean
```

**Test `/beads-status` command**:
```bash
/beads-status

# Verify shows clear project overview
```

### 6. Run Validation Commands

```bash
# Verify command files exist
ls -la .claude/commands/implement.md
ls -la .claude/commands/land.md
ls -la .claude/commands/beads-status.md

# Test beads-status (should work if tasks exist)
/beads-status | grep "Project Status"

# Test graceful degradation (rename .beads temporarily)
mv .beads .beads-backup
/implement specs/some-spec.md  # Should work without Beads
mv .beads-backup .beads

# Verify AGENTS.md updated
grep "/land" AGENTS.md
grep "/beads-status" AGENTS.md
```

## Acceptance Criteria

- [ ] `/implement` checks `bd ready` before implementing (if Beads available)
- [ ] `/implement` marks tasks active during work, done after completion
- [ ] `/implement` gracefully degrades without Beads (no errors)
- [ ] `/land` command reviews active tasks and updates status
- [ ] `/land` prompts for discovered work to be filed
- [ ] `/land` outputs summary with next session context
- [ ] `/beads-status` shows project overview (done/active/ready/blocked counts)
- [ ] `/beads-status` displays currently active and ready tasks
- [ ] AGENTS.md documents all three integration commands
- [ ] All commands tested and working

## Validation Commands

```bash
# Verify command files
cat .claude/commands/implement.md | grep "bd ready"
cat .claude/commands/land.md | grep "Session End"
cat .claude/commands/beads-status.md | grep "Project Overview"

# Test beads-status
/beads-status

# Verify output includes status counts
/beads-status | grep -E "(Completed|Active|Ready|Pending):"

# Test land command
/land

# Verify land produces summary
/land | grep "Session Summary"

# Verify AGENTS.md updated
grep -c "Workflow Integration Commands" AGENTS.md  # Should be 1

# Test graceful degradation
rm -rf .beads
/beads-status  # Should handle missing Beads gracefully
/implement some-spec.md  # Should work without Beads
bd init  # Restore Beads
```

## Notes

**Design philosophy**:
- Make Beads usage automatic, not manual
- Preserve backward compatibility (work without Beads)
- Clear visibility (status command for quick checks)
- Clean handoffs (land command for session end)

**Implementation strategy**:
- Start with simple integration (check, start, done)
- Can enhance over time (auto-filing discoveries, smarter matching)
- Keep commands simple and focused

**Graceful degradation details**:
```bash
# Check Beads availability
if [ -d ".beads" ]; then
    bd ready
else
    # Proceed without Beads
    echo "Beads not initialized. Proceeding without task tracking."
fi
```

**Future enhancements**:
- `/implement` could auto-detect matching task (fuzzy match on spec name)
- `/land` could auto-commit with references to completed Beads IDs
- `/beads-status` could show critical path (longest dependency chain)
- Integration with `/act` for voice memo → Beads task creation

**Testing tips**:
- Test with Beads present (normal case)
- Test without Beads (graceful degradation)
- Test with tasks in various states (pending, active, done, blocked)
- Test session continuity (land → new session → bd ready works)
