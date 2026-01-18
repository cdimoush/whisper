---
allowed-tools: Bash(python:*), Bash(uv:*), Bash(curl:*)
description: Transcribe audio file to text
argument-hint: <audio-file-path>
---

# Transcribe Audio

Transcribe the provided audio file using OpenAI Whisper API.

## Prerequisites

- `OPENAI_API_KEY` environment variable must be set
- Supported formats: mp3, m4a, wav, webm (max 25MB)

## Instructions

1. Verify the audio file exists:
   ```bash
   ls -la $ARGUMENTS
   ```

2. Transcribe using OpenAI API:
   ```bash
   curl -s https://api.openai.com/v1/audio/transcriptions \
     -H "Authorization: Bearer $OPENAI_API_KEY" \
     -H "Content-Type: multipart/form-data" \
     -F file="@$ARGUMENTS" \
     -F model="gpt-4o-mini-transcribe" \
     -F response_format="text"
   ```

3. Display the transcription result.

## After Transcription

You can:
- Summarize the content
- Extract action items or tasks
- Create meeting notes
- Answer questions about what was discussed
- Use `/aura.act` for full processing workflow
