# Chore: Planning Commands

## Description

Create the planning command templates: aura.epic, aura.feature, aura.tickets. These enable the workflow from idea → structured plan → beads tasks.

## Tasks

### 1. Create aura.epic.md

Copy and adapt from `whisper/.claude/commands/epic.md`:

**Location**: `aura/src/aura/templates/claude/aura.epic.md`

Key changes:
- Remove references to brain/ (aura doesn't include brain system)
- Update output path to `specs/epic-*/`
- Simplify to focus on epic creation without vision references

### 2. Create aura.feature.md

Copy and adapt from `whisper/.claude/commands/feature.md`:

**Location**: `aura/src/aura/templates/claude/aura.feature.md`

Key changes:
- Remove brain/ references
- Output to `specs/<feature-name>.md`
- Keep the plan format structure

### 3. Create aura.tickets.md

New command based on `whisper/.claude/commands/beads-from-epic.md`:

**Location**: `aura/src/aura/templates/claude/aura.tickets.md`

Key functionality:
- Parse epic README.md
- Extract phases and specs
- Create beads tasks via `bd create`
- Set up dependencies between tasks

## Template Content Outline

### aura.tickets.md Structure

```markdown
# Convert Epic to Beads Tickets

Parse an epic document and create beads tasks with dependencies.

## Usage

```
/aura.tickets <epic-directory>
```

## Instructions

1. Read the epic README at `$ARGUMENTS/README.md`
2. Extract phases and specs
3. For each spec, create a beads task:
   ```bash
   bd create "Phase N: Spec Title" --description "..."
   ```
4. Set up dependencies between tasks
5. Report summary of created tasks

## Example

```
/aura.tickets specs/epic-player-movement
```
```

## Acceptance Criteria

- [ ] `aura/src/aura/templates/claude/aura.epic.md` exists
- [ ] `aura/src/aura/templates/claude/aura.feature.md` exists
- [ ] `aura/src/aura/templates/claude/aura.tickets.md` exists
- [ ] aura.tickets.md integrates with beads CLI (`bd create`)
- [ ] After `aura init`, all three commands available in Claude Code

## Notes

- aura.epic is the main planning entry point
- aura.feature is for smaller, single-feature work
- aura.tickets bridges planning to execution via beads
