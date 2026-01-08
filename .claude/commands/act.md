---
allowed-tools: Bash(python:*), Bash(uv:*), Bash(mkdir:*), Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
description: Transcribe audio and act on the request
argument-hint: <audio-file-path>
---

# Act on Audio

Transcribe the provided audio file and execute the request spoken within it.

## Step 1: Transcribe the Audio

Run the transcription script:

```bash
uv run python scripts/transcribe.py $ARGUMENTS
```

## Step 2: Analyze the Transcription

After receiving the transcription, analyze it to identify:

1. **Request Type**: What is the user asking for?
   - **Summary**: User wants a summary of ideas, thoughts, or content they described
   - **Research**: User wants research on a topic, including sources and analysis
   - **Code**: User wants code, scripts, or technical implementation
   - **Planning**: User wants a plan, outline, or structured approach
   - **Other**: Any other actionable request

2. **Key Details**: Extract the main topics, requirements, constraints, and goals mentioned

3. **Deliverables**: What output files should be created?

## Step 3: Create Output Directory

Create a timestamped output directory:

```bash
mkdir -p output/$(date +%Y-%m-%d_%H-%M-%S)
```

Store the directory path for use in subsequent steps.

## Step 4: Create README.md

In the output directory, create a `README.md` with the following structure:

```markdown
# [Brief Title Based on Request]

## Source
- **Audio File**: [original audio file path]
- **Transcribed**: [current timestamp]

## Transcription Summary
[2-3 sentence summary of what was spoken]

## Request Identified
- **Type**: [Summary/Research/Code/Planning/Other]
- **Description**: [What the user is asking for]

## Deliverables
- [ ] [List of files that will be created]
- [ ] [Each file with brief description]

## Full Transcription
<details>
<summary>Click to expand full transcription</summary>

[Full transcription text]

</details>
```

## Step 5: Execute the Request

Based on the request type, create the appropriate deliverables in the output directory:

### For Summary Requests
- Create `summary.md` with structured summary including:
  - Key points
  - Main ideas
  - Action items (if any)
  - Conclusions

### For Research Requests
- Create `research.md` with:
  - Overview of the topic
  - Key findings (use WebSearch/WebFetch to gather current information)
  - Sources and references
  - Analysis and recommendations

### For Code Requests
- Create implementation files with appropriate extensions
- Include comments explaining the code
- Create a `usage.md` if the code needs documentation

### For Planning Requests
- Create `plan.md` with:
  - Goals and objectives
  - Step-by-step approach
  - Considerations and tradeoffs
  - Next steps

### For Other Requests
- Interpret the request and create appropriate output
- Document your interpretation in the README

## Step 6: Update README with Completion Status

After creating all deliverables, update the README.md:
- Check off completed deliverables
- Add any notes about the output
- Include suggestions for follow-up if relevant

## Important Notes

- Always create the output directory first before writing any files
- If the request is unclear or contains multiple distinct asks, focus on the primary request and note others in the README
- If research is requested, use WebSearch and WebFetch to gather current information
- Maintain a professional, organized structure in all output files
