# Beads Addendum — Persistent Task Memory for AI Agents

This file is the adapter-specific reference for the **Beads** issue
tracker (`tracker = "beads"` in `.holly/config.toml`). Read alongside
[SKILL.md](SKILL.md) for the universal protocol.

Graph-based issue tracker that survives conversation compaction. Provides
persistent memory for multi-session work with complex dependencies.

## bd vs TodoWrite

**Decision test**: "Will I need this context in 2 weeks?"
YES = bd, NO = TodoWrite.

| bd (persistent)                                  | TodoWrite (ephemeral)        |
|--------------------------------------------------|------------------------------|
| Multi-session, dependencies, compaction survival | Single-session linear tasks  |
| Dolt-backed team sync                            | Conversation-scoped          |

See [beads/resources/BOUNDARIES.md](beads/resources/BOUNDARIES.md) for the detailed comparison.

## Prerequisites

```bash
bd --version  # Requires v0.60.0+
```

- **bd CLI** installed and in `PATH`
- **Git repository** (optional — use `BEADS_DIR` + `--stealth` for
  git-free operation)
- **Initialisation**: `bd init` run once (humans do this, not agents)

## CLI Reference

- Run `bd prime` for AI-optimised workflow context (auto-loaded by hooks).
- Run `bd <command> --help` for specific command usage.

Essential commands:
`bd ready`, `bd create`, `bd show`, `bd update`, `bd close`,
`bd dolt pull`, `bd dolt push`. In Holly-managed projects,
`holly tracker sync` wraps the adapter sync operation.

## Session Protocol

1. `bd ready` — find unblocked work
2. `bd show <id>` — get full context
3. `eval "$(holly task start <id>)"` — claim + worktree + session in one;
   you're now cd'd into the worktree with write tools unblocked
4. Add notes as you work (critical for compaction survival)
5. Commit your work inside the worktree
6. `eval "$(holly task finish)"` — FF-merge into main, cd back
7. `git push origin main`
8. `bd close <id> --reason "..."` — close the issue (holly task finish
   does NOT touch the tracker, by design)
9. `bd worktree remove <path>` — clean up
10. `bd dolt push` — push to the Dolt remote (if configured)

### Low-level worktree commands (when you need them)

`holly task start` calls the adapter under the hood. The direct bd
verbs are still available:

```bash
bd worktree create <path> --branch <branch>
bd worktree list
bd worktree remove <path>
```

## Output

Append `--json` to any command for structured output. Use
`bd show <id> --long` for extended metadata.

Status icons: `○` open · `◐` in_progress · `●` blocked · `✓` closed · `❄` deferred.

## Error Handling

| Error                       | Fix                                                       |
|-----------------------------|-----------------------------------------------------------|
| `database not found`        | `bd init <prefix>` in project root                        |
| `not in a git repository`   | `git init` first                                          |
| `disk I/O error (522)`      | Move `.beads/` off cloud-synced filesystem                |
| Status updates lag          | Use server mode: `bd dolt start`                          |

See [beads/resources/TROUBLESHOOTING.md](beads/resources/TROUBLESHOOTING.md) for full details.

## Examples

**Track a multi-session feature:**

```bash
bd create "OAuth integration" -t epic -p 1 --json
bd create "Token storage" -t task --deps blocks:oauth-id --json
bd ready --json                    # Shows unblocked work
bd update <id> --claim --json      # Claim and start
bd close <id> --reason "Implemented with refresh tokens" --json
```

**Recover after compaction:**
`bd list --status in_progress --json` then `bd show <id> --long`

**Discover work mid-task:**
`bd create "Found bug" -t bug -p 1 --deps discovered-from:<current-id> --json`

## Advanced Features

| Feature              | CLI                  | Resource                                                                  |
|----------------------|----------------------|---------------------------------------------------------------------------|
| Molecules (templates)| `bd mol --help`      | [beads/resources/MOLECULES.md](beads/resources/MOLECULES.md)              |
| Chemistry            | `bd pour`, `bd wisp` | [beads/resources/CHEMISTRY_PATTERNS.md](beads/resources/CHEMISTRY_PATTERNS.md) |
| Agent beads          | `bd agent --help`    | [beads/resources/AGENTS.md](beads/resources/AGENTS.md)                    |
| Async gates          | `bd gate --help`     | [beads/resources/ASYNC_GATES.md](beads/resources/ASYNC_GATES.md)          |
| Worktrees            | `bd worktree --help` | [beads/resources/WORKTREES.md](beads/resources/WORKTREES.md)              |

## Resources

| Category         | Files                                                                                                                                        |
|------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| Getting Started  | [BOUNDARIES.md](beads/resources/BOUNDARIES.md), [CLI_REFERENCE.md](beads/resources/CLI_REFERENCE.md), [WORKFLOWS.md](beads/resources/WORKFLOWS.md) |
| Core Concepts    | [DEPENDENCIES.md](beads/resources/DEPENDENCIES.md), [ISSUE_CREATION.md](beads/resources/ISSUE_CREATION.md), [PATTERNS.md](beads/resources/PATTERNS.md) |
| Resilience       | [RESUMABILITY.md](beads/resources/RESUMABILITY.md), [TROUBLESHOOTING.md](beads/resources/TROUBLESHOOTING.md)                                 |
| Advanced         | [MOLECULES.md](beads/resources/MOLECULES.md), [CHEMISTRY_PATTERNS.md](beads/resources/CHEMISTRY_PATTERNS.md), [AGENTS.md](beads/resources/AGENTS.md), [ASYNC_GATES.md](beads/resources/ASYNC_GATES.md), [WORKTREES.md](beads/resources/WORKTREES.md) |
| Reference        | [STATIC_DATA.md](beads/resources/STATIC_DATA.md), [INTEGRATION_PATTERNS.md](beads/resources/INTEGRATION_PATTERNS.md)                         |

## Validation

If `bd --version` reports newer than `0.60.0`, this addendum may be
stale. Run `bd prime` for current CLI guidance — it auto-updates with
each bd release and is the canonical source of truth
([ADR-0001](beads/adr/0001-bd-prime-as-source-of-truth.md)).
