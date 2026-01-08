# Feature: Act On Audio Slash Command

## Feature Description
A Claude Code slash command (`/act_on_audio`) that wraps the existing `/transcribe` functionality and takes action based on what the user says in the audio. The command transcribes the audio file, interprets the spoken request, creates a timestamped project directory, generates a README summarizing the expectations, and then executes the requested task by creating appropriate files. This enables a voice-driven workflow where users can speak their ideas and have Claude Code automatically organize and act on them.

## User Story
As a Claude Code user
I want to speak my ideas into a voice memo and have them automatically transcribed and acted upon
So that I can quickly capture thoughts and have structured output (summaries, research, code) without typing

## Problem Statement
The existing `/transcribe` command converts audio to text but requires manual follow-up to act on the content. Users who record voice memos with requests like "research X", "summarize Y", or "create a script that does Z" must then manually instruct Claude to perform those tasks. This breaks the flow of voice-driven ideation and adds friction to the workflow.

## Solution Statement
Create an `/act_on_audio` slash command that:
1. Transcribes the audio file using the existing `scripts/transcribe.py`
2. Interprets the transcription as a request/instruction to the agent
3. Creates a timestamped output directory (e.g., `output/2025-01-03_18-30-00/`)
4. Generates a `README.md` summarizing what was requested and what will be delivered
5. Creates the appropriate output files based on the request type:
   - **Summary**: A markdown file with structured summary of the spoken content
   - **Research**: Markdown files with research findings, sources, and analysis
   - **Code**: Implementation files with the requested functionality

The command biases toward organized output with clear documentation of intent and deliverables.

## Relevant Files
Use these files to implement the feature:

- `README.md` - Project overview and slash command reference patterns
- `scripts/transcribe.py` - Existing transcription script to reuse
- `.claude/commands/transcribe.md` - Pattern for slash command definition with frontmatter
- `specs/transcribe-command.md` - Example spec format and implementation approach

### New Files
- `.claude/commands/act_on_audio.md` - The slash command definition that orchestrates the workflow

## Implementation Plan
### Phase 1: Foundation
Design the slash command prompt that will guide Claude to:
1. Run the transcription script
2. Analyze the transcription for actionable requests
3. Create organized output structure

### Phase 2: Core Implementation
Create the slash command markdown file with comprehensive instructions for Claude to:
- Identify the type of request (summary, research, code, or other)
- Create timestamped output directory
- Generate README with expectations
- Execute the appropriate task

### Phase 3: Integration
Test the command with real audio files containing different types of requests to validate the workflow handles various use cases.

## Step by Step Tasks

### Step 1: Create the act_on_audio slash command
- Create `.claude/commands/act_on_audio.md`
- Add frontmatter with:
  - `allowed-tools: Bash(python:*), Bash(uv:*), Bash(mkdir:*), Read, Write, Edit, Glob, Grep, WebFetch, WebSearch`
  - `description: Transcribe audio and act on the request`
  - `argument-hint: <audio-file-path>`
- Write comprehensive prompt that instructs Claude to:
  1. Run `uv run python scripts/transcribe.py $ARGUMENTS` to get transcription
  2. Analyze the transcription to identify the request type and key details
  3. Create output directory with format `output/YYYY-MM-DD_HH-MM-SS/`
  4. Create `README.md` in that directory summarizing:
     - Original audio file path
     - Transcription summary
     - Request type identified
     - Expected deliverables
  5. Execute the request by creating appropriate files in the output directory

### Step 2: Create output directory structure
- Ensure `output/` directory exists (or instruct command to create it)
- Add `output/` to `.gitignore` if not already present (user-generated content)

### Step 3: Validate with test scenarios
- Test with `initial_memo.m4a` which contains multiple request types
- Verify output directory is created with correct timestamp format
- Verify README accurately captures the request
- Verify appropriate output files are generated

## Testing Strategy
### Unit Tests
- No unit tests required (this is a prompt-based slash command orchestrating existing tools)

### Integration Tests
- Test with audio requesting a summary → should produce summary markdown
- Test with audio requesting research → should produce research markdown with sources
- Test with audio requesting code → should produce implementation files

### Edge Cases
- Audio with multiple distinct requests → should identify primary request or ask for clarification
- Audio with unclear/rambling content → should summarize and ask user what action to take
- Very short audio with minimal content → should handle gracefully
- Audio file doesn't exist → transcription script handles this error

## Acceptance Criteria
- [ ] `/act_on_audio /path/to/audio.m4a` transcribes and creates output directory
- [ ] Output directory follows `output/YYYY-MM-DD_HH-MM-SS/` format
- [ ] `README.md` is created with request summary and expected deliverables
- [ ] Summary requests produce structured markdown summary
- [ ] Research requests produce research findings with sources
- [ ] Code requests produce implementation files
- [ ] Works with `initial_memo.m4a` test file

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cat .claude/commands/act_on_audio.md` - Verify slash command content is correct
- `ls -la output/` - Verify output directory structure after running command
- `cat output/*/README.md` - Verify README content captures the request

## Notes
- The command relies on Claude's interpretation of the transcription, so output quality depends on Claude's understanding
- Users can re-run with the same audio to get different interpretations if needed
- The timestamped directory structure prevents overwriting previous runs
- Future enhancement: Add optional flags for request type override (e.g., `/act_on_audio --type=research /path/to/audio.m4a`)
- Future enhancement: Support for chaining multiple audio files into a single output
