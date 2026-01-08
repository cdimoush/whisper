# Chore: Simplify Planning Commands

## Chore Description
Rewrite `.claude/commands/feature.md`, `.claude/commands/chore.md`, and `.claude/commands/implement.md` to be optimized for this whisper audio transcription project. The current versions are copied from a complex client/server web application and include many irrelevant sections (client/server references, extensive testing strategies, multi-phase rollouts, etc.). This project is simpler: it's focused on audio transcription, simple Python scripts, and slash commands with no testing framework yet.

## Problem
The current planning commands are bloated and misaligned with this project's actual needs:
- References to `app/server/**` and `app/client/**` that don't exist
- Extensive testing sections when there are no tests yet
- Complex multi-phase implementation plans for simple script additions
- Validation commands that assume pytest and server infrastructure
- Overall complexity that adds friction to planning simple features
- Implement command assumes git repo and uses `git diff --stat` (this isn't a git repo)

## Solution
Create streamlined planning command templates that:
- Reflect the actual project structure (scripts/, .claude/commands/, specs/)
- Focus on audio transcription and processing workflows
- Emphasize simplicity for single-file script features
- Remove testing sections (can be added later when tests exist)
- Keep validation commands simple and relevant
- Maintain the core benefit: structured planning in specs/*.md files

## Current Project Structure
```
whisper_zip/
├── .claude/commands/     # Slash commands
├── scripts/              # Python scripts (transcribe.py, etc.)
├── specs/                # Planning documents
├── output/               # Generated outputs from audio processing
├── main.py               # CLI entry point
└── README.md             # Project documentation
```

## Relevant Files

### Files to Modify
- `.claude/commands/feature.md` - Feature planning command (currently 92 lines, too complex)
- `.claude/commands/chore.md` - Chore planning command (currently 54 lines, moderately complex)
- `.claude/commands/implement.md` - Implementation command (currently 12 lines, assumes git repo)

### Reference Files
- `specs/transcribe-command.md` - Example of appropriate feature spec for this project
- `specs/act-on-audio-command.md` - Example of appropriate feature spec for this project
- `README.md` - Project overview showing actual structure and scope

## Step by Step Tasks

### Step 1: Analyze current planning command usage
- Review existing specs to understand what sections are actually useful
- Identify which sections from the original templates are never used or filled with placeholder text
- Note the common patterns in this project's features (mostly: slash command + Python script)

### Step 2: Design simplified feature.md template
- Create feature template optimized for:
  - Audio transcription workflows
  - Simple Python scripts
  - Slash command creation
  - Integration with existing scripts/transcribe.py
- Remove sections:
  - Client/server references
  - Unit/integration testing (until tests exist)
  - Multi-phase rollouts (overkill for simple scripts)
- Keep sections:
  - Feature description and user story (valuable context)
  - Problem/solution statements (clarifies intent)
  - Relevant files (essential for planning)
  - Step by step tasks (core value)
  - Acceptance criteria (keeps scope clear)
  - Validation commands (simplified for scripts/commands)
  - Notes (useful for future considerations)
- Update "Relevant Files" section to focus on:
  - `README.md` - Project overview
  - `scripts/` - Python scripts
  - `.claude/commands/` - Slash commands
  - `specs/` - Prior specs as examples

### Step 3: Design simplified chore.md template
- Create chore template optimized for:
  - Quick refactoring tasks
  - Documentation updates
  - Script improvements
  - Configuration changes
- Remove sections:
  - Testing references
  - Complex validation
- Keep sections:
  - Chore description
  - Relevant files
  - Step by step tasks
  - Validation commands (simplified)
  - Notes
- Update "Relevant Files" section similarly to feature.md

### Step 4: Design simplified implement.md template
- Create implement template that doesn't assume git repo
- Remove git-specific reporting (`git diff --stat`)
- Replace with simple file-based reporting:
  - List files created/modified
  - Show brief summary of changes
  - Optionally use `diff` or file comparison if needed
- Keep the core workflow:
  - Read the plan from $ARGUMENTS (spec file path)
  - Think hard and implement the plan
  - Report what was completed
- Make reporting flexible for non-git projects

### Step 5: Simplify validation commands
- Replace `cd app/server && uv run pytest` with project-appropriate validations:
  - `python scripts/script_name.py --help` - Verify script works
  - `cat .claude/commands/command_name.md` - Verify command content
  - `python scripts/script_name.py test_file.m4a` - Test with sample audio
  - Manual testing instructions for audio workflows

### Step 6: Update instructions section
- Remove references to client/server architecture
- Emphasize keeping solutions simple (already good in original)
- Add guidance specific to audio transcription projects:
  - Consider ffmpeg requirements
  - Think about file size limits (25MB)
  - Plan for different audio formats
  - Consider chunking for long files

### Step 7: Add project-specific examples
- Include inline examples of typical features for this project:
  - Adding a new transcription model option
  - Creating a new audio processing slash command
  - Adding output formatting options
  - Improving error handling for audio files

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `cat .claude/commands/feature.md` - Review simplified feature template
- `cat .claude/commands/chore.md` - Review simplified chore template
- `cat .claude/commands/implement.md` - Review simplified implement template
- `wc -l .claude/commands/feature.md .claude/commands/chore.md .claude/commands/implement.md` - Verify line count reduction
- Compare new templates against existing specs (`specs/transcribe-command.md`, `specs/act-on-audio-command.md`) to ensure all necessary sections are present

## Notes
- This is about removing complexity, not removing value
- The core structure (specs/*.md planning files) remains the same
- Future enhancement: When tests are added, we can add back a lightweight testing section
- Goal is to make planning feel lightweight and appropriate for this project's scale
- Current line counts: feature.md (92 lines), chore.md (54 lines), implement.md (12 lines)
- Target: ~50-60 lines for feature.md, ~35-40 lines for chore.md, ~15-20 lines for implement.md
- Keep the markdown plan format structure - it's the main value
- Implement command should work for non-git projects (many users won't initialize git)
- The workflow remains: `/feature` or `/chore` creates plan → user reviews → `/implement specs/plan-name.md` executes it
