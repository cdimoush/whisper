# Feature: Intelligent Title Generation

## Feature Description

Generate memorable, human-readable titles for transcriptions using an LLM to analyze the content. Instead of relying on timestamps alone (e.g., `2025-01-03_18-30-00/`), create output directories named `api-refactor-discussion_2026-01-08_14-30-22/` where the first part is an intelligent title that makes it easy to find past memos.

This feature implements a Python module that takes transcription text as input and returns a short, kebab-case title that captures the main topic. The module will be used by the queue processor to name output directories, but is designed to be testable independently.

## User Story

As a developer using voice memos to capture ideas
I want my transcriptions to have meaningful titles instead of just timestamps
So that I can quickly browse and find "that memo about the API refactor" without searching through dates

## Problem Statement

Current workflow uses timestamp-based organization (`output/2025-01-03_18-30-00/`), which makes discoverability extremely difficult. Users must remember when they recorded something rather than what they recorded. This leads to:
- Difficulty finding specific memos ("was that Monday or Tuesday?")
- Poor scanability when browsing past transcriptions
- Need to open each README to see what a memo was about
- Mental overhead remembering temporal context instead of topical context

## Solution Statement

Create a `scripts/generate_title.py` module that uses an LLM (GPT-4o-mini) to read a transcription and generate a concise, descriptive title in kebab-case format. The module will:
1. Take transcription text as input (from stdin or file)
2. Send a focused prompt to the LLM asking for a 2-5 word title
3. Return a sanitized kebab-case string suitable for directory names
4. Handle edge cases (empty input, very long titles, special characters)

This module is designed to be integrated into the queue processor but can also be tested standalone for validation.

## Relevant Files

Use these files to implement the feature:

- `scripts/transcribe.py` - Reference for OpenAI API usage patterns (uses `OpenAI()` client)
- `.env` - Already contains `OPENAI_API_KEY` for API access

### New Files
- `scripts/generate_title.py` - Core title generation module with CLI interface
- `scripts/test_title_generation.py` - Simple test script with sample transcriptions (optional but recommended for USER BREAKPOINT #2)

## Step by Step Tasks

IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create title generation module structure
- Create `scripts/generate_title.py` with the following components:
  - Import OpenAI client and standard libraries (sys, re, argparse)
  - Define `MAX_TITLE_LENGTH = 50` constant (characters before truncation)
  - Define `sanitize_title(title: str) -> str` function to convert to kebab-case
  - Define `generate_title(transcription: str, model: str = "gpt-4o-mini") -> str` function

### Step 2: Implement sanitize_title function
- Lowercase the entire string
- Replace spaces and underscores with hyphens
- Remove all characters except alphanumeric and hyphens using regex: `re.sub(r'[^a-z0-9-]+', '', title)`
- Replace multiple consecutive hyphens with a single hyphen: `re.sub(r'-+', '-', title)`
- Strip leading and trailing hyphens: `title.strip('-')`
- Truncate to `MAX_TITLE_LENGTH` characters if needed
- Handle empty string edge case (return "untitled")

### Step 3: Implement generate_title function
- Load environment variables with `python-dotenv` (following pattern from `transcribe.py`)
- Create OpenAI client instance
- Construct a focused prompt:
  ```
  Generate a short, memorable title (2-5 words) for this voice memo transcription.
  The title should capture the main topic or purpose.
  Return ONLY the title, no explanation or formatting.

  Transcription:
  {transcription}
  ```
- Use `client.chat.completions.create()` with `gpt-4o-mini` model
- Extract the title from the response
- Pass through `sanitize_title()` to ensure it's filesystem-safe
- Return the sanitized title

### Step 4: Add CLI interface
- Implement `main()` function with argument parsing:
  - Accept transcription text from stdin (pipe support) OR
  - Accept `--file` argument to read from a file OR
  - Accept `--text` argument for direct text input
- Add `--model` argument (default: "gpt-4o-mini") for model selection
- Print the generated title to stdout
- Handle errors gracefully (missing API key, empty input, API failures)

### Step 5: Add error handling and edge cases
- Check for `OPENAI_API_KEY` environment variable
- Handle empty or very short transcriptions (< 10 characters) → return "short-memo"
- Handle very long transcriptions (> 10,000 characters) → truncate to first 5,000 before sending to LLM
- Handle API errors (rate limits, network issues) → return "transcription-{timestamp}"
- Add brief usage instructions when run with `--help`

### Step 6: Make script executable
- Add shebang line: `#!/usr/bin/env python3`
- Set executable permissions: `chmod +x scripts/generate_title.py`

### Step 7: Create test script (optional but recommended)
- Create `scripts/test_title_generation.py` with 5-6 sample transcriptions covering:
  - Code/feature discussion: "I want to refactor the authentication system to use JWT tokens instead of sessions..."
  - Meeting notes: "Standup update - finished the user dashboard, working on API rate limiting next..."
  - Research ideas: "Look into using Redis for caching the API responses, especially for the analytics endpoints..."
  - Task list: "TODO: update the documentation, fix the mobile responsive layout, and review the pull requests..."
  - Short memo: "Call Sarah about the deployment schedule"
  - Rambling/unclear: "So yeah, um, I was thinking about like, you know, the thing we talked about..."
- Run title generation on each sample and display results
- This script will be useful for USER BREAKPOINT #2 validation

### Step 8: Run validation commands
- Test the title generation with various inputs
- Verify edge cases are handled properly
- Confirm titles are filesystem-safe and memorable

## Acceptance Criteria

- [ ] `generate_title.py` exists and is executable
- [ ] Accepts transcription text via stdin, --file, or --text argument
- [ ] Generates concise, kebab-case titles (2-5 words)
- [ ] Handles empty input gracefully (returns "untitled" or similar)
- [ ] Handles very long transcriptions (truncates before API call)
- [ ] Sanitizes output to be filesystem-safe (no special characters, spaces)
- [ ] Returns meaningful titles for diverse transcription types (code, meetings, research, tasks)
- [ ] Uses `OPENAI_API_KEY` from environment
- [ ] Provides helpful error messages for missing API key or invalid input
- [ ] Can be run standalone for testing before queue processor integration

## Validation Commands

Execute every command to validate the feature works correctly.

```bash
# Verify script exists and is executable
ls -la scripts/generate_title.py
head -1 scripts/generate_title.py  # Should show #!/usr/bin/env python3

# Test with direct text input
echo "I want to refactor the authentication system to use JWT tokens instead of sessions" | uv run python scripts/generate_title.py

# Expected output: something like "auth-refactor-jwt" or "jwt-auth-system"

# Test with short input (edge case)
echo "test" | uv run python scripts/generate_title.py

# Expected output: "short-memo" or similar fallback

# Test with file input (create a sample)
echo "Standup update - finished the user dashboard, working on API rate limiting next week" > /tmp/sample_transcription.txt
uv run python scripts/generate_title.py --file /tmp/sample_transcription.txt

# Expected output: something like "standup-dashboard-rate-limiting" or "dashboard-api-progress"

# Test help text
uv run python scripts/generate_title.py --help

# Run test script if created
uv run python scripts/test_title_generation.py

# Test that titles are filesystem-safe (no special characters)
echo "Let's refactor the API! (Breaking changes ahead...)" | uv run python scripts/generate_title.py
# Should not contain special characters like !, (, ), ...
```

## Notes

- **Model choice**: Use `gpt-4o-mini` (not `gpt-4o`) to minimize cost - title generation is a simple task
- **Prompt engineering**: Keep the prompt simple and direct. We want concise titles, not verbose explanations
- **Filesystem safety**: The `sanitize_title()` function is critical - titles become directory names
- **Integration point**: This module will be imported by `process_queue.py` in the next feature
- **Testing strategy**: USER BREAKPOINT #2 will validate title quality with real examples before integrating into queue processor
- **Future enhancement**: Could add semantic deduplication (if title is too similar to existing title, add a suffix)
- **Title length**: 2-5 words (roughly 10-50 characters) is the sweet spot for scanability
- **Edge cases to test during breakpoint**:
  - Very technical transcriptions (code, algorithms)
  - Casual conversational memos
  - Multiple topics in one memo (should pick primary topic)
  - Non-English transcriptions (should still generate English titles for consistency)
