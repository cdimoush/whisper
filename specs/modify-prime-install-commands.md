# Chore: Modify Prime and Install Commands for Whisper Project

## Chore Description
Update the `/prime` and `/install` slash commands to be appropriate for the whisper audio transcription project. Currently, these commands reference git repositories, frontend/backend dependencies, and scripts that don't exist in this project. The whisper project is a simple Python tool with:
- Python dependencies managed via `uv`
- OpenAI API key in `.env` file
- `ffmpeg` system dependency
- No frontend/backend architecture
- No git repository requirement

## Relevant Files
Use these files to resolve the chore:

- `.claude/commands/prime.md` (8 lines) - Currently uses `git ls-files` which assumes a git repo, and only reads README.md
- `.claude/commands/install.md` (11 lines) - References prime.md, talks about FE/BE dependencies, and runs a non-existent `./scripts/copy_dot_env.sh` script
- `README.md` - Contains the actual setup instructions for the whisper project (uv sync, OPENAI_API_KEY, ffmpeg)
- `pyproject.toml` - Python project configuration with dependencies

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Rewrite prime.md for whisper project
- Update `/prime` to help users understand the whisper project structure
- Remove git-specific commands (`git ls-files` doesn't work for non-git projects)
- Add commands to explore the project structure:
  - List directory contents
  - Show key files (README.md, pyproject.toml, scripts/, .claude/commands/)
- Read important documentation files:
  - README.md for project overview
  - pyproject.toml for dependencies
  - Example spec files to understand the planning workflow
- Provide a clear summary of what the tool does and how it's organized

### Step 2: Rewrite install.md for whisper project
- Update `/install` to set up the whisper project for use
- Remove references to FE/BE dependencies and non-existent scripts
- Add actual setup steps:
  - Check for `ffmpeg` installation (required system dependency)
  - Run `uv sync` to install Python dependencies
  - Check for `.env` file existence
  - Guide user to create `.env` with `OPENAI_API_KEY` if missing
  - Verify installation by checking if dependencies are installed
- Call the updated `/prime` command to help user understand the codebase
- Report what was set up and any manual steps needed

### Step 3: Test both commands work correctly
- Verify prime.md can be executed and provides useful output
- Verify install.md can be executed and runs setup steps
- Ensure both commands work for non-git projects

## Validation Commands
Execute every command to validate the chore is complete.

- `cat .claude/commands/prime.md` - Review updated prime command
- `cat .claude/commands/install.md` - Review updated install command
- `wc -l .claude/commands/prime.md .claude/commands/install.md` - Verify reasonable length
- Manual test: Try running the commands conceptually to ensure they make sense

## Notes
- The `/prime` command should help users quickly understand the project without assuming git
- The `/install` command should be a helpful onboarding tool for new users
- Both commands should work whether or not the project is in a git repository
- Focus on the actual dependencies: uv, ffmpeg, OpenAI API key
- These are onboarding/setup commands, not planning commands, so they can be more prescriptive
