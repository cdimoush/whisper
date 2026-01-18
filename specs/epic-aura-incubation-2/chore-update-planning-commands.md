# Chore: Update Planning Commands

## Description

Review and update planning commands (`aura.epic.md`, `aura.feature.md`, `aura.tickets.md`) to use correct paths and remove any whisper-specific references.

## Files to Review

### 1. aura.epic.md

**Location**: `aura/src/aura/templates/claude/aura.epic.md`

**Check for**:
- References to `brain/` (remove - aura doesn't have brain system)
- Output path should be `specs/epic-<name>/README.md`
- No whisper-specific file references

### 2. aura.feature.md

**Location**: `aura/src/aura/templates/claude/aura.feature.md`

**Check for**:
- Output path should be `specs/<feature-name>.md`
- Template should be self-contained
- No references to whisper's structure

### 3. aura.tickets.md

**Location**: `aura/src/aura/templates/claude/aura.tickets.md`

**Check for**:
- Correctly calls `bd create` for beads
- Parses epic README structure
- Sets up dependencies correctly

## Changes to Make

### Remove Brain References

Replace patterns like:
```markdown
- Read brain/active_projects.md first
- Check brain/technical_systems.md
```

With:
```markdown
- Read CLAUDE.md for project context
- Check README.md for project overview
```

### Standardize Output Paths

All planning outputs go to `specs/`:
```
specs/
├── epic-<name>/
│   └── README.md
├── <feature-name>.md
└── ...
```

## Acceptance Criteria

- [ ] No `brain/` references in any planning command
- [ ] All output paths are relative to repo root
- [ ] Commands are self-contained
- [ ] Epic structure matches what aura.tickets expects

## Notes

- Planning commands don't need scripts - they're pure prompt/template
- Main concern is removing whisper-specific paths and patterns
