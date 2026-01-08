# Feature: Vision and Epic Planning Commands

## Feature Description
Add two new slash commands (`/vision` and `/epic`) that extend the existing planning hierarchy. These commands turn big, visionary thinking into tangible plans with explicit paths and decision points. The `/vision` command creates high-level strategy documents with multiple implementation paths, while `/epic` breaks a chosen vision path into ordered specs (features and chores).

The planning hierarchy becomes:
```
/vision → vision-*.md (high-level strategy with paths)
    ↓
/epic → epic-*/README.md (ordered specs for a chosen path)
    ↓
/feature or /chore → specs/*.md (individual implementation plans)
    ↓
/implement → execute the plan
```

## User Story
As a developer
I want to turn big ideas into structured, actionable plans
So that I can systematically implement large features without losing sight of the bigger picture or getting stuck in analysis paralysis

## Problem
Currently, when starting a large initiative, developers must:
1. Keep high-level strategy in their head while writing individual feature specs
2. Manually track which features belong to which initiative
3. Lose context about alternative approaches that were considered
4. Jump straight from vague ideas to detailed implementation plans

This leads to:
- Inconsistent planning depth (some ideas get over-planned, others under-planned)
- Lost context about strategic decisions and trade-offs
- No clear progression from "vision" to "implementation"
- Difficulty communicating the "why" behind a set of related changes

## Solution
Create two new slash commands that formalize the visionary-to-tactical planning workflow:

1. **`/vision`**: Takes a loose prompt (and optionally linked context like URLs or files) and produces a `vision-*.md` document that:
   - Analyzes the current state and identifies gaps
   - Defines clear goals and success criteria
   - Proposes multiple implementation paths with trade-offs
   - Allows paths to be independent OR have shared/optional portions
   - Recommends an approach but leaves the decision to the user

2. **`/epic`**: Takes a vision document (or creates one inline) and produces an `epic-*/README.md` that:
   - References the source vision
   - Breaks the chosen path into ordered feature and chore specs
   - Defines execution order with dependencies
   - Includes user testing breakpoints
   - Tracks completion status

## Relevant Files

### Files to Modify
- None - this feature creates new files only

### New Files
- `.claude/commands/vision.md` - Slash command definition for `/vision`
- `.claude/commands/epic.md` - Slash command definition for `/epic`

## Step by Step Tasks

### Step 1: Create the /vision Command
Create the vision slash command that generates high-level strategy documents.

- Create `.claude/commands/vision.md` with:
  - Frontmatter with description and argument hints
  - Instructions for researching codebase context
  - Vision document format template including:
    - Vision statement
    - Current state analysis
    - Vision goals
    - Implementation paths (with effort/impact/risk/trade-offs for each)
    - Path comparison matrix
    - Recommended approach
    - Open questions
    - Future considerations
  - Guidance on presenting multiple paths (independent vs. shared portions)
  - Instruction to output as `specs/vision-<name>.md`

### Step 2: Create the /epic Command
Create the epic slash command that breaks a vision into ordered specs.

- Create `.claude/commands/epic.md` with:
  - Frontmatter with description and argument hints
  - Instructions for reading the source vision (if provided)
  - Epic document format template including:
    - Epic overview
    - Vision context (link to source vision, key points)
    - Specs in this epic (checklist of features and chores)
    - Execution order (with dependencies and user breakpoints)
    - Path dependencies diagram
    - Implementation notes (cross-cutting concerns)
    - Success metrics
    - Future enhancements (out of scope items)
  - Instruction to create `specs/epic-<name>/README.md` directory structure
  - Guidance on defining user testing breakpoints (🔄 markers)

### Step 3: Validate Commands Exist and Are Well-Formed
Run validation to ensure the commands are properly structured.

- Verify both command files exist with correct frontmatter
- Verify templates include all required sections
- Verify output paths match expected patterns

## Acceptance Criteria
- [ ] `/vision some idea` creates a `specs/vision-<name>.md` document
- [ ] Vision documents include multiple implementation paths with trade-offs
- [ ] Vision documents include a path comparison matrix
- [ ] Vision documents include a recommended approach section
- [ ] `/epic vision-doc.md` creates a `specs/epic-<name>/README.md` structure
- [ ] Epic documents reference their source vision
- [ ] Epic documents include ordered specs with dependencies
- [ ] Epic documents include user testing breakpoints (🔄)
- [ ] Both commands follow existing patterns from `/feature` and `/chore`
- [ ] Both commands include clear instructions for researching context

## Validation Commands
- `cat .claude/commands/vision.md` - Verify vision command content and format
- `cat .claude/commands/epic.md` - Verify epic command content and format
- `ls -la .claude/commands/` - Verify both files exist alongside feature.md and chore.md
- `head -10 .claude/commands/vision.md` - Verify frontmatter is present
- `head -10 .claude/commands/epic.md` - Verify frontmatter is present

## Notes
- The vision and epic documents in `specs/` serve as excellent examples of the format (see `specs/vision-frictionless-voice-memo-workflow.md` and `specs/epic-frictionless-voice-capture/README.md`)
- Paths in vision documents can be:
  - Completely independent (choose one)
  - Partially shared (common foundation with divergent approaches)
  - Sequential (path B depends on path A)
- User breakpoints (🔄) in epics are critical for preventing over-investment in the wrong direction
- The hierarchy is flexible: users can run `/feature` directly without going through `/vision` → `/epic` for smaller work
