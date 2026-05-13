---
name: issue-tracker
description: >
  Adapter-agnostic reference for the issue-tracker integration in holly.
  Covers the session protocol for claiming, tracking, and closing issues
  using whichever adapter is installed.
  For adapter-specific commands, read the matching addendum file in this
  same directory (`addendum-<adapter>.md`).
  Use whenever managing multi-session work, tracking dependencies, or
  recovering context after compaction.
---

# Issue Tracker

Holly drives issue tracking through a pluggable adapter. The active
adapter is configured in `.holly/config.toml` (`[holly] adapter = "..."`)
and decides which CLI or API actually runs.

```bash
holly adapters       # list registered adapters
holly tracker info   # show the active adapter and its capabilities
```

If the active adapter ships an addendum file in this skill directory,
read it before doing real work — it contains the concrete CLI verbs for
that backend.

---

## Decision: Issue Tracker vs TodoWrite

**Use the issue tracker when:** work spans multiple sessions, has
blockers or dependencies, or needs to survive conversation compaction.

**Use TodoWrite when:** a single-session linear task with no
cross-session persistence is required.

**Self-check question:** "Will I need this context in two weeks?"
Yes → tracker. No → TodoWrite.

---

## The IssueTrackerAdapter API

Every adapter exposes the same capability groups regardless of backend:

| Group       | Operations                                                                 |
|-------------|----------------------------------------------------------------------------|
| `issues`    | `list_issues`, `get_issue`, `create_issue`, `update_issue`, `close_issue` |
| `comments`  | `list_comments`, `add_comment`                                            |
| `worktrees` | `list_worktrees`, `create_worktree`, `remove_worktree`, `worktree_tool_name()` |
| `sync`      | `sync_push()`, `sync_pull()`                                              |
| `labels`    | `add_label`, `remove_label`                                               |
| `blockers`  | `add_blocker`, `remove_blocker`                                           |

The `null` adapter implements everything as a no-op — useful for
projects that do not want issue tracking at all.

---

## Universal Session Protocol

Regardless of adapter, every session follows the same flow:

1. **Find** the next unblocked issue.
2. **Claim** it atomically before doing any work.
3. **Add notes** as you progress (critical for compaction survival).
4. **Close** the issue with a brief reason on completion.
5. **Sync** state with `holly tracker sync` (no-op for adapters
   without a remote).

The exact CLI verbs live in the per-adapter addendum.

---

## Worktrees

All implementation work happens in a dedicated worktree — never on the
main checkout. The PreToolUse hook enforces this and the BLOCKED message
points at the canonical one-command path.

```bash
# Start work on an existing issue (claim + worktree + session in one)
eval "$(holly task start <ISSUE-ID>)"

# When work in the worktree is committed
eval "$(holly task finish)"
git push origin main
```

`holly task start` is adapter-agnostic. It calls the adapter's
`start_task` method, which uses the native worktree CLI under the hood.
Look up the adapter's addendum file in this same directory for the
low-level commands when you need them.

See `docs/worktree-workflow.md` for the full lifecycle.

---

## Recovery after compaction

```bash
holly tracker list --status in_progress      # what was I doing?
holly tracker show <id>                      # full context for the issue
```

Then re-claim or re-open the issue and continue.

---

## Adapter Addenda

Adapter packages may overlay this skill with `addendum-<name>.md` and
supporting resources. When you add a new adapter, ship a matching
addendum in that adapter package so agents can find the concrete
command surface after `holly init` or `holly skills sync`.
