# Chore: Execution Commands

## Description

Create the execution command templates: aura.implement and aura.prime. These complete the workflow by enabling implementation from tickets and context loading.

## Tasks

### 1. Create aura.implement.md

Copy and adapt from `whisper/.claude/commands/implement.md`:

**Location**: `aura/src/aura/templates/claude/aura.implement.md`

Key functionality:
- Accept a beads task ID as argument
- Read task details via `bd show <id>`
- Create implementation plan from task description
- Execute the plan with user approval
- Offer to mark task complete when done

```markdown
# Implement from Ticket

Execute implementation work based on a beads ticket.

## Usage

```
/aura.implement <ticket-id>
```

## Instructions

1. Read ticket details:
   ```bash
   bd show $ARGUMENTS
   ```

2. Parse the ticket description for requirements

3. Create implementation plan:
   - What files need to be created/modified
   - What order to make changes
   - How to validate the work

4. Present plan to user for approval

5. Execute the plan

6. When complete, offer to mark ticket done:
   ```bash
   bd update $ARGUMENTS --status closed
   ```

## Example

```
/aura.implement aura-001
```
```

### 2. Create aura.prime.md

Copy and adapt from `whisper/.claude/commands/prime.md`:

**Location**: `aura/src/aura/templates/claude/aura.prime.md`

Key functionality:
- Read project's CLAUDE.md for context
- Read README.md for project overview
- Summarize current state for the agent
- No brain/ references (aura is simpler)

```markdown
# Prime Agent with Context

Load project context to prepare for work.

## Usage

```
/aura.prime
```

## Instructions

1. Read and summarize these files if they exist:
   - `CLAUDE.md` - Agent instructions
   - `README.md` - Project overview
   - `.aura/config.md` - Aura configuration

2. Check current beads status:
   ```bash
   bd list --status in_progress
   ```

3. Report summary:
   - Project name and description
   - Current active tasks
   - Available commands

## Output Format

```
📋 Project: [Name]
[Brief description]

🔨 Active Work:
  ◐ [task-id]: [Title]

📚 Available Commands:
  /aura.record, /aura.act, /aura.epic, ...

Ready to help! What would you like to work on?
```
```

## Acceptance Criteria

- [ ] `aura/src/aura/templates/claude/aura.implement.md` exists
- [ ] `aura/src/aura/templates/claude/aura.prime.md` exists
- [ ] aura.implement reads ticket from beads and creates plan
- [ ] aura.prime loads project context without brain/ dependencies
- [ ] Both commands handle missing files gracefully

## Notes

- aura.implement is the "do the work" command
- aura.prime is the "get oriented" command
- Keep these simpler than whisper versions (no brain system)
- These complete the full workflow: record → plan → tickets → implement
