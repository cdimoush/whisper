# Feature: Title Generation Script

## Feature Description

Port whisper's `scripts/generate_title.py` to `.aura/scripts/generate_title.py` for intelligent output directory naming.

## User Story

As a developer using aura
I want output directories to have meaningful names
So that I can find transcriptions easily

## Source

Copy from: `whisper/scripts/generate_title.py`

## Purpose

When `/aura.act` processes an audio file, it creates an output directory like:
```
.aura/output/design-lab-architecture-review_2026-01-18_14-30-00/
```

Instead of:
```
.aura/output/audio_2026-01-18_14-30-00/
```

## Target File

**Location**: `aura/src/aura/templates/aura/scripts/generate_title.py`

## Interface

```bash
# Input: transcription text (via stdin or argument)
python .aura/scripts/generate_title.py "I want to talk about the design lab architecture..."

# Output: kebab-case title
design-lab-architecture-review
```

## Key Requirements

1. **Use LLM for title generation** (OpenAI API)
2. **Output kebab-case** (lowercase, hyphens)
3. **Keep it short** (3-5 words ideal)
4. **Be descriptive** (capture the essence)
5. **Fallback gracefully** if API fails

## Example Transformations

| Input (excerpt) | Output |
|-----------------|--------|
| "I want to add user authentication..." | `user-authentication-feature` |
| "Today I'm thinking about the simulation mandate..." | `simulation-mandate-planning` |
| "Quick note about the bug in checkout..." | `checkout-bug-fix` |

## Acceptance Criteria

- [ ] Script exists at `aura/src/aura/templates/aura/scripts/generate_title.py`
- [ ] Accepts text via argument or stdin
- [ ] Outputs kebab-case title to stdout
- [ ] Uses OpenAI API for intelligent generation
- [ ] Graceful fallback if API unavailable
- [ ] Works standalone (no aura imports)

## Notes

- Uses same OPENAI_API_KEY as transcription
- Should be fast (use smaller model like gpt-4o-mini)
- Fallback: extract first few words and kebab-case them
