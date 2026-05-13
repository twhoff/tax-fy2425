---
name: project-knowledge
description: >-
  Holly-owned memory framework for per-project knowledge. Governs how agents
  discover, store, update, and validate project-specific facts in a
  workspace-scoped memory tree. Use when starting any task in a Holly-enabled
  project, when looking up project conventions, when encountering unfamiliar
  entities or terms, or when adding new facts to the project knowledge base.
---

# Project Knowledge

**Holly owns the rails. Each project owns the cargo.**

Holly owns the memory framework: scaffold layout, file templates, lifecycle
rules, validation commands, and migration logic. Each target project owns its
memory content: glossary entries, domain rules, people notes, project facts,
and local conventions.

Agents never invent the memory structure from scratch. Holly installs it.
Agents never embed project-specific facts inside generic agent files. The
memory tree holds them.

---

## Canonical Scaffold Layout

After `holly memory install`, every Holly-enabled project has:

```
.agents/memory/
├── HOLLY_SCAFFOLD_VERSION   # version marker — do not edit
├── AGENT_MEMORY.md          # hot cache (~100 lines, top facts)
├── README.md                # explains layout to humans
├── glossary.md              # decoder ring for all project terms
├── projects/                # one file per project or sub-system
├── people/                  # one file per person, team, or system actor
└── context/                 # domain rules, conventions, constraints
```

`AGENT_MEMORY.md` is the hot cache. It is auto-loaded by the VS Code workspace
context. Keep it under 100 lines. It contains the 30 most important current
facts, the active glossary summary, and links to deep nodes.

Deep nodes live in `projects/`, `people/`, and `context/`. They are loaded
on-demand when a task references the relevant entity.

---

## Node Shape

Every node in `projects/`, `people/`, and `context/` MUST start with YAML
frontmatter:

```yaml
---
tags: [<tag1>, <tag2>]
last-verified: YYYY-MM-DD
supersedes: <relative path to old node if this replaces one, else omit>
status: active | stale | archived
---
```

Rules:
- `last-verified` is the date the agent last confirmed the content is still
  correct. Update it when you act on the node during a task.
- `status: stale` means the content needs review. Do not delete stale nodes;
  mark them and fix them.
- `status: archived` means superseded. Keep for audit trail; do not delete.
- `supersedes` creates an explicit deprecation chain. Always set it when
  replacing a node.

---

## Agent Lifecycle

### On every task start

1. **Load the hot cache.** Read `AGENT_MEMORY.md`. It is your operating
   context for this task.
2. **Identify relevant entities.** For each named system, person, concept, or
   rule that appears in the task, check whether a deep node exists.
3. **Load relevant deep nodes.** Read the matching files from `projects/`,
   `people/`, or `context/` before proceeding.

### When you encounter an unfamiliar entity

1. Search `glossary.md` and all deep node filenames first.
2. If found: load the node, follow its cross-links, and proceed.
3. If not found: this is a discovery moment. Gather the fact from context,
   existing files, or the user. Then create a new node (see Writing Nodes).

### When you finish a task

1. Check whether any facts you relied on changed or proved incorrect.
2. Update stale nodes: fix content and update `last-verified`.
3. Promote heavily-used deep facts to the hot cache if they now qualify as
   top-30.
4. Demote cold hot-cache entries to deep nodes if they are no longer top-30.

---

## Writing Nodes

### Creating a new node

1. Check for duplicates first — search `glossary.md`, `projects/`, `people/`,
   `context/` by file name and content. If a related node exists, add to it
   rather than creating a new file.
2. Choose the correct subdirectory:
   - `projects/` — systems, apps, services, codebases, epics
   - `people/` — humans, teams, external agents, system actors with personas
   - `context/` — rules, conventions, constraints, domain knowledge,
     policies, security posture
3. Name the file in `kebab-case.md` matching the entity name.
4. Write the frontmatter (see Node Shape above).
5. Write the content. Be specific. Avoid vague generalities.
6. Cross-link to related nodes using relative paths:
   `See also: [[../context/styling-policy.md]]`
7. Add a glossary entry if the entity has a name or abbreviation that will
   appear in tasks.

### Updating an existing node

1. Edit the content.
2. Update `last-verified` to today.
3. If the node has been substantially changed, add a brief `## Change log`
   section at the bottom noting what changed and when.
4. If the old node is being replaced entirely, set `status: archived` on the
   old file and create a new file with `supersedes: <old-path>`.

### Deduplication rule

Before writing, always ask: does this fact belong in an existing node? If yes,
extend the existing node. Creating duplicate nodes is worse than a slightly
overlong existing node.

---

## Staleness and Deduplication Checks

Run these checks before committing any memory tree changes:

1. **Dedup check:** Scan all node filenames and glossary entries for
   overlapping concepts. Merge or cross-link.
2. **Staleness check:** Any node with `last-verified` more than 90 days ago
   or `status: stale` needs review. Either verify and update the date, or
   archive the node.
3. **Hot cache size:** `AGENT_MEMORY.md` must stay under 100 lines. Demote
   anything that has not been used in the last 30 days.
4. **Orphan check:** Any node with no incoming cross-links and not referenced
   in the hot cache is a candidate for archiving.

---

## Validation

Run `holly memory validate` to check:
- Scaffold directories exist
- `HOLLY_SCAFFOLD_VERSION` is present and current
- `AGENT_MEMORY.md` is under 100 lines
- All deep nodes have required frontmatter fields
- No node is both `active` and listed in a `supersedes` chain

Fix every failure before committing.

---

## Upgrade

When Holly releases a new scaffold version, run `holly memory upgrade`. It
will:
- Refresh templated files (README, HOLLY_SCAFFOLD_VERSION)
- Leave all content nodes untouched
- Print a migration guide if the format changed

---

## Cross-references

- `agent-lifecycle` skill — session boot, warm-up, shutdown
- `agent-sessions` skill — task intent, PreToolUse gate
- `ax-commandments` skill — mandatory tool design rules

Holly CLI reference: `holly memory --help`
