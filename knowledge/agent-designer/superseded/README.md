# Superseded Agent Specs

This directory archives **deprecated or replaced versions** of agent spec templates.

## Naming Convention

When an agent spec is superseded by a new version, the old version is moved here **before** the new version is written to `agent-spec-templates/`.

File naming format:

```
{agent-name-kebab}-v{N}-template.md
```

Where `N` is a monotonically increasing integer starting at `1`.

Example:
```
customer-support-v1-template.md   ← superseded
customer-support-v2-template.md   ← superseded
customer-support-template.md      ← current (in agent-spec-templates/)
```

## Front Matter

Every superseded file retains its original YAML front matter, with one additional field:

```yaml
---
agent_name: Customer Support Agent
cognitive_mode: generator
architecture: single
status: superseded
superseded_by: customer-support-template   # filename of the replacement (no extension)
superseded_date: 2025-07-15
created_date: 2025-07-10
---
```

| Field | Purpose |
|-------|---------|
| `status` | Always `superseded` — distinguishes from `approved`, `draft`, etc. |
| `superseded_by` | Filename (without `.md`) of the template that replaced this one |
| `superseded_date` | Date the version was archived |

## Why Keep Old Versions?

1. **Rollback** — If a new design direction fails, the previous version is recoverable
2. **Audit trail** — Design decisions evolve; archived specs show *what changed and when*
3. **Learning** — Past designs (including failed ones) are training data for future agent design
4. **Accountability** — Every spec version is traceable to its origin

## Rules

- **Never delete** a superseded spec. Archive it here.
- **Always update** the front matter with `status: superseded`, `superseded_by`, and `superseded_date`.
- **Only the current version** lives in `agent-spec-templates/`. All others live here.
- **Version numbering** is sequential integers (`v1`, `v2`, …), not dates or hashes.