---
name: orchestration
description: >-
  Reference for the Orchestrator's routing tables, formula system, recovery
  playbooks, and learning mechanism. Use when the Orchestrator needs to select
  a worker agent, manage a formula, recover from delivery failure, or record
  a lesson. Complements the orchestrator-v2 agent definition.
---

# Orchestration

Reference guide for the Holly Orchestrator's delivery machinery. The
`orchestrator-v2.agent.md` file is the cockpit checklist. This skill is the
operations manual.

---

## 1. Agent Routing Table

Select the cheapest agent whose capability envelope covers the task.

| Agent | Cost tier | Capability envelope |
|-------|-----------|---------------------|
| **Haiku Worker** | 0.33× | Validation, linting, grep, schema checks, status queries, simple one-file edits with clear spec |
| **Sonnet Worker** | 1× | Implementation, refactoring, documentation, multi-file changes, API work, test writing |
| **Opus Worker** | 7.5× | Architecture, deep reasoning, ambiguity reduction, cross-system discovery, high-risk planning |
| **Starbug** | 7.5× (Opus) | Universal worker with delegation authority; owns the current session; use for complex tasks that require all tools plus delegation |
| **Explore** | varies | Read-only codebase search and Q&A; safe to run in parallel |

**Selection heuristic:**

1. Is the task read-only and search-based? → **Explore**
2. Is the spec crisp, the scope local, and the output verifiable? → **Haiku**
3. Is the task implementation, refactoring, or structured writing? → **Sonnet**
4. Does the task need deep discovery, architectural reasoning, or is it high-risk? → **Opus**
5. Does the task need full tool access + delegation? → **Starbug**

**Override triggers** — always use Opus or Starbug when:
- Root cause is unknown and the search space is large
- A wrong early decision creates downstream rework across multiple branches
- The task involves modifying agent infrastructure, workflows, or hooks
- Recovery from a failed delegation requires reasoning about what went wrong

---

## 2. Formula System

### What a formula is

A delivery pattern is a parameterised DAG of tracker issues with typed
variables, dependency edges, wave labels, and agent path hints. Patterns
let the Orchestrator instantiate repeatable delivery work without manual
decomposition on each invocation.

### Delivery pattern lifecycle

```
recognise pattern
  → check existing adapter-supported patterns
  → if match: inspect → set variables → preview → approve
  → if no match but repeatable: design → validate → instantiate → distill after delivery
  → if novel: manual decomp → wire deps → label waves → validate manually
```
Concrete commands for listing, previewing, instantiating, and distilling
patterns are adapter-specific. Read the active tracker addendum before
using this workflow.

### Formula JSON shape (for authoring)

```json
{
  "id": "formula-id",
  "title": "Human-readable name",
  "description": "When to use this formula",
  "variables": [
    { "name": "VAR_NAME", "type": "string", "description": "What it controls" }
  ],
  "issues": [
    {
      "id": "step-1",
      "title": "{{VAR_NAME}}: first step",
      "type": "feature",
      "priority": 2,
      "wave": 1,
      "agent": "Sonnet Worker",
      "depends_on": []
    },
    {
      "id": "step-2",
      "title": "Verify {{VAR_NAME}}",
      "type": "chore",
      "priority": 1,
      "wave": 2,
      "agent": "Haiku Worker",
      "depends_on": ["step-1"]
    }
  ]
}
```

### Design principles

- Every issue in a formula must have a clear verification step.
- Waves are not optional — they define the order of execution.
- Agent hints are suggestions; the Orchestrator may override when context
  changes.
- Formulas should be distilled after 2+ successful uses of the same manual
  decomposition pattern.

---

## 3. Multi-Agent Delivery Playbook

### Onboarding

Generate a self-contained onboarding prompt per agent containing:
- Identity and role in this delivery
- Epic ID and channel name
- Assigned child issue(s)
- Wave order and dependencies
- Claim instructions from the active tracker addendum
- Verification expectations
- Blocker protocol (post to channel immediately)
- Idle wait requirement
- Worktree requirement
- Do-not-start-until-BEGIN instruction

Post each prompt to the channel. Wait for all expected agents to post
"registered" or equivalent before posting BEGIN.

### Monitoring loop

```
while not all required children closed and verified:
    wait for message (bounded: 15 min then health check)
    dispatch:
        completion  → verify against tracker + git → mark done or request fix
        blocker     → diagnose → unblock or escalate
        question    → answer precisely → agent continues
        discovery   → assess impact → update plan if needed → post update
        idle        → check ready work → assign or park explicitly
        timeout     → post health-check ping → reassign if no response
    track wave transitions → announce to channel
```

Never background `chat wait`. All waits must have bounded fallback behaviour.

### Failure-recovery playbook

| Failure | First response | Escalation |
|---------|---------------|------------|
| Agent does not register within 5 min | Re-post onboarding prompt; check if agent window is alive | Reassign to a different agent or self |
| Channel silence >15 min | Post health-check ping | If no response in 5 min, check git and tracker for silent progress; reassign if nothing |
| Hook delivery stops | Check `holly hooks` output; post context manually | Restart hook dispatch if safe |
| Lost worker mid-task | Check git state; read last known commit; resume from checkpoint or restart | Create new tracker child if needed |
| Completion mismatch (agent says done; tracker not closed) | Ask agent to confirm close commands; verify git push | Close manually if agent is unreachable |
| Truth-source conflict (agent says X; tracker says Y; git says Z) | Git and tests are authoritative for code state; tracker is authoritative for work state; agent assertions require verification |

---

## 4. Learning System

After each delivery, record lessons that would change routing, formula design,
or recovery behaviour. Store them in the project memory (if the project-knowledge
skill is installed) or in a session note.

**What to record:**

- Routing decisions that turned out wrong (expected Haiku, needed Sonnet)
- Pattern gaps (needed a reusable delivery pattern that didn't exist)
- Recovery actions that worked
- Repeated failure modes

**Format (project memory node: `context/orchestration-lessons.md`):**

```yaml
---
tags: [orchestration, lessons]
last-verified: YYYY-MM-DD
status: active
---
```

Entry per lesson:
```
## YYYY-MM-DD — <brief title>

**Context:** <what task was being orchestrated>
**Decision:** <what routing/formula choice was made>
**Outcome:** <what happened>
**Lesson:** <what to do differently>
```

---

## 5. Cross-references

- `orchestrator-v2.agent.md` — agent definition, fast routing test, planning model
- `issue-tracker` skill — issue lifecycle, worktree commands
- `agent-chat` skill — channel choice, wait semantics, file-based posting
- `agent-lifecycle` skill — session boot, task intent, shutdown
- `project-knowledge` skill — project memory system
