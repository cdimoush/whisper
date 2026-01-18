# Feature: Beads Test Workflow

## Feature Description

Execute the full end-to-end test of Aura using beads for task tracking. This is the validation that proves Aura works.

## User Story

As an Aura developer
I want to test the full workflow on the tron fixture
So that I can validate Aura is ready for extraction

## Problem

We've built all the components but haven't proven they work together.

## Solution

Execute a scripted test workflow on a separate git branch, using beads to track progress, and document the results.

## Git Branching for Test

**CRITICAL**: Test implementation must happen on a separate branch to avoid polluting Aura code.

```bash
# Ensure we're on aura-incubation branch with all aura code
git checkout aura-incubation

# Create test branch
git checkout -b aura-tron-test

# All test work happens here
# This branch can be deleted after validation
```

## Step-by-Step Test Execution

### Step 0: Prepare Test Environment

```bash
# From whisper root, on aura-tron-test branch
cd aura/tests/tron

# Verify tron fixture exists
ls -la
# Should see: README.md, pyproject.toml, src/

# Verify aura CLI works
cd ../../..  # back to aura/
python -m aura.cli --version
```

### Step 1: Initialize Aura in Tron

```bash
cd aura/tests/tron
python -m aura.cli init
```

**Expected output**:
```
Initializing Aura...

  Created .aura/
  Created .aura/config.md
  Created .claude/commands/aura.record.md
  Created .claude/commands/aura.act.md
  ... (all 12 commands)
  Initialized beads task tracking

Aura initialized! Run /aura.prime in Claude Code to get started.
```

**Verify**:
```bash
ls -la .aura/
ls -la .claude/commands/
ls -la .beads/
```

**Git checkpoint**:
```bash
git add -A
git commit -m "tron: initialize aura"
```

### Step 2: Create Epic from Transcript

Open Claude Code in `aura/tests/tron/` directory.

```
/aura.epic Add player movement - arrow keys control light bike, leaves trail behind. Phase 1: movement only. Phase 2: trail rendering. Skip collision detection for now.
```

**Expected**: Creates `specs/epic-player-movement/README.md` with:
- Overview of the feature
- Phase 1: Basic Movement
- Phase 2: Trail Rendering
- Clear scope boundaries

**Verify**:
```bash
cat specs/epic-player-movement/README.md
```

**Git checkpoint**:
```bash
git add -A
git commit -m "tron: create player movement epic"
```

### Step 3: Convert Epic to Beads Tickets

```
/aura.tickets specs/epic-player-movement/
```

**Expected**: Creates beads tasks like:
- tron-001: Create Player class
- tron-002: Add keyboard input
- tron-003: Implement movement loop
- tron-004: Create Trail class
- tron-005: Render trail

**Verify with beads commands**:
```
/beads.status
/beads.ready
```

**Git checkpoint**:
```bash
git add -A
git commit -m "tron: create beads tickets from epic"
```

### Step 4: Work Through Tickets

**Start first ticket**:
```
/beads.ready
/beads.start tron-001
```

**Implement first ticket**:
```
/aura.implement tron-001
```

Follow the implementation plan, create `src/tron/player.py`.

**Complete first ticket**:
```
/beads.done tron-001
```

**Git checkpoint**:
```bash
git add -A
git commit -m "tron: implement player class (tron-001)"
```

**Repeat for ticket tron-002**:
```
/beads.ready
/beads.start tron-002
/aura.implement tron-002
/beads.done tron-002
```

```bash
git add -A
git commit -m "tron: implement keyboard input (tron-002)"
```

### Step 5: Validate Results

**Check beads progress**:
```
/beads.status
```

Expected:
```
📊 Beads Project Status

Progress: 2 of 5 tasks complete (40%)

┌─────────────────────────────────────────┐
│ Status Breakdown                        │
├─────────────────────────────────────────┤
│ ✓ Completed:    2 tasks                 │
│ ◐ In Progress:  0 tasks                 │
│ ○ Open:         3 tasks                 │
└─────────────────────────────────────────┘
```

**Check created files**:
```bash
ls -la src/tron/
# Should see: __init__.py, player.py, input.py (or similar)
```

**Validate the workflow completed**:
- [ ] aura init created all directories and commands
- [ ] Epic was created with clear phases
- [ ] Tickets were created in beads with dependencies
- [ ] At least 2 tickets were implemented
- [ ] Beads tracking shows correct progress
- [ ] All commands worked without errors

### Step 6: Document Results

Create `aura/tests/tron/TEST_RESULTS.md`:

```markdown
# Aura Test Results

**Date**: [DATE]
**Branch**: aura-tron-test
**Tester**: [NAME]

## Summary

[PASS/FAIL] - Full workflow completed successfully

## Step Results

| Step | Command | Result | Notes |
|------|---------|--------|-------|
| 1 | aura init | PASS | All 12 commands created |
| 2 | /aura.epic | PASS | Epic created with phases |
| 3 | /aura.tickets | PASS | 5 tickets created |
| 4a | /aura.implement tron-001 | PASS | Player class created |
| 4b | /aura.implement tron-002 | PASS | Input handling added |
| 5 | /beads.status | PASS | Shows 2/5 complete |

## Issues Found

- [List any bugs or issues]

## Recommendations

- [Ready for extraction / Needs more work]
```

**Final git checkpoint**:
```bash
git add -A
git commit -m "tron: document test results"
```

### Step 7: Clean Up

If test passed, the branch served its purpose:

```bash
# Return to aura development branch
git checkout aura-incubation

# Optionally delete test branch (or keep for reference)
# git branch -D aura-tron-test
```

**DO NOT merge aura-tron-test back** - it contains tron implementation, not aura code.

## Acceptance Criteria

- [ ] Test executed on separate `aura-tron-test` branch
- [ ] `aura init` successfully scaffolded tron project
- [ ] `/aura.epic` created structured epic document
- [ ] `/aura.tickets` created beads tasks with dependencies
- [ ] At least 2 tickets implemented via `/aura.implement`
- [ ] Beads tracking shows accurate progress
- [ ] Test results documented in TEST_RESULTS.md
- [ ] Aura-incubation branch not polluted with tron code

## Notes

- This is a human-in-the-loop test, not automated
- Focus on workflow validation, not perfect output
- Document any issues found for fixing before extraction
- Test branch is disposable - don't worry about code quality there
