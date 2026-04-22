---
name: design-process
description: 7-phase agent design process — DISCOVER, SCOPE, SPECIFY, REVIEW & APPROVE, GENERATE, VALIDATE, PERSIST. Load when designing a new agent or continuing an in-progress design.
metadata:
  version: "1.0.0"
  author: edgeai
  tags: ["agent-design", "process", "workflow"]
---

# Agent Design Process

You follow a 7-phase process for every agent design. Phases 1–3 are conversational.
Phase 4 is a mandatory human review gate. Phases 5–7 only proceed after approval.

## Phase Overview

| Phase | Name | Key Activity | Gate? |
|-------|------|-------------|-------|
| 1 | DISCOVER | Understand purpose, users, cognitive mode | No |
| 2 | SCOPE | Architecture, tools, knowledge, memory, storage | No |
| 3 | SPECIFY | Model, prompt, tools, knowledge, memory, guardrails | No |
| 4 | REVIEW & APPROVE | Present completed template for human approval | **Yes** |
| 5 | GENERATE | Produce complete Python agent file + setup instructions | No |
| 6 | VALIDATE | Verify imports, params, env vars, dependencies | No |
| 7 | PERSIST | Save spec to database, advance lifecycle status | No |

## When to Load Sub-Skills

Load the reference for the phase you're currently in:

- **Phase 1** → `get_skill_reference("design-process", "discover.md")`
- **Phase 2** → `get_skill_reference("design-process", "scope.md")`
- **Phase 3** → `get_skill_reference("design-process", "specify.md")`
- **Phase 4** → `get_skill_reference("design-process", "review-approve.md")`
- **Phase 5** → `get_skill_reference("design-process", "generate.md")`
- **Phase 6** → `get_skill_reference("design-process", "validate.md")`
- **Phase 7** → `get_skill_reference("design-process", "persist.md")`

## Cross-Phase Rules

1. **Never skip Phase 4** — the completed template MUST be approved before code generation.
2. **Check session state before requesting approval** — if the spec was already approved and nothing changed, don't ask again.
3. **Use your knowledge base FIRST** for API verification — only fall back to DuckDuckGo when the KB has no results.
4. **Explain technical choices in plain language** — load the `non-technical-explanations` skill when the user is non-technical.
5. **Always use Ollama models** — default `Ollama(id="glm-5.1:cloud")`. Embeddings are the only exception (use `OpenAIEmbedder`).