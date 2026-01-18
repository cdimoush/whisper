---
allowed-tools: Bash(python:*), Bash(uv:*), Bash(mkdir:*), Bash(mv:*), Bash(date:*), Bash(curl:*), Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
description: Transcribe audio and act on the request
argument-hint: <audio-file-path>
---

# Act on Audio

Transcribe the provided audio file, generate an intelligent title, and execute the request spoken within it.

## Step 1: Transcribe the Audio

Use the OpenAI Whisper API to transcribe:

```bash
curl -s https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: multipart/form-data" \
  -F file="@$ARGUMENTS" \
  -F model="gpt-4o-mini-transcribe" \
  -F response_format="text"
```

Save the full transcription text for use in subsequent steps.

## Step 2: Generate Intelligent Title

Analyze the transcription and create a descriptive, kebab-case title (3-5 words).

Examples of good titles:
- `player-movement-feature-request`
- `api-refactor-discussion`
- `bug-fix-auth-flow`

## Step 3: Create Timestamp

Get the current timestamp:

```bash
date +%Y-%m-%d_%H-%M-%S
```

## Step 4: Analyze the Transcription

Identify:

1. **Request Type**: What is the user asking for?
   - **Summary**: User wants a summary of ideas or content
   - **Research**: User wants research on a topic
   - **Code**: User wants code or technical implementation
   - **Planning**: User wants a plan or structured approach
   - **Other**: Any other actionable request

2. **Key Details**: Extract main topics, requirements, constraints, and goals

3. **Deliverables**: What output files should be created?

## Step 5: Create Output Directory

Create the output directory using the generated title and timestamp:

```bash
mkdir -p ".aura/output/{title}_{timestamp}/"
```

Example: `.aura/output/api-refactor-discussion_2026-01-08_14-30-22/`

## Step 6: Create README.md

In the output directory, create a `README.md` with:

```markdown
# {Generated Title}

## Source
- **Audio File**: [original filename]
- **Transcribed**: [timestamp]

## Transcription Summary
[2-3 sentence summary of what was spoken]

## Request Identified
- **Type**: [Summary/Research/Code/Planning/Other]
- **Description**: [What the user is asking for]

## Deliverables
- [ ] [List of files that will be created]

## Full Transcription
<details>
<summary>Click to expand</summary>

[Full transcription text]

</details>
```

## Step 7: Execute the Request

Based on the request type, create appropriate deliverables:

### For Summary Requests
- Create `summary.md` with key points, main ideas, action items

### For Research Requests
- Create `research.md` with overview, findings, sources, recommendations

### For Code Requests
- Create implementation files with appropriate extensions
- Include usage documentation if needed

### For Planning Requests
- Create `plan.md` with goals, steps, considerations, next actions

## Step 8: Move Audio to Output Directory

Move the processed audio file into the output directory:

```bash
mv "$ARGUMENTS" ".aura/output/{title}_{timestamp}/"
```

## Important Notes

- Always create the output directory first before writing any files
- If the request is unclear, focus on the primary request and note others in the README
- Only move the audio after successful processing
