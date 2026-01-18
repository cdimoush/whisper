# Epic: Aura Incubation Phase 3 - Dogfooding Refactor

## The Problem

Aura can't use itself. The current structure puts all commands inside `src/aura/templates/`, which means:

1. **No `.claude/commands/` at aura repo root** → Can't use `/aura.act`, `/aura.epic`, etc. while developing aura
2. **No `.aura/scripts/` at aura repo root** → Can't test transcription without targeting another repo
3. **We've been freeloading on whisper** → All our "easy" development used whisper's commands, not aura's

This is backwards. An agentic framework should be developed using itself.

## Current (Broken) Structure

```
aura/
├── src/aura/
│   ├── templates/
│   │   ├── aura/           ← Templates (not usable by aura itself)
│   │   │   ├── scripts/
│   │   │   └── .gitignore
│   │   └── claude/         ← Templates (not usable by aura itself)
│   │       ├── aura.*.md
│   │       └── beads.*.md
│   ├── cli.py
│   └── init.py
├── tests/tron/             ← Test fixture (has .aura/, .claude/)
├── pyproject.toml
└── README.md
                            ← NO .aura/ here!
                            ← NO .claude/commands/ here!
```

**Result**: Developing aura requires using whisper's commands or manually running scripts.

## Target Structure

```
aura/
├── .aura/                  ← WORKING copy (dogfood!)
│   ├── scripts/
│   │   ├── transcribe.py
│   │   ├── generate_title.py
│   │   └── requirements.txt
│   ├── queue/              ← gitignored
│   ├── output/             ← gitignored
│   └── .gitignore
├── .claude/
│   └── commands/           ← WORKING copy (dogfood!)
│       ├── aura.act.md
│       ├── aura.epic.md
│       ├── aura.feature.md
│       ├── aura.implement.md
│       ├── aura.prime.md
│       ├── aura.record.md
│       ├── aura.tickets.md
│       ├── aura.transcribe.md
│       ├── beads.done.md
│       ├── beads.ready.md
│       ├── beads.start.md
│       └── beads.status.md
├── .beads/                 ← Task tracking for aura development
├── src/aura/
│   ├── cli.py
│   └── init.py             ← Copies FROM .aura/ and .claude/ TO target repos
├── tests/tron/
├── pyproject.toml
├── README.md
└── CLAUDE.md
```

**Key insight**: The "templates" ARE the working copies. `aura init` copies from aura's own `.aura/` and `.claude/` to target repos.

## Benefits of New Structure

1. **Dogfooding**: Develop aura using aura's own commands
2. **Single source of truth**: No template drift - what we use is what gets copied
3. **Faster iteration**: Test command changes immediately, not via tron fixture
4. **Self-documenting**: Aura's own repo demonstrates the expected structure
5. **Natural testing**: If it works for aura development, it works for users

## Specs in This Epic

### Phase 1: Structure Migration
- [ ] [Chore: Move Templates to Root](./chore-move-templates.md) - Move templates from src/ to repo root
- [ ] [Chore: Update Init Logic](./chore-update-init.md) - Change init.py to copy from root dirs

### Phase 2: Path Fixes
- [ ] [Chore: Fix Template Paths](./chore-fix-paths.md) - Update any hardcoded paths in commands
- [ ] [Chore: Update gitignore](./chore-update-gitignore.md) - Root .gitignore for queue/output

### Phase 3: Validation
- [ ] [Chore: Dogfood Test](./chore-dogfood-test.md) - Verify aura commands work in aura repo
- [ ] [Chore: Tron Re-test](./chore-tron-retest.md) - Verify init still works for target repos

### Phase 4: Cleanup
- [ ] [Chore: Remove Old Templates](./chore-remove-old.md) - Delete src/aura/templates/
- [ ] [Chore: Update Docs](./chore-update-docs.md) - Update README and CLAUDE.md

## Execution Order

### Phase 1: Structure Migration (~20 minutes)
**Goal**: `.aura/` and `.claude/commands/` exist at aura repo root

Execute in order:
1. [Chore: Move Templates to Root](./chore-move-templates.md)
2. [Chore: Update Init Logic](./chore-update-init.md)

**Success Criteria**:
- `.aura/scripts/transcribe.py` exists at aura root
- `.claude/commands/aura.act.md` exists at aura root
- `init.py` references new locations

**🔄 USER BREAKPOINT #1**: Verify files moved correctly

---

### Phase 2: Path Fixes (~15 minutes)
**Goal**: All paths resolve correctly

Execute in order:
1. [Chore: Fix Template Paths](./chore-fix-paths.md)
2. [Chore: Update gitignore](./chore-update-gitignore.md)

**Success Criteria**:
- Commands reference `.aura/scripts/` (unchanged, already correct)
- Root `.gitignore` ignores `.aura/queue/`, `.aura/output/`

**🔄 USER BREAKPOINT #2**: Verify no broken paths

---

### Phase 3: Validation (~20 minutes)
**Goal**: Both dogfooding and init work

Execute in parallel:
1. [Chore: Dogfood Test](./chore-dogfood-test.md)
2. [Chore: Tron Re-test](./chore-tron-retest.md)

**Success Criteria**:
- `/aura.transcribe` works from aura repo root
- `aura init` in tron creates correct structure
- Commands in tron reference `.aura/scripts/`

**🔄 USER BREAKPOINT #3**: Manually test a voice memo workflow

---

### Phase 4: Cleanup (~10 minutes)
**Goal**: Remove old structure, update docs

Execute in order:
1. [Chore: Remove Old Templates](./chore-remove-old.md)
2. [Chore: Update Docs](./chore-update-docs.md)

**Success Criteria**:
- `src/aura/templates/` directory deleted
- README reflects new structure
- CLAUDE.md updated

**🔄 USER BREAKPOINT #4**: Final review before extraction

---

## Path Dependencies Diagram

```
Phase 1: Migration
├── chore-move-templates ─────┐
└── chore-update-init ────────┤
                              ▼
Phase 2: Path Fixes
├── chore-fix-paths
└── chore-update-gitignore
        │
        ▼
Phase 3: Validation (parallel)
├── chore-dogfood-test
└── chore-tron-retest
        │
        ▼
Phase 4: Cleanup
├── chore-remove-old
└── chore-update-docs

Critical Path:
move-templates → update-init → dogfood-test → remove-old
```

## Implementation Notes

### Init.py Changes

**Before** (broken):
```python
TEMPLATES = Path(__file__).parent / "templates"

# .aura/ templates
aura_templates = TEMPLATES / "aura"

# .claude/commands/ templates
claude_templates = TEMPLATES / "claude"
```

**After** (dogfood-friendly):
```python
# Find aura package root (where .aura/ and .claude/ live)
AURA_ROOT = Path(__file__).parent.parent.parent.parent  # src/aura/init.py → aura/

# Copy from aura's own directories
aura_source = AURA_ROOT / ".aura"
claude_source = AURA_ROOT / ".claude" / "commands"
```

### What Gets Copied

| Source (aura repo) | Destination (target repo) |
|--------------------|---------------------------|
| `.aura/scripts/*` | `.aura/scripts/*` |
| `.aura/.gitignore` | `.aura/.gitignore` |
| `.aura/.env.example` | `.aura/.env.example` |
| `.claude/commands/*.md` | `.claude/commands/*.md` |

### What Doesn't Get Copied

- `.aura/queue/` - User's queue, not template
- `.aura/output/` - User's output, not template
- `.beads/` - Initialized fresh via `bd init`

## Risk Mitigation

### Risk: Breaking init for existing users
**Mitigation**: Test thoroughly in tron before removing old templates

### Risk: Path resolution issues in installed package
**Mitigation**: Use `importlib.resources` or similar for robust path finding

### Risk: Accidental commit of queue/output
**Mitigation**: Root .gitignore covers `.aura/queue/`, `.aura/output/`

## Success Metrics

- [ ] Can run `/aura.transcribe` from aura repo root
- [ ] Can run `/aura.act` from aura repo root
- [ ] Can run `/aura.epic` from aura repo root
- [ ] `aura init` in fresh directory creates working structure
- [ ] `src/aura/templates/` no longer exists
- [ ] Aura development no longer requires whisper

## Why This Matters

Every agentic framework should be developed using itself. If we can't build aura with aura, we're:

1. **Missing bugs** - We don't feel the pain our users will feel
2. **Slowing iteration** - Context switching to whisper adds friction
3. **Lying to ourselves** - "It works" means nothing if we don't use it

After this epic, aura development happens with aura. Full circle.

## Relation to Previous Epics

- **epic-aura-incubation-1**: Built scaffolding (CLI, templates, tron) ✅
- **epic-aura-incubation-2**: Added scripts, docs ✅
- **epic-aura-incubation-3**: Enable dogfooding (this epic)
- **epic-aura-incubation-4** (future): Extract to standalone repo
