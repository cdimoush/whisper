# Feature: Transcribe Slash Command

## Feature Description
A Claude Code slash command (`/transcribe`) that transcribes audio files using OpenAI's Whisper API. Users can invoke `/transcribe /path/to/audio.m4a` to get the spoken content converted to text, which can then be used for summarization, task extraction, or other LLM processing. This is particularly useful for Mac Voice Memos (`.m4a` files).

## User Story
As a Claude Code user
I want to transcribe audio files with a simple slash command
So that I can quickly convert voice memos to text for further processing

## Problem Statement
Users have audio recordings (voice memos, meeting recordings, etc.) that they want to process with Claude Code, but there's no built-in way to convert audio to text. Currently, users would need to manually transcribe or use external tools before bringing content into Claude Code.

## Solution Statement
Create a `/transcribe` slash command that:
1. Accepts an audio file path as an argument
2. Runs a Python script that calls OpenAI's Whisper API
3. Returns the transcription text for further processing by Claude

The command will use `gpt-4o-mini-transcribe` as the default model for fast, cost-effective transcription.

## Relevant Files
Use these files to implement the feature:

- `README.md` - Contains supported formats, model options, and slash command reference patterns
- `one_idea.md` - Contains the Python implementation code and API details
- `.claude/commands/` - Directory where slash commands are stored; existing commands show the pattern

### New Files
- `.claude/commands/transcribe.md` - The slash command definition
- `scripts/transcribe.py` - Python script that calls OpenAI's Whisper API
- `.env.example` - Template showing required environment variables
- `.env` - Local environment file with actual API keys (gitignored)
- `.gitignore` - Excludes `.env` and other sensitive/generated files

## Implementation Plan
### Phase 1: Foundation
Set up the Python transcription script that interfaces with OpenAI's API. This script will be the backend for the slash command.

### Phase 2: Core Implementation
Create the slash command markdown file with proper frontmatter configuration to allow bash execution of Python scripts.

### Phase 3: Integration
Test the command with a real audio file (`initial_memo.m4a`) to validate end-to-end functionality.

## Step by Step Tasks

### Step 1: Create scripts directory
- Create `scripts/` directory if it doesn't exist
- This will hold the Python transcription script

### Step 2: Create .env files for API key management
- Create `.env.example` with placeholder: `OPENAI_API_KEY=your-api-key-here`
- Create `.gitignore` with `.env` entry to prevent committing secrets
- User copies `.env.example` to `.env` and fills in their real API key

### Step 3: Create the transcription Python script
- Create `scripts/transcribe.py`
- Load environment variables from `.env` using `python-dotenv`
- Implement the `transcribe_audio()` function using OpenAI's API
- Use `gpt-4o-mini-transcribe` as the default model
- Handle file path argument from command line
- Print the transcription to stdout for Claude to consume

### Step 4: Create the slash command
- Create `.claude/commands/transcribe.md`
- Add frontmatter with:
  - `allowed-tools: Bash(python:*), Bash(uv:*)`
  - `description: Transcribe audio file to text`
  - `argument-hint: <audio-file-path>`
- Add prompt instructing Claude to run the transcription script with `$ARGUMENTS`

### Step 5: Add execution permission to script
- Make `scripts/transcribe.py` executable with `chmod +x`

### Step 6: Validate with test audio file
- Run the transcription on `initial_memo.m4a` to verify it works
- Ensure the output is clean text suitable for further LLM processing

## Testing Strategy
### Unit Tests
- No unit tests required for this simple script (it's a thin wrapper around OpenAI's API)

### Integration Tests
- Test the slash command with `initial_memo.m4a`
- Verify transcription output is returned correctly

### Edge Cases
- Audio file doesn't exist - script should error gracefully
- File too large (>25MB) - script should warn user
- Missing OPENAI_API_KEY - script should provide helpful error message
- Unsupported file format - script should list supported formats

## Acceptance Criteria
- [ ] `/transcribe /path/to/audio.m4a` successfully transcribes the audio file
- [ ] Transcription text is returned and visible in Claude Code
- [ ] `.env.example` exists with placeholder for `OPENAI_API_KEY`
- [ ] `.env` is gitignored and not committed to version control
- [ ] Script loads API key from `.env` file using python-dotenv
- [ ] Script handles missing files gracefully with clear error message
- [ ] Script handles missing API key gracefully with clear error message
- [ ] Works with the included `initial_memo.m4a` test file

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `ls -la scripts/transcribe.py .claude/commands/transcribe.md .env.example .gitignore` - Verify all files exist
- `cat .env.example` - Verify .env template is correct
- `cat .gitignore` - Verify .env is gitignored
- `cat .claude/commands/transcribe.md` - Verify slash command content is correct
- `python scripts/transcribe.py initial_memo.m4a` - Test transcription with sample file (requires .env with OPENAI_API_KEY)

## Notes
- Requires Python packages: `pip install openai python-dotenv` or `uv add openai python-dotenv`
- Copy `.env.example` to `.env` and add your OpenAI API key
- The `.env` file is gitignored to prevent committing secrets
- For files >25MB, user should compress with ffmpeg: `ffmpeg -i input.m4a -vn -ac 1 -ar 16000 -b:a 48k output.m4a`
- Alternative models available: `gpt-4o-transcribe` (higher quality), `whisper-1` (timestamp support)
