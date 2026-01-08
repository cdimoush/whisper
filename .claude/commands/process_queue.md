---
allowed-tools: Bash(ls:*), Bash(mv:*), Bash(mkdir:*), Bash(date:*), Bash(python:*), Bash(uv:*), Task, Read, Write, Glob
description: Process all audio files in queue directory
---

Process all audio files in the queue/ directory using parallel sub-agents.

## Instructions

1. **Discover queue files**: Use Glob to find all audio files in `queue/` with pattern `queue/*.{m4a,mp3,wav,mp4,mpeg,mpga,webm}`

2. **Handle empty queue**: If no files found, display:
   ```
   Queue is empty. Add audio files to queue/ directory.
   ```

3. **Process files in parallel**: For each audio file, spawn a Task agent (subagent_type: "general-purpose", model: "haiku") with this prompt:

   ```
   Process this audio file from the queue. Working directory: /Users/conner/dev/whisper

   Audio file: {full_path_to_audio_file}

   Steps:
   1. Transcribe the audio:
      uv run python scripts/transcribe.py "{audio_file_path}"
      Save the transcription output.

   2. Generate intelligent title from the transcription:
      uv run python scripts/generate_title.py --text "{transcription_text}"
      Save the title output.

   3. Create timestamp: Run `date +%Y-%m-%d_%H-%M-%S` and save result.

   4. Create output directory:
      mkdir -p "output/{title}_{timestamp}/"

   5. Create README.md in the output directory with this format:
      # {Title}

      **Source:** {original_filename}
      **Transcribed:** {timestamp}

      ## Transcription

      {full_transcription_text}

   6. Move processed audio to archive:
      mv "{audio_file_path}" archive/

   Report: "SUCCESS: {filename} -> output/{title}_{timestamp}/" or "FAILED: {filename} - {error}"
   ```

4. **Spawn all agents in parallel**: Use multiple Task tool calls in a single response block.

5. **Report summary** after all agents complete:
   ```
   Queue Processing Complete

   Total files: X
   Successfully processed: Y
   Failed: Z

   Output directories created in: output/
   Processed audio archived in: archive/
   ```

## Error Handling

- If a sub-agent fails, log the error but continue processing other files
- Do NOT move audio to archive if transcription fails (leave in queue for retry)
- If queue/ directory doesn't exist, create it and display empty queue message
