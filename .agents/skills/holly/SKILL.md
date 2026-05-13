---
name: holly
description: >-
  Base bootstrap skill for the Holly live orchestration platform. Use when the
  user asks for /holly, asks to bootstrap Holly, or asks to prepare
  orchestration for an issue such as "Prepare to orchestrate GRO-492". Validates
  installation, verifies adapter context, boots session and chat readiness,
  analyses task scope, and prepares parallel execution prompts.
---

# Holly

> ## ⛔ MANDATORY SKILL READS — DO THIS BEFORE ANY OTHER ACTION
>
> **You MUST read every mandatory skill file listed below before you run a
> single shell command, post a single chat message, or touch the board.**
> Skipping this step is not a shortcut — it will cost more tokens than reading
> the skills, because you will re-invent tooling that the skills already
> provide.
>
> **Mandatory reads (no exceptions, no skipping):**
>
> | File                                                | What it gives you                                                                                    |
> | --------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
> | `issue-tracker/SKILL.md`                            | Issue CRUD, board state, verdict posting                                                             |
> | active tracker addendum skill                       | Every tracker command verb for the current adapter                                                   |
> | `ui-visual-capture/SKILL.md`                        | One CLI that captures all 4 viewports in parallel; replaces all manual Playwright browser tool calls |
> | project tracker CLI skill, if the project ships one | Board queries, status updates, comments, and local tracker ergonomics                                |
>
> **DO NOT start bootstrap step 1 until all four files are open in context.**
>
> If you skip `ui-visual-capture` and then manually call `browser_resize`,
> `browser_take_screenshot`, or `browser_evaluate` to capture UI screenshots,
> you are doing it wrong. The `playwright-screenshot.mjs` CLI handles all
> viewports in one command. Read the skill. Use the CLI.

---

Adapter-agnostic bootstrap entrypoint for running Holly in any IDE or runtime.
This skill does not encode tracker-specific command verbs. It determines the
active adapter, then routes to the appropriate adapter addendum through the
issue-tracker skill.

## What This Skill Owns

Use this skill to prepare live orchestration end-to-end:

1. Validate Holly installation and runtime context.
2. Confirm the active tracker adapter and load adapter-specific guidance.
3. Bootstrap session and chat readiness.
4. Analyse the user task and select the right workflow.
5. Plan parallel execution and produce onboarding prompts for worker agents.
6. Ask the user to open agent chat windows and paste prompts.

## Trigger Phrases

Activate this skill when requests include language like:

- `/holly`
- `bootstrap holly`
- `prepare to orchestrate <issue-id>`
- `set up live orchestration`
- `start multi-agent delivery`

## Bootstrap Protocol

### 1) Validate installation and version source

Run a fast environment check before orchestration:

```bash
holly validate
holly tracker info
holly skills list
```

Then verify the installed package path and version:

```bash
HOLLY_BIN="$(command -v holly)"
ls -l "$HOLLY_BIN"

HOLLY_PY="$(cd "$(dirname "$HOLLY_BIN")" && pwd)/python"
"$HOLLY_PY" - <<'PY'
import holly
from pathlib import Path
from importlib.metadata import version
print(f"holly_version={version('holly')}")
print(f"holly_path={Path(holly.__file__).resolve()}")
PY
```

Do not assume `python` or `python3` can import `holly`. A uv-installed Holly
tool often lives in its own environment, so the sibling interpreter next to the
`holly` launcher is the reliable source of truth. This is not Codex-specific.

If the user expects the local checkout at `../holly` to be active, compare the
reported package path with that checkout and stop to fix environment drift
before planning delivery.

### 2) Detect adapter and load the correct skill set

Read the active adapter first:

```bash
holly tracker info
```

#### Mandatory skills (always load, regardless of task)

Load these on every `/holly` invocation before doing anything else:

| Skill                                 | Source          | Purpose                                                               |
| ------------------------------------- | --------------- | --------------------------------------------------------------------- |
| `issue-tracker`                       | holly package   | Issue CRUD, board state, verdict posting                              |
| active tracker addendum               | adapter package | Adapter-specific commands and tracker verbs                           |
| `ui-visual-capture`                   | project skill   | Screenshot capture for IC evidence and reviews                        |
| project tracker CLI skill, if present | project skill   | Board queries, status updates, comments, and local tracker ergonomics |

Load the active adapter addendum immediately after reading `issue-tracker/SKILL.md`.
The active tracker addendum is the authoritative source for all
tracker-specific command syntax.

If the adapter's tracker CLI reports project or company context errors, stop
guessing and consult the active tracker addendum for the exact bootstrap or
priming command before treating the output as a real blocker.

#### Orchestration-only skills (load only when coordinating parallel agents)

Load these only when the task involves spinning up worker agents or managing a
live multi-agent session:

- `agent-sessions`
- `agent-chat`
- `agent-lifecycle`
- `orchestration`

For heartbeat, IC pickup, or solo delivery tasks these four skills are not
needed and should be skipped to reduce context overhead.

### 3) Bootstrap session state

Ensure session gates are satisfied in order:

```bash
session get --name "<agent-name>"
# export SESSION_ID=...
session claim <vscode-uuid>
session task set "<task description>" --intent "<execution intent>"
session task verify
```

Critical: all later `session` and `chat` commands need `SESSION_ID` in the
environment. In Codex and similar one-shot shell runners, environment state
does not persist across separate tool calls, so prefix commands explicitly when
needed:

```bash
SESSION_ID=sess-123456 session task verify
SESSION_ID=sess-123456 chat read --channel all-agents
```

If the VS Code UUID is unknown, intentionally trigger a blocked tool call and
copy the UUID from the block message, then claim it.

### 4) Bootstrap chat state

Establish coordination channels and presence:

```bash
chat usage
chat read --channel all-agents --last 5 --include-self
chat post --channel all-agents --message "STATUS: Orchestrator online and preparing delivery plan."
chat who --channel all-agents --since 60
```

When an epic or parent issue is known, also initialize its channel and post plan
status there.

Codex-specific note: verify optional chat flags with `chat usage` or
`chat <subcommand> --help` before guessing. For example, `chat read` uses
`--last`, not `--limit`.

### 5) Analyse task and choose workflow

Parse the user task for issue IDs and intent. Then choose the workflow:

- For preparation and routing: `workflows/begin-session.yaml`
- For parallel epic delivery: `workflows/orchestrate.yaml`
- For direct implementation: `workflows/implement.yaml`

When the request is "Prepare to orchestrate <issue>", perform preparation only:
resolve scope, collect context, build agent plan, and stop at the user handoff
point before execution.

If no issue or epic ID is supplied yet, stop after installation, adapter,
session, and chat readiness. Report what is ready, what blocked, and what input
is needed next instead of inventing scope.

### 6) Produce parallel plan and onboarding prompts

Generate:

- Execution snapshot (issue, adapter, workflow, safety gates)
- Parallel decomposition with dependencies and wave order
- Model recommendations per agent
- One self-contained onboarding prompt per worker agent

Each onboarding prompt must include:

- Identity and assigned work slice
- Session bootstrap reminders
- Channel name and registration message
- Start gate: do not begin until orchestrator sends BEGIN
- Blocker protocol and wait protocol
- Completion reporting format

### 7) User handoff for live orchestration

After prompts are generated, ask the user to:

1. Open one chat window per worker agent.
2. Assign the requested model in each window.
3. Paste the matching onboarding prompt in each window.
4. Confirm all workers have posted registration in the channel.

Only after confirmation should the orchestrator post BEGIN and start active
coordination.

## Guardrails

- Stay adapter-agnostic in this skill. Route command specifics through the
  issue-tracker adapter addendum.
- Do not start execution before user confirmation when the request is
  preparation-only.
- Keep messages ASCII-safe when using direct chat message flags.
- Prefer deterministic verification commands over assumptions.
- Codex-specific: if `chat` or the active tracker CLI fails against
  `http://localhost` with `Operation not permitted` or a similar sandbox error,
  request local-network permission and retry before concluding the local server
  is down.

## Related Assets

**Mandatory skills:**

- `issue-tracker/SKILL.md`
- active tracker addendum skill for the current adapter
- `ui-visual-capture/SKILL.md` (project skill)
- project tracker CLI skill, if the project ships one

**Orchestration-only skills:**

- `agent-sessions/SKILL.md`
- `agent-chat/SKILL.md`
- `orchestration/SKILL.md`
- `agent-lifecycle/SKILL.md`

**Workflows:**

- `workflows/begin-session.yaml`
- `workflows/orchestrate.yaml`
- `workflows/implement.yaml`
