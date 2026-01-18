# Chore: Install and Initialize Beads

## Overview

Install the `bd` CLI tool and initialize Beads in the Whisper project. This is foundational infrastructure—everything else in this epic depends on having Beads properly set up. The installation script handles cross-platform setup, and initialization creates the `.beads/` directory structure needed for task tracking.

## Context

**Why this matters**: Without Beads installed, we can't experience or test any of the agent memory features. This is table stakes for the entire epic.

**Current state**: No Beads infrastructure exists in Whisper project.

**Desired state**: `bd` CLI installed globally, `.beads/` directory initialized in project root, git configured to track JSONL files but ignore the local database.

## Tasks

### 1. Install bd CLI

**Steps**:
```bash
# Run official installation script
curl -fsSL https://raw.githubusercontent.com/steveyegge/beads/main/scripts/install.sh | bash

# Verify installation
bd --version
```

**Expected output**: Version number (e.g., `bd version 0.1.0`)

**Troubleshooting**:
- If `bd` not found after install, check if install directory is in PATH
- May need to restart shell or source profile (`.bashrc`, `.zshrc`)
- Installation script should handle macOS and Linux automatically

### 2. Initialize Beads in Whisper Project

**Steps**:
```bash
cd /Users/conner/dev/whisper
bd init
```

**Expected result**: Creates `.beads/` directory with initial structure

**What gets created**:
- `.beads/issues.jsonl` - Task storage (git-tracked)
- `.beads/beads.db` - Local SQLite cache (git-ignored)
- `.beads/config.json` - Configuration (git-tracked)

### 3. Configure Git Tracking

**Update `.gitignore`**:
```bash
# Add to .gitignore
echo ".beads/beads.db" >> .gitignore
```

**Rationale**:
- JSONL files should be committed (version-controlled tasks)
- DB file is local cache only (rebuilt from JSONL)
- This enables git-backed task synchronization across machines

**Verify**:
```bash
git status
# Should show .beads/ files except beads.db
```

### 4. Verify Installation

**Test basic commands**:
```bash
bd list              # Should show empty (no tasks yet)
bd create "test"     # Create test task
bd list              # Should show one task
bd show 1            # Show task details
bd done 1            # Mark as done
bd list --done       # Verify task shows as done
```

**Success criteria**: All commands work without errors

### 5. Update Project Documentation

**Update README.md** - Add Beads setup section:

```markdown
### Optional: Beads Integration

Whisper supports [Beads](https://github.com/steveyegge/beads) for enhanced agent memory and task tracking.

**Install Beads:**
```bash
curl -fsSL https://raw.githubusercontent.com/steveyegge/beads/main/scripts/install.sh | bash
```

**Initialize in project:**
```bash
bd init
```

See `AGENTS.md` for agent workflow with Beads.
```

**Rationale**: Make it easy for future users/contributors to set up Beads

## Acceptance Criteria

- [ ] `bd --version` shows version number
- [ ] `.beads/` directory exists in whisper project root
- [ ] `.beads/issues.jsonl` and `.beads/config.json` exist
- [ ] `.gitignore` includes `.beads/beads.db`
- [ ] Test task can be created, listed, and marked done
- [ ] README.md includes Beads installation instructions

## Testing

**Manual verification**:
1. Run `bd --version` - should succeed
2. Run `bd list` - should work (empty or with test tasks)
3. Check git status - `.beads/beads.db` should be ignored
4. Create/modify task - should appear in `bd list` immediately

**Edge cases**:
- Already have Beads installed (should skip installation gracefully)
- `.beads/` already exists (should error or prompt to reinitialize)
- Permission issues (installation script should handle)

## Dependencies

**Requires**: None (this is the foundation)

**Blocks**: All other specs in this epic

## Estimated Effort

**Time**: 30 minutes

**Breakdown**:
- Installation: 10 minutes (mostly waiting for download)
- Initialization and git config: 5 minutes
- Testing and verification: 10 minutes
- Documentation update: 5 minutes

## Implementation Notes

**Platform considerations**:
- Installation script supports macOS and Linux
- Windows support unclear (check Beads documentation if needed)
- User is on macOS per environment context

**Git workflow**:
- After initialization, commit `.beads/` setup:
  ```bash
  git add .beads/issues.jsonl .beads/config.json .gitignore README.md
  git commit -m "Initialize Beads task management system"
  ```

**Graceful degradation**:
- If installation fails, document the error for assessment
- Epic can still be valuable for evaluating if Beads *would* work
- Don't force installation if user environment has conflicts

## Success Metrics

- Installation completes without errors
- Basic commands (`bd list`, `bd create`, `bd done`) work
- Git tracking configured correctly
- User can proceed to manual Beads experience with working tool

## Related Files

- `.gitignore` - Updated to ignore local DB
- `README.md` - Updated with installation instructions
- `.beads/issues.jsonl` - Created by initialization
- `.beads/config.json` - Created by initialization

## Tags

`chore` `infrastructure` `installation` `beads` `setup` `git-config` `phase-1`
