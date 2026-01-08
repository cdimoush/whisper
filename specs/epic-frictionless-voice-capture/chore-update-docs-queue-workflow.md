# Chore: Update Documentation for Queue Workflow

## Chore Description

Update the main `README.md` to document the new queue-based workflow. Add sections explaining how to use the queue system, the three-directory structure, available commands, and example workflows. Ensure users understand both the current manual queue approach and the upcoming hotkey capture feature.

This chore makes the queue system discoverable and usable by documenting it clearly in the main project README.

## Relevant Files

Use these files to resolve the chore:

- `README.md` - Main project documentation (will be updated)
- `queue/README.md` - Reference for queue directory explanation
- `archive/README.md` - Reference for archive directory explanation
- `output/README.md` - Reference for output directory explanation
- `.claude/commands/process_queue.md` - Reference for command documentation
- `.claude/commands/queue_status.md` - Reference for command documentation

## Step by Step Tasks

IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Add "Queue-Based Workflow" section to README
- Insert a new major section after the current "What It Does" section
- Title: `## Queue-Based Workflow (New!)`
- Brief introduction paragraph explaining the shift from one-at-a-time to batch processing:
  ```markdown
  The queue system enables efficient batch processing of multiple voice memos. Instead of transcribing files one at a time, drop audio files into the `queue/` directory and process them all at once with parallel sub-agents.
  ```

### Step 2: Document directory structure
- Add subsection: `### Directory Structure`
- Explain the three-directory system:
  ```markdown
  - **queue/** - Unprocessed audio files waiting for transcription
  - **archive/** - Processed audio files (preserved for reference)
  - **output/** - Transcription results organized by intelligent title + timestamp
  ```
- Link to detailed README files in each directory:
  ```markdown
  Each directory contains a README explaining its purpose in detail.
  ```

### Step 3: Document queue commands
- Add subsection: `### Queue Commands`
- Document `/queue_status`:
  ```markdown
  **Check queue status:**
  ```bash
  /queue_status
  ```
  Shows pending audio files, total duration, and estimated processing time.
  ```
- Document `/process_queue`:
  ```markdown
  **Process all queued files:**
  ```bash
  /process_queue
  ```
  Transcribes all audio files in `queue/` using parallel sub-agents, generates intelligent titles, and moves processed audio to `archive/`.
  ```

### Step 4: Add example workflow
- Add subsection: `### Example Workflow`
- Provide step-by-step example:
  ```markdown
  1. **Add voice memos to queue:**
     - Drag and drop `.m4a` files from Voice Memos app into `queue/` directory
     - Or save recordings directly to `queue/` (hotkey support coming soon)

  2. **Check what's queued (optional):**
     ```bash
     /queue_status
     ```
     Output:
     ```
     Files queued: 3
     Total duration: ~15 minutes
     ```

  3. **Process the queue:**
     ```bash
     /process_queue
     ```
     Output:
     ```
     Processing 3 files in parallel...
     Queue Processing Complete
     Total files: 3
     Successfully processed: 3
     ```

  4. **Browse transcriptions:**
     - Check `output/` directory for organized transcriptions
     - Example directory names: `api-refactor-discussion_2026-01-08_14-30-22/`
     - Each contains a README with full transcription and metadata
  ```

### Step 5: Document output organization
- Add subsection: `### Output Organization`
- Explain intelligent titling:
  ```markdown
  Transcriptions are organized in `output/` with format:
  ```
  output/INTELLIGENT-TITLE_YYYY-MM-DD_HH-MM-SS/
  ```

  Example:
  - `api-refactor-discussion_2026-01-08_14-30-22/`
  - `standup-ideas-jan-8_2026-01-08_09-15-03/`
  - `feature-planning-auth_2026-01-07_16-45-10/`

  Titles are auto-generated based on transcription content, making past memos easy to find.
  ```

### Step 6: Add "Coming Soon" section for hotkey capture
- Add subsection: `### Coming Soon: Instant Capture`
- Briefly mention the upcoming hotkey feature:
  ```markdown
  **System-wide hotkey** (in development):
  - Press a global hotkey to start/stop recording from anywhere
  - Audio automatically saved to `queue/` with no manual file management
  - Works on macOS and Ubuntu

  **Claude command** (in development):
  ```bash
  /record_memo
  ```
  Start recording directly from within Claude Code sessions.
  ```

### Step 7: Update the existing "Claude Code Slash Commands Reference" section
- Add references to the new queue commands in the commands list:
  ```markdown
  - `/queue_status` - View pending audio files in queue
  - `/process_queue` - Batch process all queued audio files
  ```

### Step 8: Add queue workflow to table of contents (if exists)
- If README has a table of contents, add entry for "Queue-Based Workflow"
- Ensure navigation is easy to find

### Step 9: Update "Notes" section
- Add a note about the queue system:
  ```markdown
  - **Queue processing**: Process multiple voice memos at once with `/process_queue` (3-5x faster than one-at-a-time)
  ```

## Validation Commands

Execute every command to validate the chore is complete.

```bash
# Verify README has been updated
cat README.md | grep -A 5 "Queue-Based Workflow"

# Verify directory structure is documented
grep -i "queue/" README.md
grep -i "archive/" README.md
grep -i "output/" README.md

# Verify commands are documented
grep "/queue_status" README.md
grep "/process_queue" README.md

# Verify example workflow exists
grep -A 10 "Example Workflow" README.md

# Check that coming soon section exists
grep -i "coming soon" README.md
grep "/record_memo" README.md

# Verify overall structure is coherent (check line count)
wc -l README.md  # Should be significantly longer than before (50-100+ lines added)

# Manual review: Read the updated sections
less README.md
```

## Notes

- **Tone**: Keep documentation clear and concise - users should understand the queue workflow in 2-3 minutes
- **Examples**: Use realistic directory names in examples (helps users understand what "intelligent titles" look like)
- **Structure**: Organize logically: concept → directory structure → commands → workflow → organization
- **"Coming Soon" section**: Set expectations that hotkey capture is planned but not yet implemented
- **Link to architecture**: Consider adding a brief mention and link to `docs/architecture/recording-system.md` for users interested in design details
- **Visual hierarchy**: Use proper markdown heading levels (##, ###) to make scanning easy
- **Code blocks**: Use triple backticks for all commands and example output (improves readability)
- **Migration path**: Existing users familiar with `/transcribe` should understand how queue workflow complements (not replaces) single-file transcription
- **Future updates**: After hotkey implementation (Phase 2), update the "Coming Soon" section to "Instant Capture" with actual instructions
