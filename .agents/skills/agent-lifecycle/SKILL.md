---
name: agent-lifecycle
description: >-
  Complete agent lifecycle from session boot to shutdown, integrating the
  session system and chat system. Covers session registration, chat
  announcement, work loop with periodic check-ins, and clean shutdown.
  Use at the start of any agent interaction or when an agent's lifecycle
  behaviour is unreliable.
---

# Agent Lifecycle

Governs how an agent starts up, stays coordinated during work, and shuts down cleanly. This is the canonical reference for session + chat integration.

## When to Use

- At the start of any agent session (automatically via `SessionStart` hook, or manually)
- When you need to understand how session and chat systems interact
- When debugging agent lifecycle issues (stale sessions, missed messages, orphaned state)
- When onboarding a new agent type

## Decision: What Kind of Agent Are You?

```text
Are you a worker invoked via runSubagent?
  YES --> Follow "Worker Agent" path (you inherit $SESSION_ID, no lifecycle to manage)
  NO  --> Follow "Primary Agent" path (you own your session)
```

---

## Primary Agent Path

Primary agents own their session lifecycle. This includes Orchestrators, Paralegals, and any agent running directly in a VS Code chat window.

### Phase 1: Boot

The `SessionStart` hook fires automatically and runs `hooks/session_start.py`, which calls:

```python
get_or_create_session(name=os.environ.get("AGENT_NAME", "Agent"))
```

This does the right thing in every case:

| Scenario | What happens |
|---|---|
| Fresh chat window, no `$SESSION_ID` | Generates new ID, creates session, sets `$SESSION_ID` |
| `$SESSION_ID` set, session active + fresh | Updates `last_activity`, reuses session |
| `$SESSION_ID` set, session ended or stale | Reactivates session with new timestamps |
| `$SESSION_ID` set, not in file | Registers new entry with that ID |

**After boot, you MUST have a valid `$SESSION_ID` in your environment.** Every subsequent chat and tool call depends on it.

#### Verify boot succeeded

```bash
echo $SESSION_ID
# Should print: sess-XXXXXX
```

If empty, the hook didn't fire. Boot manually:

```bash
export SESSION_ID=$(session get --name "YourName")
```

The `--name` flag is mandatory. You cannot get a session without identifying yourself.

### Phase 2: Announce (orchestration only)

In multi-agent orchestration scenarios, announce yourself on the chat system. Skip this phase when working solo.

Your `$SESSION_ID` is automatically injected into every chat message, so you do not need to include it in the message body:

```bash
chat post --channel all-agents --message "Online. Ready for work."
```

If you have been assigned a task epic, also announce on that channel:

```bash
chat post --channel <epic-id> --message "Online. Claiming task."
```

### Phase 3: Check Ready Work

List unblocked tasks via the active tracker adapter:

```bash
holly tracker list --limit 10
```

If work was pre-assigned (e.g. via an onboarding prompt), skip this step and proceed directly to the work loop.

**Worktree isolation:** All implementation work happens in a dedicated worktree.
The `pre_tool_use` hook will BLOCK file writes on the main checkout and show
the exact command to create a worktree. See `docs/worktree-workflow.md` for
the full lifecycle, or the `issue-tracker` skill for adapter-specific commands.

### Phase 4: Work Loop

While working, the `PostToolUse` hook fires automatically on **every tool call** and runs `update_activity()`. This keeps `last_activity` fresh so other agents can see you're alive. You do not need to do anything for this -- it just works.

**Chat check-ins (orchestration only):** In multi-agent scenarios, periodically read chat channels for coordination messages. Use the `agent-chat` skill, which handles this:

```bash
chat read --channel all-agents
chat read --channel <epic-id>        # if you have an active epic
```

**When posting status updates:**

- Use `chat post --channel <epic-id> --message "STATUS: ..."` for task progress
- Use `chat post --channel all-agents --message "DISCOVERY: ..."` for cross-cutting findings
- Prefer `--file /tmp/chat_msg.txt` for anything longer than a simple line
- All chat messages MUST be ASCII-only (unicode breaks shell parsing)
- For non-trivial messages, use the file-based protocol: write to `/tmp/chat_<channel>_<desc>.txt` with `create_file`, then `chat post --channel <ch> --file /tmp/chat_<channel>_<desc>.txt`

**Chat message prefixes:**

| Prefix | When to use |
|---|---|
| `STATUS:` | Progress updates, completions, blockers |
| `DISCOVERY:` | Findings that affect other agents' work |
| `BEGIN:` | Starting a new task or phase |
| `DONE:` | Task complete, ready for next assignment |

### Phase 5: Idle / Standby

When you have no active work and are waiting for instructions:

```bash
chat monitor
```

This auto-detects your last active channel and polls forever (`--timeout 0`). It exits when a new message arrives. No arguments needed.

If you need to wait on a specific channel with a timeout:

```bash
chat wait --channel <epic-id> --timeout 300
```

### Phase 6: Shutdown

The `Stop` hook fires automatically and runs:

1. `idle_session()` — marks the session as `idle` in `.holly/agent-sessions.json`
   (the session is NOT terminated; the same `$SESSION_ID` can be reactivated
   by the next user prompt).
2. The hook does NOT sync the issue tracker. If you want a sync on stop,
   run `holly tracker sync` or add adapter sync to the workflow postflight
   (see `workflows/end-session.yaml`).

The distinction matters:

- `idle` — set by the Stop hook; the chat window is quiet but the session
  is preserved. Coming back in the same window resumes it.
- `ended` — set explicitly by `holly session end`; the session is closed
  and `ended_at` is stamped. Use this on intentional shutdown.

**Before shutdown, you MUST:**

1. Push all committed work: `git pull --rebase && git push`
2. File issues for remaining work via your tracker.
3. Close completed work via your tracker.
4. Post a final status message:

```bash
chat post --channel all-agents --message "Shutting down. All work pushed."
```

**Manual shutdown (if hook won't fire or you want a hard end):**

```bash
export SESSION_ID=sess-XXXXXX
holly session end
holly tracker sync
```

---

## Worker Agent Path

Workers are invoked by an Orchestrator via `runSubagent`. They are stateless and short-lived.

### Rules

1. **Inherit `$SESSION_ID`** — do not call `get_or_create_session()` or `session get`
2. **Do not write to `.holly/agent-sessions.json`** — the parent owns the session file
3. **Do not call `end_session()`** — the parent manages lifecycle
4. **Do not post to chat independently** — report results back to the parent via the handoff response
5. **Exception:** If you discover something that affects other agents' work, post `DISCOVERY:` to the epic channel

### What Workers Can Do

- Read chat channels (for context only)
- Use `$SESSION_ID` for tool attribution
- Focus entirely on the delegated task

---

## Session State Reference

Sessions are stored in `.holly/agent-sessions.json` (workspace root, gitignored).

| Field | Type | Description |
|---|---|---|
| `agent_name` | string | Display name (set via `--name`) |
| `status` | `active`, `idle`, or `ended` | Current state |
| `started_at` | ISO 8601 | Creation timestamp |
| `ended_at` | ISO 8601 / null | Completion timestamp |
| `last_activity` | ISO 8601 | Most recent tool use |

### Staleness

A session is **stale** when `last_activity` is older than 30 minutes. Stale sessions can be reactivated by the same chat window (same `$SESSION_ID`).

### CLI Quick Reference

```bash
holly session get --name "Name"     # Get or create (name mandatory), prints session ID
holly session end                   # End current session (status=ended)
holly session activity              # Refresh last_activity
holly session list                  # List all sessions
holly session status                # Show current session
holly session --json <command>      # JSON output
```

---

## Chat System Reference

All inter-agent communication goes through the `chat` CLI. Messages are posted as comments on tracker-backed channels.

### Channels

- `all-agents` — daily broadcast channel (auto-created as `all-agents-{yyyy-MM-dd}`)
- `<epic-id>` — task-specific channel (e.g. `the project-w1mw`)

### Commands

```bash
chat post --channel <ch> --message "short ASCII msg"   # simple messages
chat post --channel <ch> --file /tmp/msg.txt            # preferred for all messages
chat read --channel <ch>                                # last 5 messages with READ/NEW markers
chat read --channel <ch> --last 10                      # more context
chat wait --channel <ch> --timeout 300                  # wait for new message
chat monitor                                            # idle monitoring (auto-detects channel)
```

### Message Rules

- All messages MUST be ASCII-only (unicode breaks shell parsing)
- Prefer `--file` over `--message` for anything non-trivial
- `chat read` shows `[NEW]` markers for unread, `[you]` for own messages
- `chat wait` exits with code 0 on new message, 1 on timeout

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `SESSION_ID not set` errors | Hook didn't fire or env lost | `export SESSION_ID=$(session get --name "Name")` |
| Chat commands fail | No `$SESSION_ID` in environment | Set it as above |
| Session shows as stale | No `PostToolUse` hook running | Check hook config in `.vscode/settings.json` |
| Duplicate session IDs | Extremely unlikely (1 in 16M) | `session list` to inspect, restart chat window |
| Old session won't reactivate | `$SESSION_ID` doesn't match | Check `session --json list` for the correct ID |

---

## Related

- Session skill: `agent-sessions` — bootstrap, UUID claiming, task intent
- Chat skill: `agent-chat` — full chat CLI reference
- Issue tracker skill: `issue-tracker` — adapter-agnostic task management
- Worktree docs: `docs/worktree-workflow.md` — full worktree lifecycle
- Hook scripts: `hooks/session_start.py`, `hooks/session_end.py`, `hooks/post_tool_use.py`
- Workflow wrapper: `workflows/workflow-wrapper.yaml`
- Begin-session workflow: `workflows/begin-session.yaml` (task discovery, separate concern)
