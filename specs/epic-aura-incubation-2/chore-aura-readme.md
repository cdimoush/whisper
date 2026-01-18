# Chore: Aura README

## Description

Create a comprehensive README.md for the aura project that explains installation, usage, and the command reference.

## Target File

**Location**: `aura/README.md`

## Structure

```markdown
# Aura

Agentic workflow layer for codebases. Voice-driven development from idea to implementation.

## What is Aura?

[Brief explanation of what aura does and why]

## Installation

### Option 1: Git Clone (Development)
[Instructions]

### Option 2: UV Tool Install (Coming Soon)
[Instructions]

## Quick Start

1. Initialize in your project
2. Record a voice memo
3. Create an epic
4. Generate tickets
5. Implement

## Commands Reference

### Voice Commands (aura.*)
| Command | Description |
|---------|-------------|
| /aura.record | Record voice memo |
| /aura.transcribe | Transcribe audio |
| /aura.act | Full transcribe + act pipeline |

### Planning Commands (aura.*)
| Command | Description |
|---------|-------------|
| /aura.epic | Create epic document |
| /aura.feature | Plan a feature |
| /aura.tickets | Convert to beads tasks |
| /aura.implement | Implement from ticket |
| /aura.prime | Load project context |

### Task Commands (beads.*)
| Command | Description |
|---------|-------------|
| /beads.status | Project overview |
| /beads.ready | Available tasks |
| /beads.start | Start task |
| /beads.done | Complete task |

## Directory Structure

After `aura init`:
[Show structure]

## Prerequisites

- Claude Code
- OpenAI API key
- sox (for recording)
- beads CLI (optional)

## Configuration

[.aura/config.md explanation]

## Examples

[Link to tests/tron as example]

## Contributing

[Brief contribution guide]

## License

[License info]
```

## Acceptance Criteria

- [ ] README.md exists at `aura/README.md`
- [ ] Installation instructions are clear
- [ ] All 12 commands are documented
- [ ] Directory structure is shown
- [ ] Prerequisites are listed
- [ ] Quick start gets users running in <5 minutes

## Notes

- Keep it concise but complete
- Link to specs for deeper details
- Include the tron example as reference
