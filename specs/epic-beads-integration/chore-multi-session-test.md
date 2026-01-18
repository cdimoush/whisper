# Chore: Multi-Session Feature Test

## Overview

Build one real Whisper feature using the full Beads workflow across 3+ work sessions to validate that Beads solves agent memory problems. This is the critical test: does an agent resuming work days later know exactly where to pick up? Do discovered subtasks get captured and not forgotten? This chore validates the core value proposition of Beads integration.

## Context

**Why this matters**: Manual testing and bridge commands are infrastructure. This tests the actual goal: agent session continuity and memory. If this fails, Beads doesn't solve our problem regardless of how well the tooling works.

**Current state**: Beads infrastructure exists, workflow commands implemented, but not tested across real multi-session work.

**Desired state**: Concrete evidence that agent can resume work across sessions without context loss, discovers and files subtasks without forgetting, and completes feature faster/better with Beads than without.

## Tasks

### 1. Choose Real Feature to Implement

**Criteria**:
- Non-trivial (takes 3+ sessions to complete)
- Real Whisper feature (not toy example)
- Has discoverable subtasks (not fully specified upfront)
- Can be scoped to complete within test timeframe

**Candidates**:
- Improve instant memo hotkey reliability
- Add tagging autocomplete to `/act` command
- Implement basic search across output/ directory
- Create `/memo-history` command to show recent memos

**Select one** and create spec if doesn't exist yet.

### 2. Set Up Initial Task in Beads

**Create primary task**:
```bash
bd create "Implement [chosen feature name]"
bd edit 1  # Add notes: spec location, goal, acceptance criteria
```

**Set context**:
- Link to spec file
- Note dependencies
- Set initial scope

### 3. Session 1: Initial Implementation

**Start session workflow**:
```bash
bd ready       # Verify task 1 is ready
bd start 1     # Mark as active
```

**Implement for 45-60 minutes**:
- Read spec and understand requirements
- Start implementation
- **Important**: When discovering subtasks, file them immediately:
  ```bash
  bd create "Add error handling for X"
  bd create "Write tests for Y"
  bd dep add <new-id> 1  # Block on main task
  ```

**End session**:
```bash
/land  # Review status, file discoveries, prepare handoff
```

**Don't mark task 1 done** - leave in-progress intentionally

**Document observations**:
- How easy was filing discoveries?
- Did `/land` capture state well?
- What context would be needed for resumption?

### 4. Session 2: Resume and Continue (24+ hours later)

**Start fresh session** (simulate real time gap):
```bash
bd ready               # "Where was I?"
bd list --active       # "What was I working on?"
bd show 1              # "What's the context?"
```

**Evaluate resumption**:
- Did you remember context?
- Were discoveries from Session 1 visible?
- Could you pick up without re-reading spec?
- Time to regain context vs without Beads?

**Continue implementation** (45-60 minutes):
- Work on main task or subtasks
- File new discoveries
- Update task notes if needed

**End session**:
```bash
/land  # Update status again
```

### 5. Session 3: Complete Feature

**Resume again** (another time gap):
```bash
bd ready
bd list --active
```

**Finish implementation**:
- Complete main task
- Verify all subtasks done
- Run tests/validation

**Mark complete**:
```bash
bd done 1              # Mark main task
bd list --done         # Verify completion
```

### 6. Evaluate Session Continuity

**Questions to answer**:

**Agent Memory**:
- [ ] Could agent resume without user re-explaining?
- [ ] Were discovered subtasks captured and accessible?
- [ ] Did `bd ready` show correct next work?
- [ ] Did `bd show` provide sufficient context?

**Workflow Speed**:
- [ ] Faster than reading epic spec each session?
- [ ] Filing discoveries felt valuable vs overhead?
- [ ] Status tracking helped vs hindered?

**Pain Points**:
- [ ] What was confusing or broken?
- [ ] What information was missing?
- [ ] What felt like unnecessary overhead?

**Evidence of Value**:
- [ ] Sessions 2 & 3 started faster than without Beads?
- [ ] No "forgot to do X" moments?
- [ ] Clear sense of progress throughout?

### 7. Document Findings

Create `multi-session-test-findings.md` in epic directory:

```markdown
# Multi-Session Test Findings

## Feature Tested
[Feature name and scope]

## Session Summary
- Session 1: [Date, duration, what was done]
- Session 2: [Date, duration, what was done]
- Session 3: [Date, duration, what was done]

## Beads Usage
- Tasks created: X
- Discoveries filed: Y
- Dependencies set: Z

## Agent Memory Validation
✅ **What worked well**:
- [Specific examples]

❌ **What didn't work**:
- [Specific problems]

## Speed Comparison
- Time to context (Session 2 start): X minutes with Beads vs Y minutes estimated without
- Total feature time: X hours
- Estimated without Beads: Y hours

## Recommendation
[Proceed to Phase 4 / Iterate / Stop]
```

## Acceptance Criteria

- [ ] Real Whisper feature implemented across 3+ sessions
- [ ] Beads workflow used throughout (ready, start, done, land)
- [ ] At least 2-3 discovered subtasks filed during implementation
- [ ] Agent successfully resumed work in Sessions 2 & 3 using Beads
- [ ] Documented findings with concrete examples
- [ ] Clear evidence whether Beads solved agent memory problem
- [ ] Recommendation on proceeding to Phase 4

## Testing

**Validation approach**:
- Compare session resumption with vs without Beads (estimate time/friction)
- Track discoveries filed vs discoveries forgotten
- Measure context regain time at session starts
- Evaluate completeness (did we ship everything intended?)

**Success indicators**:
- Session 2 & 3 start in <5 minutes (vs 10-15 min re-reading specs)
- Zero "forgot to do X" moments post-launch
- Clear audit trail of all work done

## Dependencies

**Requires**:
- [Feature: Workflow Integration Commands](./feature-workflow-integration.md) - Need /land and integrated /implement

**Blocks**:
- [Chore: Multi-Agent Coordination Test](./chore-multi-agent-test.md) - Validate single-agent first
- [Chore: Assessment and Decision](./chore-assessment-decision.md) - Need test results for decision

## Estimated Effort

**Time**: 4-6 hours (spread across multiple days)

**Breakdown**:
- Session 1: 60-90 minutes (setup + initial implementation)
- Session 2: 60-90 minutes (resume + continue)
- Session 3: 60-90 minutes (complete feature)
- Documentation: 30 minutes (findings and evaluation)

**Note**: Intentional time gaps between sessions (24+ hours) are part of test

## Implementation Notes

**Real feature, real timeline**:
- Don't rush to complete in one day
- Authentic time gaps test memory better
- Ship the feature (not just prototype)

**Honest evaluation**:
- Document what actually happened
- Include friction points and failures
- OK to conclude Beads didn't help if that's reality

**Comparison baseline**:
- Estimate how long/hard this would be without Beads
- Consider: time to regain context, forgotten work, rework

## Success Metrics

- Agent resumes work in <5 minutes (vs estimated 10-15 without Beads)
- Zero forgotten subtasks (all discoveries captured)
- Feature complete with all intended scope
- Clear recommendation supported by concrete evidence

## Tags

`chore` `testing` `validation` `multi-session` `agent-memory` `phase-3` `critical-test`
