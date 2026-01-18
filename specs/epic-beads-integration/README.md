# Epic: Beads Integration with Whisper

## Epic Overview

Transform Whisper from a stateless transcription tool into an agent-memory platform where voice memos become persistent, trackable work items that agents can execute across multiple sessions without losing context. This epic implements a **Hybrid Model** approach that preserves Whisper's existing vision/epic planning documents while adding Beads as an execution and memory layer. The goal is to solve agent amnesia (agents forgetting context between sessions) while maintaining human-readable strategic documentation.

This is a **discovery-driven epic** with explicit user testing breakpoints. Rather than fully committing to Beads upfront, we'll validate the integration incrementally: install and experience Beads manually, prototype the bridge between epic specs and Beads tasks, test real-world workflows across multiple sessions, and make a data-driven decision on broader rollout. Each phase includes clear success criteria and a breakpoint where we evaluate whether to proceed, iterate, or stop.

The epic follows Path 1 (Hybrid Model) from the vision: keep existing planning commands (`/vision`, `/epic`), add Beads for execution tracking and agent memory, enable multi-agent coordination, and provide graceful degradation if Beads isn't available. By the end, agents will check `bd ready` at session start to know what's next, file discoveries during implementation, and land tasks cleanly at session end—all while epic specs remain the source of truth for strategic context.

## Vision Context

**Source Vision**: [Vision: Beads Integration with Whisper](../../output/beads-integration-vision_2026-01-17_20-27-21/vision.md)

### Key Vision Points

**Current Pain Points Addressed:**
- **Session Amnesia**: Agent forgets context between sessions, wastes time re-reading specs
- **Lost Discoveries**: Subtasks/blockers discovered during implementation get forgotten
- **Blocked Work**: Agent doesn't know what's blocked, attempts out-of-order work
- **No Status Visibility**: Hard to answer "what's done?" without reading commits and specs
- **Multi-Agent Coordination**: Parallel agents have no shared memory, risk conflicts

**Vision Goals:**
1. Persistent Agent Memory - agents remember done/in-progress/blocked/next across all sessions
2. Autonomous Session Resumption - agent checks task graph, knows context immediately
3. Dependency-Aware Execution - agent cannot attempt blocked work, only sees ready tasks
4. Discovered Work Capture - agent files new tasks as discovered, prevents forgetting
5. Multi-Agent Coordination - multiple agents share memory, see each other's work
6. Git-Backed Audit Trail - every task has commit history, full traceability
7. Maintain Human Readability - keep vision/epic docs for strategic context and team communication

**Architecture Decision:**
Hybrid Model (Path 1) - keep existing planning documents, add Beads as execution layer. Specs remain source of truth for requirements, Beads tracks execution status and discovered work. This provides graceful degradation (works without Beads) and lower risk (additive change vs replacement).

## Status

**Epic Status**: ✅ Complete
**Decision**: Continue with Path 1 (Hybrid Model)
**Date Completed**: 2026-01-17

See [brain/beads-discovery/decision.md](../../brain/beads-discovery/decision.md) for full assessment.

## Specs in This Epic

### Phase 1: Foundation & Discovery
- [x] [Chore: Install and Initialize Beads](./chore-install-initialize-beads.md) - Set up `bd` CLI, initialize `.beads/`, configure git
- [x] [Chore: Manual Beads Experience](./chore-manual-beads-experience.md) - Use Beads hands-on to understand workflow
- [x] [Chore: Create AGENTS.md](./chore-create-agents-md.md) - Document Beads workflow for agents

### Phase 2: Bridge & Integration
- [x] [Feature: Bridge Command Implementation](./feature-bridge-command.md) - Create `/beads-from-epic` to convert epic specs to Beads tasks
- [x] [Feature: Workflow Integration Commands](./feature-workflow-integration.md) - Modify `/implement`, create `/land` and `/beads-status`

### Phase 3: Real-World Testing
- [x] [Chore: Multi-Session Feature Test](./chore-multi-session-test.md) - Build one feature using full Beads workflow across sessions
- [x] [Chore: Multi-Agent Coordination Test](./chore-multi-agent-test.md) - Test parallel agents with shared Beads memory

### Phase 4: Assessment & Documentation
- [x] [Chore: Create Brain Discovery Structure](./chore-brain-discovery-structure.md) - Document findings in `brain/beads-discovery/`
- [x] [Chore: Assessment and Decision](./chore-assessment-decision.md) - Make go/no-go decision on broader rollout

## Execution Order

### Phase 1: Foundation & Discovery (3-4 hours)
**Goal**: Experience Beads firsthand and establish baseline infrastructure

Execute in order:
1. [Chore: Install and Initialize Beads](./chore-install-initialize-beads.md) - Must exist before any Beads usage. Sets up CLI tool and project initialization.
2. [Chore: Manual Beads Experience](./chore-manual-beads-experience.md) - Must follow installation. Provides hands-on understanding of Beads workflow before automation.
3. [Chore: Create AGENTS.md](./chore-create-agents-md.md) - Must follow manual experience. Documents learned workflow patterns for agent reference.

**Success Criteria**:
- `bd` CLI installed and working (`bd --version` succeeds)
- `.beads/` directory initialized in whisper project
- At least 5-10 tasks manually created representing current work
- Successfully practiced `bd ready` → `bd start` → `bd done` workflow
- AGENTS.md created with Beads workflow documentation
- User understands Beads concepts: handles, dependencies, status tracking

**🔄 USER BREAKPOINT #1**: Does Beads feel promising?

**Questions to answer:**
- Is the `bd` CLI intuitive to use?
- Does creating and managing tasks feel natural or cumbersome?
- Do dependencies and status tracking seem valuable?
- Does this approach feel like it would solve agent memory problems?

**Decision criteria:**
- ✅ **Proceed to Phase 2** if: Beads CLI is usable, workflow feels cleaner than current markdown-only approach, can see path to agent integration
- 🔄 **Iterate on Phase 1** if: Need more manual practice to understand workflow, unclear on key concepts
- ❌ **Stop epic** if: Beads adds more friction than value, tool is buggy/broken, doesn't fit mental model

---

### Phase 2: Bridge & Integration (4-5 hours)
**Goal**: Automate conversion from epic specs to Beads tasks and integrate into agent workflow

**Dependencies**: Phase 1 complete

Execute in order:
1. [Feature: Bridge Command Implementation](./feature-bridge-command.md) - Core automation. Parses epic READMEs and creates matching Beads task graph.
2. [Feature: Workflow Integration Commands](./feature-workflow-integration.md) - Depends on bridge command existing. Modifies agent workflow to check Beads first.

**Success Criteria**:
- `/beads-from-epic <epic-dir>` command implemented and working
- Command correctly parses epic README "Execution Order" sections
- Creates Beads tasks matching spec structure with proper dependencies
- Links each Beads task to corresponding spec file via notes
- `/implement` modified to check `bd ready` before starting work
- `/land` command created for session-end cleanup
- `/beads-status` command created for visibility

**🔄 USER BREAKPOINT #2**: Does the bridge work correctly?

**Questions to answer:**
- Does `/beads-from-epic` correctly parse epic structure?
- Are dependencies set up correctly (blocking relationships work)?
- Does `bd ready` show the right next tasks?
- Do the integration commands (`/implement`, `/land`, `/beads-status`) feel natural?

**Decision criteria:**
- ✅ **Proceed to Phase 3** if: Bridge accurately creates task graph, dependencies work, integration commands are useful
- 🔄 **Iterate on Phase 2** if: Parsing issues, dependency logic wrong, commands need refinement
- ❌ **Rollback to Phase 1** if: Automation too complex, manual Beads usage better than bridge

---

### Phase 3: Real-World Testing (4-6 hours)
**Goal**: Validate Beads solves agent memory across real work scenarios

**Dependencies**: Phase 2 complete

Execute in order:
1. [Chore: Multi-Session Feature Test](./chore-multi-session-test.md) - Tests agent continuity. Must come first to validate single-agent workflow.
2. [Chore: Multi-Agent Coordination Test](./chore-multi-agent-test.md) - Tests shared memory. Requires multi-session workflow proven first.

**Success Criteria**:
- One real feature built across 3+ sessions using Beads workflow
- Agent successfully resumes work by checking `bd ready` at session start
- Agent files discovered subtasks during implementation
- Agent lands tasks cleanly at session end
- Multi-agent test with `/process_queue` shows coordination
- No conflicts between parallel agents
- Agents see each other's work and status

**🔄 USER BREAKPOINT #3**: Does Beads solve the agent memory problem?

**Questions to answer:**
- Does agent session resumption work (no context re-explaining)?
- Are discovered tasks captured and not forgotten?
- Do dependencies prevent out-of-order work?
- Can multiple agents coordinate via shared Beads memory?
- Is this faster/better than current workflow?

**Decision criteria:**
- ✅ **Proceed to Phase 4** if: Beads demonstrably solves agent amnesia, improves workflow, multi-agent coordination works
- 🔄 **Iterate on Phase 3** if: Partial success but needs workflow refinement, test different scenarios
- ❌ **Rollback** if: Beads doesn't improve workflow, adds overhead without benefit, breaks multi-agent

---

### Phase 4: Assessment & Documentation (2-3 hours)
**Goal**: Document findings and make informed decision on broader Beads rollout

**Dependencies**: Phase 3 complete

Execute in order:
1. [Chore: Create Brain Discovery Structure](./chore-brain-discovery-structure.md) - Captures learnings. Must precede decision.
2. [Chore: Assessment and Decision](./chore-assessment-decision.md) - Final evaluation. Requires all learnings documented.

**Success Criteria**:
- `brain/beads-discovery/` directory created with all findings
- Integration findings documented (what works, what doesn't)
- Workflow patterns documented (effective usage)
- Multi-agent notes documented (coordination findings)
- Clear recommendation: continue (Path 1), pivot (Path 2), or abandon
- If continuing: plan for broader rollout documented
- If abandoning: lessons learned documented for future reference

**🔄 USER BREAKPOINT #4**: What's the verdict on Beads integration?

**Questions to answer:**
- Does Beads justify the added complexity?
- Should we continue with Path 1 (Hybrid), pivot to Path 2 (Full), or abandon?
- What would need to change to make Beads more valuable?
- Are there alternative approaches to solve agent memory?

**Decision criteria:**
- ✅ **Continue with Beads** if: Clear evidence of improved agent continuity, faster workflows, successful multi-agent coordination
- 🔀 **Pivot to Path 2** if: Beads works well but hybrid model creates duplication, full Beads would be simpler
- ❌ **Abandon Beads** if: Doesn't solve core problems, too much complexity, alternative approaches better

---

## Path Dependencies Diagram

```
Phase 1: Foundation & Discovery (3-4 hrs)
    ├─ Install & Initialize Beads
    ├─ Manual Beads Experience (depends on installation)
    └─ Create AGENTS.md (depends on experience)
    ↓
🔄 BREAKPOINT #1: Beads promising?
    ↓
Phase 2: Bridge & Integration (4-5 hrs)
    ├─ Bridge Command (/beads-from-epic)
    └─ Workflow Integration (/implement, /land, /beads-status)
    ↓
🔄 BREAKPOINT #2: Bridge works correctly?
    ↓
Phase 3: Real-World Testing (4-6 hrs)
    ├─ Multi-Session Feature Test (single agent continuity)
    └─ Multi-Agent Coordination Test (parallel agents)
    ↓
🔄 BREAKPOINT #3: Solves agent memory?
    ↓
Phase 4: Assessment & Documentation (2-3 hrs)
    ├─ Create Brain Discovery Structure
    └─ Assessment and Decision
    ↓
🔄 BREAKPOINT #4: Final verdict?
    ↓
Decision Point:
    ├─ Continue (Path 1: Hybrid)
    ├─ Pivot (Path 2: Full Beads)
    └─ Abandon (document lessons)

Critical Path:
- Phase 1 must complete before Phase 2 (need manual understanding before automating)
- Phase 2 must complete before Phase 3 (need bridge before testing real workflows)
- Phase 3 must complete before Phase 4 (need testing results to inform decision)
- All 4 breakpoints are mandatory decision gates
```

## Implementation Notes

### Cross-Cutting Concerns

**Architecture Decisions:**
- Hybrid model preserves existing planning documents as source of truth
- Beads provides execution layer (status tracking, agent memory)
- Graceful degradation: commands work without Beads (just lose memory features)
- Git-backed: `.beads/*.jsonl` files committed, `.beads/beads.db` ignored
- Agent-first: Beads primarily benefits agents, optional for user direct interaction

**Shared Dependencies:**
- `bd` CLI tool (must be installed on all development machines)
- `.beads/` directory structure in whisper project
- `.gitignore` configured to ignore DB but commit JSONL
- AGENTS.md as reference for Beads workflow patterns
- Brain files (`brain/beads-discovery/`) for capturing learnings

**Testing Strategy:**
- Phase 1: Manual validation of Beads CLI and workflow
- Phase 2: Test bridge command on this epic itself (meta!)
- Phase 3: Real feature across multiple sessions (not toy example)
- Phase 3: Multi-agent test with actual `/process_queue` usage
- Phase 4: Comprehensive assessment with clear go/no-go criteria

**Rollout Plan:**
- Incremental adoption: start with one epic, expand if successful
- Breakpoints prevent over-investment before validation
- Documentation captures learnings for future reference
- If abandoned, brain files preserve "why we didn't adopt this"
- If continuing, brain files become permanent reference

### User Testing Breakpoints

This epic includes **4 explicit user testing breakpoints** (marked with 🔄):

1. **After Phase 1**: Does Beads feel promising? (Is manual usage valuable?)
2. **After Phase 2**: Does the bridge work correctly? (Is automation accurate?)
3. **After Phase 3**: Does Beads solve agent memory? (Real-world validation)
4. **After Phase 4**: What's the final verdict? (Continue/pivot/abandon decision)

Each breakpoint is a decision point: proceed to next phase, iterate on current phase, or stop if goals are met or approach is invalidated. This prevents over-investment in an approach that doesn't fit our workflow.

## Success Metrics

- [ ] Agent can resume work across sessions without user re-explaining context
- [ ] Agent discovers and files subtasks during implementation without forgetting
- [ ] Dependencies prevent agent from attempting out-of-order work
- [ ] `bd ready` accurately shows next available work
- [ ] Multiple agents coordinate via shared Beads memory without conflicts
- [ ] User can quickly see project status via `bd list` / `bd show`
- [ ] Clear documented decision on Beads integration with supporting evidence

## Future Enhancements

Ideas that came up during planning but are out of scope for this epic:

1. **Automatic Beads Task Creation**: `/act` processing audio creates Beads tasks for action items mentioned in voice memo
2. **Brain-Beads Linking**: Tasks reference brain files for context (e.g., task notes include "Context: brain/technical_systems.md#design-lab")
3. **Tag-Driven Task Context**: Beads tasks inherit tags from memos, enable context-aware task grouping
4. **Beads Status in Brain Summary**: `brain/summary.md` could include Beads task statistics per project
5. **Cross-Repository Beads**: Multiple repos with Beads, agents coordinate across codebases
6. **Gastown Integration**: Full multi-agent orchestrator with Whisper as interface layer
7. **Time Tracking**: Beads tasks track time spent (via commits or explicit logging)
8. **Priority Automation**: Agent suggests priority based on strategic roadmap in `brain/claudes_wants_this.md`
9. **Voice-to-Beads Direct**: Speak a voice memo, agent transcribes AND files Beads tasks, no intermediate steps
10. **Beads + Brain Sync**: Brain files become living documents updated by agents as tasks complete

---

**Status**: Epic README complete. Ready to create individual spec files.

**Next Steps**: Create individual chore and feature spec files for each item in the epic, then begin Phase 1 execution.

**Tags**: `beads` `task-management` `agent-memory` `whisper` `epic` `hybrid-model` `git-backed` `session-continuity` `multi-agent` `discovery-driven`
