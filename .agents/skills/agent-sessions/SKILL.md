---
name: agent-sessions
description: >-
  Quick-reference for session bootstrap, UUID claiming, task intent
  management, and PreToolUse hook restrictions. Covers the exact command
  sequence to get from a fresh chat window to an unblocked working state.
  Use when starting a new agent session, when tools are blocked by hooks,
  or when debugging session/task gate failures.
---

# Agent Sessions

Practical guide to bootstrapping and maintaining a session in this
workspace. If the PreToolUse hook is blocking your tools, this is the
skill you need.

See also: `agent-lifecycle` skill for the full lifecycle model
(phases, chat integration, shutdown protocol).

---

## The Bootstrap Sequence

Every agent in a fresh VS Code chat window MUST run these commands
**in this exact order** before write tools will be unblocked.

**CRITICAL:** Always use the `holly session` CLI (or its `session` alias),
never the legacy `python3 scripts/...` form. The PreToolUse hook exempts
terminal commands matching `session `, `chat `, or your tracker CLI — the
`python3 scripts/...` form does NOT match and WILL be blocked.

```bash
# Step 1: Create or reclaim your session
# MUST use the `session` alias — not session
session get --name "YourRedDwarfName"
# Copy the output and run it:
export SESSION_ID=sess-XXXXXX

# Step 2: Claim your VS Code UUID
#   The UUID is shown in the BLOCKED message from the PreToolUse hook.
#   Copy it from there.
session claim <your-vscode-uuid>

# Step 3: Set your current task with intent
session task set "Description of what you are doing" \
  --intent "Specific plan for this work"

# Step 4: Verify your intent
session task verify
```

After step 4, all gated tools are unblocked.

### Common Mistakes That Cause Deadlock

- Using `session` instead of the `session` alias
  (the bootstrap regex won't match, and you'll be blocked)
- Wrapping the command in `eval "$(...)"` — this can work but is
  fragile. Prefer running `session get` and manually exporting.
- Trying `read_file` or `grep_search` before claiming the UUID —
  these ARE exempt and should work, but if they don't, the hook
  may have a bug. Report it.

### What Each Step Does

| Step | Command | What It Does |
|------|---------|-------------|
| 1 | `session get --name` | Creates or reactivates a session, sets `$SESSION_ID` in your shell |
| 2 | `session claim <uuid>` | Maps your VS Code chat window's internal UUID to your `$SESSION_ID` |
| 3 | `session task set` | Records what you're working on and why |
| 4 | `session task verify` | Confirms the intent is correct, unlocks write tools |

---

## PreToolUse Hook -- What Gets Blocked and Why

The `hook_pre_tool_use.py` script runs before every tool call. It
enforces a three-tier gate:

```text
  Tier 1: Is the VS Code UUID claimed?
    NO  --> BLOCKED (run: session claim <uuid>)
    YES --> continue

  Tier 2: Does an active session exist?
    NO  --> BLOCKED (run: session get --name "Name")
    YES --> continue

  Tier 3: Is a task set with verified intent?
    NO task        --> BLOCKED (run: session task set "..." --intent "...")
    Task but       --> BLOCKED (run: session task verify)
     not verified
    Verified       --> ALLOWED
```

### What Is Never Blocked

The following are always exempt from **all three tiers**, including
the UUID gate:

- **Read-only tools**: `read_file`, `grep_search`, `semantic_search`,
  `file_search`, `list_dir`, `get_errors`, `memory`, `manage_todo_list`,
  `tool_search_tool_regex`, `search_subagent`, `runSubagent`,
  `get_terminal_output`.
  These are exempt so agents can read code and debug bootstrap
  issues without being locked out.
- **Bootstrap CLI commands** in the terminal: any `run_in_terminal`
  command where the command text contains `session `, `chat `, or a
  bootstrap CLI name reported by the active tracker adapter. This lets
  you run the bootstrap sequence even before claiming UUIDs.
  **Important:** The match is on the alias name, not the full path.
  `session get --name "Holly"` matches. `session
  get --name "Holly"` does NOT match and will be blocked.
- **Worktree isolation blocks** are separate from session blocks --
  even with a valid session, you cannot write files on the main
  checkout. Use the adapter-specific worktree command shown by the
  block message, or the generic `git worktree` fallback.

### The UUID Problem

VS Code assigns each chat window an internal UUID (like
`fe4ad96d-cf5c-4e98-936f-9464c39b48e3`). This is NOT a session ID.
The hooks need to know which session owns which chat window, so you
must claim the UUID.

**How to find your UUID:** Try any non-exempt tool call (e.g.
`run_in_terminal` with a non-bootstrap command). If the UUID is
unclaimed, the BLOCKED message will contain it:

```
BLOCKED: Unclaimed VS Code UUID: fe4ad96d-cf5c-4e98-936f-9464c39b48e3
Run this command NOW to associate it with your session:
  session claim fe4ad96d-cf5c-4e98-936f-9464c39b48e3
```

Copy the UUID from that message and run the claim command.

---

## Task Intent Management

After each new user prompt, the `UserPromptSubmit` hook **resets
intent verification**. This means you must re-verify after every
user message that changes context.

### Commands

```bash
# Set a new task (archives any existing task automatically)
session task set "Implementing CSS migration for .25" \
  --intent "Convert AIReviewPanel.tsx to Tailwind, remove CSS section"

# Verify intent matches what you're doing
session task verify

# Clear task when done (archives it)
session task clear
```

### When to Re-verify

- After every user prompt (hook resets verification automatically)
- After changing what you're working on
- If you see a BLOCKED message about intent verification

### Quick Re-verify Pattern

If you get blocked after a user prompt but your task hasn't changed:

```bash
session task verify
```

That's it -- one command. You don't need to re-set the task unless
the work has actually changed.

---

## Common Problems and Fixes

### "BLOCKED: No active session"

Your `$SESSION_ID` is not set or the session has expired.

```bash
eval "$(session get --name "YourName")"
```

### "BLOCKED: Unclaimed VS Code UUID"

You haven't linked your chat window to your session yet.

```bash
session claim <uuid-from-error-message>
```

**Important:** `$SESSION_ID` must be set BEFORE claiming. If it's
not, run `session get` first.

### "BLOCKED: No current_task set"

You need to declare what you're working on.

```bash
session task set "Description" --intent "Plan"
session task verify
```

### "BLOCKED: Task intent not verified"

The UserPromptSubmit hook reset your verification. Just re-verify:

```bash
session task verify
```

### "session claim" exits with code 1

Three possible causes:

1. **`$SESSION_ID` not set** -- run `session get --name` first
2. **UUID already claimed by another session** -- check with
   `session list` to see who owns it
3. **UUID expired** -- pending UUIDs expire after 10 minutes.
   Try any tool call to re-register the UUID, then claim again.

### Tools blocked even after full bootstrap

Check for **worktree isolation** blocks (separate from session
blocks):

```
BLOCKED: Editing files on the main checkout is not allowed.
```

Fix: create a worktree first with the command shown in the block
message.

---

## Full Session CLI Reference

| Command | Purpose |
|---------|---------|
| `session get --name "Name"` | Create or reactivate session, print `export SESSION_ID=...` |
| `session claim <uuid>` | Map VS Code UUID to current session |
| `session status` | Show current session details |
| `session list` | List all sessions |
| `session activity` | Refresh activity timestamp |
| `session task set "desc" --intent "plan"` | Set current task and intent |
| `session task verify` | Confirm intent, unblock tools |
| `session task clear` | Archive current task |
| `session end` | End current session |
| `session sweep` | End expired idle sessions (cron) |
| `session prune` | Remove stale entries from sessions file |

---

## Session States

| State | Meaning | Transitions To |
|-------|---------|---------------|
| `active` | Agent is working (tools firing, prompts arriving) | `idle` (Stop hook) |
| `idle` | Chat window closed/stopped; session still warm | `ended` (60 min sweep) or `active` (resume) |
| `ended` | Expired; no activity for 60+ minutes | `active` (manual reactivation via `session get`) |

The `PostToolUse` hook automatically calls `update_activity()` on
every tool call, keeping `last_activity` fresh. You don't need to
manage this manually.

---

## Subagent Sessions

If you are invoked via `runSubagent`, you inherit `$SESSION_ID` from
the parent agent. Do NOT:

- Call `session get` or `session claim`
- Call `session end`
- Modify session state in any way

Just do your work and return. The parent manages everything.
