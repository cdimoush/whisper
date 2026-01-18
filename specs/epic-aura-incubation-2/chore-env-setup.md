# Chore: Environment Setup Documentation

## Description

Create `.env.example` and document the environment variables needed for aura to work.

## Files to Create

### 1. .env.example for Aura repo

**Location**: `aura/.env.example`

```bash
# Aura Environment Variables
# Copy to .env and fill in values

# Required for transcription
OPENAI_API_KEY=sk-your-key-here

# Optional: Override default transcription model
# AURA_TRANSCRIPTION_MODEL=gpt-4o-mini-transcribe

# Optional: Override default title generation model
# AURA_TITLE_MODEL=gpt-4o-mini
```

### 2. .env.example Template for Wrapped Repos

**Location**: `aura/src/aura/templates/aura/.env.example`

```bash
# Aura Environment Variables
# Copy to .env and fill in values

# Required for /aura.transcribe and /aura.act
OPENAI_API_KEY=sk-your-key-here
```

### 3. Update Setup Documentation

Add to README.md installation section:

```markdown
## Environment Setup

1. Copy the example env file:
   ```bash
   cp .env.example .env
   ```

2. Add your OpenAI API key:
   ```bash
   # Edit .env
   OPENAI_API_KEY=sk-your-actual-key
   ```

3. Verify setup:
   ```bash
   aura check
   ```
```

## Acceptance Criteria

- [ ] `aura/.env.example` exists with documented variables
- [ ] Template `.env.example` is copied during init
- [ ] README.md includes env setup instructions
- [ ] `aura check` validates OPENAI_API_KEY is set

## Notes

- .env files should be in .gitignore
- Keep required variables minimal (just OPENAI_API_KEY)
- Optional variables have sensible defaults
