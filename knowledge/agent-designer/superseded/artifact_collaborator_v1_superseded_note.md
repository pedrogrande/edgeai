---
title: "Artifact Collaborator v1 — Superseded"
description: "Supersession notice for the original Artifact Collaborator agent, replaced by AI Assisted Learning Designer"
artifact_type: other
created: 2026-04-21T23:20:00Z
updated: 2026-04-21T23:20:00Z
status: approved
project: AI Assisted Learning
tags: [superseded, agent, artifact-collaborator]
version: 1
---

# Artifact Collaborator v1 — Superseded

This document records the supersession of the original **Artifact Collaborator** agent
(`agents/artifact_collaborator.py`) by the **AI Assisted Learning Designer**
(`agents/ai_assisted_learning_designer.py`).

## Changes Applied

| # | Change | Old Value | New Value | Why |
|---|--------|-----------|-----------|-----|
| 1 | Name | Artifact Collaborator | AI Assisted Learning Designer | More specific — tells you the domain AND the purpose |
| 2 | Cognitive mode | aggregator | generator | The agent actively ideates, connects, and strategises — it adds beyond inputs |
| 3 | Knowledge source | File system (FileTools) | PgVector (ai_learning_artifacts table) | Document manager handles file→vector pipeline; this agent just queries |
| 4 | Front matter | No description | Added `description` field | One-line summary makes search/triage/knowledge indexing more effective |
| 5 | Artifact path | `artifacts/` | `artifacts/ai-assisted-learning/` | Path encodes the domain for document manager context |
| 6 | Artifact types | 6 types | 7 types (+ `other`) | Catch-all for uncategorized artifacts until patterns emerge |
| 7 | Session state | 5 fields | 6 fields (+ `exploration_threads`) | Track open ideation threads not yet resolved into artifacts |

## Spec Reference

- **Spec UUID**: `6e951118-d5ad-4d04-b2bf-7f194e2b1b21`
- **Design System**: `1aa42923-221f-4995-ba01-bdbf59817be7`
- **Status**: `spec_complete`