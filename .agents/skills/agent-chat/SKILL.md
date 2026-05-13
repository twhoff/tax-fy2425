---
name: agent-chat
description: >
  Comprehensive reference for agent-to-agent chat. Covers the chat CLI
  (post, read, wait, monitor), channel strategy, message protocol,
  file-based posting, monitoring patterns, and common pitfalls.
  Use whenever an agent needs to communicate with other agents.
---

# Agent Chat

Complete reference for inter-agent communication via the `chat` CLI.

mechanics, protocol, and coordination patterns.

See also: `ax-commandments` skill for mandatory tool design rules.

---

## Prerequisites

`SESSION_ID` must be set in your environment (e.g. `sess-hx48by`).
The chat script injects this into every message automatically.
You do not need to include your session ID in message bodies.

Verify: `echo $SESSION_ID` -- should print `sess-XXXXXX`.

If unset, bootstrap with: `eval "$(session get --name '<name>')"`.
The `chat` shim (`chat`) also auto-bootstraps a "Holly"
session if `$SESSION_ID` is empty, so `chat` works even from a stale
shell -- but other tools may not, so set it properly when starting real
work.

If `which chat` reports `/usr/sbin/chat`, your `PATH` is missing
`the project's bin/ directory`. Add the repo's `the project's bin/ directory` to `PATH` (it ships the
`chat` shim that wraps `chat`).

---

## CLI Reference

### Posting Messages

```bash
# Short ASCII message (under 500 chars, single line, no unicode)
chat post --channel <channel> --message "Short status update"

# File-based (PREFERRED for anything non-trivial)
# Step 1: write message to temp file
# Step 2: post with --file
chat post --channel <channel> --file /tmp/chat_<channel>_<desc>.txt

# Pipe from stdin
echo "Hello" | chat post --channel <channel> --stdin
```

**When to use each method:**

| Method | Use when |
|--------|----------|
| `--message` | ASCII-only, single line, under 500 chars |
| `--file` | Multi-line, contains special chars, or over 500 chars |
| `--stdin` | Piping output from another command |

**Hard rule:** Messages MUST be ASCII-only. Unicode breaks shell parsing.
For non-ASCII content, use the file-based protocol with `create_file`.

### Reading Messages

```bash
# Last 5 messages (default)
chat read --channel <channel>

# Last N messages
chat read --channel <channel> --last 10

# Include your own messages in the output
chat read --channel <channel> --include-self

# Machine-readable output
chat read --channel <channel> --format json
```

**Message markers in output:**

| Marker | Meaning |
|--------|---------|
| `[NEW]` | Unread message from another agent |
| `[you]` | Your own message (only with `--include-self`) |
| *(none)* | Previously read message shown for context |

**Example output:**
```
--- the project-w1mw (the project-w1mw) | 10 total, 2 new ---
  [19:38 AEDT] sess-a975a0: Agent 1 online.
  [19:40 AEDT] sess-5e6593: Agent 2 online.
  [19:41 AEDT] sess-a975a0: BEGIN: start work now.
  [20:28 AEDT] sess-a975a0: Task complete. [NEW]
  [20:42 AEDT] sess-a975a0: Nice working with you. [NEW]
--- 2 new message(s) ---
```

### Waiting for Messages

```bash
# Default: wait up to 5 min, poll every 10s
chat wait --channel <channel>

# Custom timeout and interval
chat wait --channel <channel> --timeout 120 --interval 5

# Wait forever (standby mode)
chat wait --channel <channel> --timeout 0
```

**Behaviour:** Reads any unread messages first (exits immediately if
found), then polls at `--interval` seconds until a new message arrives
or `--timeout` elapses.

**Timeout semantics:**
- `--timeout 0` -- wait forever (correct for standby mode)
- `--timeout 300` -- wait at most 5 minutes (default)

**Guardrails (validated at parse time):**
- `--interval` must be >= 1 (prevents tight-loop polling)
- `--interval` must be <= `--timeout` (unless `--timeout 0`)
- Negative values are rejected

**Exit codes:**
- `0` -- new message received
- `1` -- timeout elapsed, no new messages
- `2` -- validation or runtime error

**Progress:** Prints a status line every ~60s so you know it's alive.

### Monitoring (Idle Mode)

```bash
# Auto-detect last active channel, wait forever
chat monitor
```

Equivalent to `chat wait --channel <last-channel> --timeout 0` but
auto-detects the channel from your most recent post/read/wait.
No arguments needed. Use this for standby between tasks.

---

## Channels

### all-agents

Broadcast channel for cross-cutting announcements and coordination.
Backed by a daily tracker channel: `all-agents-{yyyy-MM-dd}`.
Auto-created by the chat script if it doesn't exist.

Use for:
- Announcing you're online/offline
- Cross-cutting discoveries that affect multiple agents
- Orchestrator broadcasts (progress updates, wave transitions)

### Epic channels

Each epic gets its own channel using the tracker item's ID as the
channel name (e.g. `the project-va8u`). Use for task-specific coordination.

Use for:
- Task assignments and claim announcements
- Progress updates, completions, blockers
- Review requests and verdicts
- Worker-to-worker coordination within the same epic

---

## Message Protocol

### Prefixes

Prefix messages with a type tag for quick scanning:

| Prefix | When to use |
|--------|-------------|
| `STATUS:` | Progress updates, task completions |
| `DISCOVERY:` | Findings that affect other agents |
| `BEGIN:` | Starting a new task or phase |
| `DONE:` | Task fully complete |
| `BLOCKER:` | Stuck, need help |
| `HEALTH-CHECK` | Orchestrator pinging for liveness |

### Grind Pipeline Messages

The grind pipeline uses its own message protocol with messages like
`REVIEW-READY`, `REVIEW-VERDICT`, `LANDED`, `ASSIGN`, etc.
See the `grind` skill for the full protocol reference.

### Relaying User Messages

When the user asks you to post on their behalf, prefix with their
name under your session ID:

```bash
chat post --channel <ch> --message "[Thomas] The message text here"
```

---

## File-Based Posting Protocol

For anything beyond a simple ASCII line, use this protocol:

1. Write the message body to a temp file:
   ```
   create_file /tmp/chat_<channel>_<description>.txt
   ```

2. Post with `--file`:
   ```bash
   chat post --channel <channel> --file /tmp/chat_<channel>_<description>.txt
   ```

**Why:** The `--message` flag passes through zsh, which mangles
quotes, special characters, and multi-line content. The file-based
protocol bypasses shell parsing entirely.

**Naming convention:** `/tmp/chat_<channel>_<brief-description>.txt`

---

## Periodic Check-in Pattern

During active work, check for new messages periodically. The
PostToolUse hook does this automatically every ~15 seconds though
hook-delivered output. If hooks are not firing:

```bash
# Manual check-in (every 3-5 tool calls)
chat read --channel all-agents --last 5
chat read --channel <epic-id> --last 5    # if on an active epic
```

**What to do with messages:**
- Coordination requests: respond on the channel
- Questions: answer or escalate to user
- Blockers from others: assess if you can help
- Assignments: acknowledge and begin work

---

## Monitoring Patterns

### Active Orchestration

When coordinating multiple agents on an epic:

```bash
# Poll with bounded timeout
chat wait --channel <epic-id> --timeout 300 --interval 10

# Process messages, dispatch work, repeat
```

Use `--timeout 300` (5 min), not `--timeout 0`, so you can
periodically check for silent agents and run health checks.

### Idle Standby

When waiting for instructions with no active work:

```bash
chat monitor
```

This auto-detects your last channel and waits forever.

### Joining a Channel on Request

When the user asks you to "join chat" or "hop on the channel":

1. Read recent messages: `chat read --channel <ch> --last 20 --include-self`
2. Announce presence: `chat post --channel <ch> --message "Online. What have I missed?"`
3. Summarise unread to the user in the VS Code panel
4. Enter polling loop: `chat wait --channel <ch> --timeout 0 --interval 10`
5. Stay on the channel until dismissed
6. During quiet periods: be sociable -- share what you're working on,
   ask what others are up to, offer help

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Unicode in `--message` | Shell parsing breaks | Use `--file` for non-ASCII |
| Forgetting `--include-self` | Can't see own messages when debugging | Add flag when reviewing conversation |
| `--timeout 0` during orchestration | Never runs health checks | Use `--timeout 300` and loop |
| Posting to unsupported channels | The tracker adapter rejects it | Use valid epic or broadcast channels |
| Tight polling (`--interval 0`) | Wastes resources, rejected by CLI | Minimum interval is 1s |
| Not reading before posting | Duplicate or conflicting messages | Always read first |
| Manual channel tracking | Forget which channel you're on | Use `chat monitor` |

---

## Quick Reference Card

```
POST:  chat post --channel <ch> --message "short ASCII"
       chat post --channel <ch> --file /tmp/chat_<ch>_desc.txt
READ:  chat read --channel <ch> --last 10 --include-self
WAIT:  chat wait --channel <ch> --timeout 300 --interval 10
IDLE:  chat monitor
```
