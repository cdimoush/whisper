# Feature: Sample Workflow Definition

## Feature Description

Define the exact test scenario for validating Aura: what "voice transcript" to use, what epic should be generated, what tickets should be created, and what implementation should result.

## User Story

As an Aura developer
I want a documented test scenario
So that I can validate the full workflow works correctly

## Problem

Without a defined test scenario, validation is subjective. We need concrete inputs and expected outputs.

## Solution

Create sample artifacts that define:
1. A written "transcript" (simulating voice input)
2. Expected epic structure
3. Expected beads tickets
4. Expected implementation changes

## Relevant Files

### New Files
- `aura/tests/tron/examples/sample_transcript.txt` - Simulated voice input
- `aura/tests/tron/examples/expected_epic.md` - What epic should look like
- `aura/tests/tron/examples/expected_tickets.md` - What beads tasks should exist

## The Test Scenario

### Input: Sample Transcript

**File**: `aura/tests/tron/examples/sample_transcript.txt`

```
I want to add player movement to the tron game. The player should be able
to use arrow keys to control the light bike. When you press up, the bike
goes up. Down goes down. Left and right work the same way.

The bike should leave a trail behind it as it moves. The trail should be
a different color from the bike itself.

For now, don't worry about collision detection or game over - just get
the movement and trail working.

Actually, let's break this into two parts: first just get movement working,
then add the trail as a second phase.
```

### Expected: Epic Structure

**File**: `aura/tests/tron/examples/expected_epic.md`

```markdown
# Epic: Player Movement

## Overview
Add arrow key controls and trail rendering to the tron light bike.

## Phases

### Phase 1: Basic Movement
- Player can control bike with arrow keys
- Bike moves in the pressed direction

### Phase 2: Trail Rendering
- Bike leaves a trail as it moves
- Trail is visually distinct from bike

## Out of Scope
- Collision detection
- Game over logic
```

### Expected: Beads Tickets

**File**: `aura/tests/tron/examples/expected_tickets.md`

```markdown
# Expected Beads Tasks

After running `/aura.tickets`, these tasks should exist:

## Task 1: Create Player Class
- ID: tron-001 (or similar)
- Description: Create a Player class with position and direction
- Status: open
- Dependencies: none

## Task 2: Add Keyboard Input Handling
- ID: tron-002
- Description: Capture arrow key presses and update player direction
- Status: open
- Dependencies: tron-001

## Task 3: Implement Movement Loop
- ID: tron-003
- Description: Update player position based on direction each frame
- Status: open
- Dependencies: tron-002

## Task 4: Create Trail Class
- ID: tron-004
- Description: Create a Trail class to store previous positions
- Status: open
- Dependencies: tron-003

## Task 5: Render Trail
- ID: tron-005
- Description: Draw trail segments on screen as bike moves
- Status: open
- Dependencies: tron-004
```

### Expected: Implementation Result

After implementing tickets tron-001 through tron-003:

```
aura/tests/tron/
├── src/
│   └── tron/
│       ├── __init__.py
│       ├── player.py      # NEW: Player class
│       ├── input.py       # NEW: Keyboard handling
│       └── game.py        # NEW: Game loop
└── ...
```

## Acceptance Criteria

- [ ] `sample_transcript.txt` exists with test input
- [ ] `expected_epic.md` documents expected epic structure
- [ ] `expected_tickets.md` lists expected beads tasks
- [ ] Test scenario is realistic and achievable
- [ ] Documentation clear enough for another developer to validate

## Validation Steps

During Phase 4 (end-to-end test):

1. **Compare Epic**: Does `/aura.epic` with sample_transcript produce something similar to expected_epic.md?
2. **Compare Tickets**: Does `/aura.tickets` create tasks matching expected_tickets.md?
3. **Check Implementation**: Does `/aura.implement` on first few tickets create reasonable code?

## Notes

- "Expected" files are guides, not exact matches required
- Focus on structure and flow, not exact wording
- The test proves the workflow works, not that output is perfect
- Human judgment required for final validation
