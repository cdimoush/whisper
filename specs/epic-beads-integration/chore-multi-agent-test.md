# Chore: Multi-Agent Coordination Test

## Overview

Test whether multiple agents can coordinate via shared Beads memory by running `/process_queue` with parallel agents accessing the same task graph. This validates that Beads solves multi-agent coordination problems: agents seeing each other's work, avoiding conflicts, and respecting task ownership and dependencies.

## Context

**Why this matters**: Single-agent memory is valuable, but multi-agent coordination is where Beads could become transformative. If parallel agents can safely work on different tasks without conflicts, we can process voice memos in parallel, work on multiple features simultaneously, and truly scale agent capabilities.

**Current state**: Beads tested for single-agent continuity but not multi-agent coordination.

**Desired state**: Evidence that multiple agents can work concurrently using shared Beads task graph without conflicts, confusion, or duplicate work.

## Tasks

### 1. Set Up Multi-Task Scenario

**Create realistic parallel work**:
```bash
bd create "Process voice memo 1"
bd create "Process voice memo 2"
bd create "Process voice memo 3"
```

**No dependencies** (all can run in parallel):
```bash
bd ready  # Should show all 3 tasks
```

**Alternative**: Use real queued voice memos if available

### 2. Test Parallel Agent Execution

**Option A: Use `/process_queue`** (if implemented):
```bash
# Ensure queue has 3+ audio files
ls queue/*.m4a

# Process with parallel agents
/process_queue
```

Agents should naturally use Beads if configured.

**Option B: Manually spawn agents**:
```bash
# Terminal 1
bd start 1
# ... agent works on task 1 ...

# Terminal 2 (simultaneously)
bd start 2
# ... agent works on task 2 ...

# Terminal 3 (simultaneously)
bd start 3
# ... agent works on task 3 ...
```

### 3. Monitor Coordination

**Watch for**:

**✅ Good coordination indicators**:
- Each agent works on different task
- No two agents start same task
- Agents see each other's active status
- Tasks marked active by one agent don't appear in other's `bd ready`

**❌ Coordination failures**:
- Two agents start same task (conflict)
- Agent doesn't see other's active status
- Race conditions in status updates
- JSONL merge conflicts

**Check during execution**:
```bash
# In separate terminal
watch -n 2 'bd list --active'  # See who's working on what
```

### 4. Test Dependency Coordination

**Create dependent tasks**:
```bash
bd create "Task A (foundation)"
bd create "Task B (depends on A)"
bd create "Task C (depends on A)"
bd dep add 2 1  # B depends on A
bd dep add 3 1  # C depends on A
```

**Spawn agents on different tasks**:
- Agent 1: Works on Task A
- Agent 2: Tries to work on Task B (should be blocked)
- Agent 3: Tries to work on Task C (should be blocked)

**Expected behavior**:
- Agents 2 & 3 see tasks blocked
- When Agent 1 completes A: `bd done 1`
- Agents 2 & 3 now see B & C as ready
- Both can work in parallel (no deps between B & C)

### 5. Test Discovery Filing by Multiple Agents

**Scenario**: Two agents discover subtasks while working

**Agent 1**:
```bash
bd start 1
# During work, discovers subtask
bd create "Subtask discovered by Agent 1"
bd dep add 4 1  # Block on current work
```

**Agent 2**:
```bash
bd start 2
# During work, discovers subtask
bd create "Subtask discovered by Agent 2"
bd dep add 5 2  # Block on current work
```

**Verify**:
```bash
bd list  # Both new tasks visible
bd show 4  # Depends on task 1
bd show 5  # Depends on task 2
```

**No conflicts**: Each agent's discoveries tracked separately

### 6. Test JSONL Sync and Merges

**Simulate distributed work**:
- Make changes on "machine A" (or git branch A)
- Make changes on "machine B" (or git branch B)
- Merge and verify no corruption

**Process**:
```bash
# Branch A
git checkout -b test-agent-a
bd create "Task from Agent A"
git add .beads/issues.jsonl
git commit -m "Agent A work"

# Branch B
git checkout -b test-agent-b
bd create "Task from Agent B"
git add .beads/issues.jsonl
git commit -m "Agent B work"

# Merge
git checkout main
git merge test-agent-a
git merge test-agent-b  # Should merge cleanly (JSONL is append-only)

# Verify
bd list  # Should show both tasks
```

### 7. Document Coordination Findings

Create `multi-agent-test-findings.md`:

```markdown
# Multi-Agent Coordination Test Findings

## Test Setup
- Number of agents: X
- Tasks tested: Y
- Dependencies tested: Yes/No

## Coordination Results

### Task Distribution
✅/❌ Agents worked on different tasks (no conflicts)
✅/❌ Agents saw each other's active status
✅/❌ `bd ready` correctly showed only available tasks

### Dependency Enforcement
✅/❌ Blocked tasks not visible to agents
✅/❌ Unblocking worked correctly (task A done → B & C ready)
✅/❌ Parallel work on non-dependent tasks succeeded

### Discovery Filing
✅/❌ Multiple agents filed discoveries without conflicts
✅/❌ Discoveries visible to all agents
✅/❌ Dependency relationships preserved

### Git Sync
✅/❌ JSONL merged cleanly across branches
✅/❌ No data corruption or lost tasks
✅/❌ Beads DB rebuilt correctly from merged JSONL

## Issues Encountered
[Specific problems, race conditions, conflicts]

## Performance
- Time for X agents to complete Y tasks: Z minutes
- Comparison to sequential: estimated A minutes
- Speedup: B%

## Recommendation
[Proceed to Phase 4 / Needs fixes / Major blocker]
```

## Acceptance Criteria

- [ ] Multiple agents successfully worked on different tasks concurrently
- [ ] No task conflicts (two agents on same task)
- [ ] Dependency blocking enforced across agents
- [ ] Discoveries filed by multiple agents without conflicts
- [ ] JSONL merged cleanly in git (no corruption)
- [ ] Beads DB rebuilt correctly after merge
- [ ] Documented findings with evidence of coordination success/failure

## Testing

**Coordination validation**:
1. Spawn 2-3 agents on ready tasks
2. Verify each takes different task
3. Check `bd list --active` shows all agents' work
4. Complete tasks and verify unblocking

**Conflict testing**:
1. Try to start same task from two terminals (should one fail?)
2. Test rapid status updates (race conditions?)
3. Test merge conflicts (should be rare/none with append-only JSONL)

## Dependencies

**Requires**:
- [Chore: Multi-Session Feature Test](./chore-multi-session-test.md) - Validate single-agent first

**Blocks**:
- [Chore: Assessment and Decision](./chore-assessment-decision.md) - Need multi-agent results for decision

## Estimated Effort

**Time**: 2-3 hours

**Breakdown**:
- Setup multi-task scenario: 15 minutes
- Parallel execution testing: 60 minutes
- Dependency coordination testing: 30 minutes
- Git sync testing: 15 minutes
- Documentation: 30 minutes

## Implementation Notes

**Real parallelism**:
- Use actual `/process_queue` if available
- Or manually spawn agents in separate terminals
- Authentic concurrent access is key

**What success looks like**:
- Agents naturally partition work
- No manual coordination needed
- Faster than sequential processing
- No conflicts or lost work

**What failure looks like**:
- Agents fight over same task
- Race conditions in status updates
- JSONL corruption
- Agents don't see each other's work

## Success Metrics

- Multiple agents successfully completed parallel work without conflicts
- Dependency blocking worked across agents
- Git sync worked correctly
- Clear speedup vs sequential execution

## Tags

`chore` `testing` `multi-agent` `coordination` `parallel` `phase-3` `distributed`
