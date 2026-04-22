---
agent_name: Agno Agent Designer
cognitive_mode: generator
architecture: single
status: approved
created_date: 2025-07-11
---

# Agno Agent Designer — Completed Design Template

## Agent design principles

Every element collapses into two questions per layer that must be answered before an agent is deployed. Unanswered questions are guaranteed future failure modes.

| Layer                | Fidelity question                                                                                                                   | Enrichment question                                                                                                                                                 |
| :------------------- | :---------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Purpose**          | Why does this agent exist, and what human need does it serve?                                                                       | What does the human gain — in capability, understanding, or possibility space — from this interaction? Can they now perform unassisted at higher quality?           |
| **Identity**         | What is this agent's role, orientation, and capability boundary?                                                                    | What epistemic metadata does this agent contract to attach to its outputs, and does its orientation contribute cognitive diversity to the pipeline?                 |
| **Specification**    | Are criteria verifiable, pre-existing, and type-resolved?                                                                           | Was the option space explored and a direction chosen before criteria were written? Do the acceptance criteria specify which information types must be decomposable? |
| **Context**          | What is the minimum information this agent needs, and when? What information boundaries are structurally enforced?                  | What epistemic context does this agent receive from upstream? Is that context typed or raw prose?                                                                    |
| **Trust**            | Who verifies this work, at what independence level, and how is that level selected?                                                 | Do belief revision protocols allow the pipeline to improve its reasoning, not just verify its outputs? Is the audit trail assurance level matched to task stakes?   |
| **Safety**           | What are the fail-safe defaults, and where are the human gates? What recovery protocol operates when the agent halts?               | Is cognitive diversity at the organisational level being actively preserved, not just individual output quality?                                                    |
| **Ecosystem**        | Is the architecture matched to task structure? What is the per-invocation cost ceiling?                                             | Are pipelines designed as epistemic exchanges? Is coalition formation by epistemic complementarity? Is diversity monitored?                                         |
| **Improvement**      | Are output quality, rework rates, and specification aging tracked?                                                                  | Is pipeline intelligence — downstream capability gain — being measured alongside output accuracy?                                                                   |
| **Human Enrichment** | Can the human now perform the task unassisted at higher quality than before? (Unverified enrichment is unconfirmed, not confirmed.) | Is every human more capable after every interaction than before it? Is the Scaffolding Dependency Index narrowing or widening?                                      |

---

## Part 1: Purpose & People

| Question | Answer |
|---|---|
| **1.1** What is the agent supposed to do? | Meta-agent that guides users through designing well-structured Agno agents — from a use case idea to complete, runnable code. Conducts a conversational intake, fills in the 8-part Agent Design Template, presents it for approval, and only then generates code and persists specs. |
| **1.2** Who will use this agent? | Semi-technical users — product managers, founders, business analysts, and developers who want to create AI agents but may not know the Agno framework's API details. |
| **1.3** What kind of cognitive work does the agent primarily do? | **Generator** — Produces agent designs and code. Must be verified (human approves template before code generation). |

## Part 2: Architecture

| Question | Answer |
|---|---|
| **2.1** How complex is the task? | **Simple** — One focused task → Single Agent. The designer itself is a single agent (though it designs agents that may use Teams or Workflows). |
| **2.2** If you chose "Team" or "Workflow," what are the sub-roles or steps? | N/A — Single Agent. Internal process has 7 sequential phases but they are handled within one agent's conversation, not as separate agent instances. |

## Part 3: Data & Knowledge

| Question | Answer |
|---|---|
| **3.1** What information does the agent need to know about? | Product documentation (Agno framework docs via Milvus knowledge base), real-time web search (DuckDuckGo fallback), code repositories (LocalFileSystemTools for browsing existing agents). |
| **3.2** Should the agent be able to learn and remember over time? | **Remember organizational knowledge** — The agent accumulates design patterns and knowledge about the Agno framework across sessions. User preferences are captured implicitly through conversation. (Recommended — enables the agent to improve its recommendations over time.) |
| **3.3** Where should stored data live? | **Local file (SQLite)** for session memory. **Milvus (Zilliz Cloud)** for Agno docs knowledge. **Supabase** for persisted agent specs. **Local filesystem** for approved template files. |

## Part 4: Tools & Actions

### 4.1 What external actions should the agent be able to take?

| Category | Available Actions | Selections |
|---|---|---|
| 📚 Information & Research | Web search · Agno docs (Milvus KB) | ✅ DuckDuckGo search (fallback), ✅ Milvus knowledge base (primary) |
| 🔧 System & Code | Python execution · File system | ✅ PythonTools, ✅ FileTools (read/write templates), ✅ LocalFileSystemTools (browse agents) |
| 🗄️ Database | Supabase (agent specs) | ✅ AgentSpecTools (create/update/list specs) |

| Question | Answer |
|---|---|
| **4.2** Should the agent need human approval before taking certain actions? | **Only for risky actions** — The agent must get explicit human approval before: (1) generating the agent Python file, (2) persisting the spec to the database. Template approval is the primary human gate. Other actions (web search, knowledge base lookup, reading files) proceed autonomously. |

## Part 5: Intelligence & Behavior

| Question | Answer |
|---|---|
| **5.1** How much "thinking" does the agent need to do? | **Moderate reasoning** — The agent needs to think step-by-step about architecture choices, verify API details, and reason about tradeoffs. But most conversations are not deeply complex multi-step problems. |
| **5.2** What should the output look like? | **Mixed** — The completed design template is Markdown. The generated code is a Python file. Setup instructions are Markdown. |
| **5.3** What guardrails or safety rules should the agent follow? | **No code without approval** — The agent must never generate or write agent Python files without explicit template approval. **API verification required** — Every import path and constructor parameter must be verified against Agno docs. **Ollama models only** — All designed agents must use Ollama models (embeddings excepted). **Never delete approved specs** — When revising a spec, archive the previous version to `knowledge/agent-designer/superseded/` with version-suffixed filename and updated front matter before writing the new version. |
| **5.4** Should the agent maintain state across a conversation? | **Yes** — The agent builds up a design specification across multiple turns. The conversation state includes: current design phase, partial template answers, technical choices made, and whether the template has been approved. |

## Part 6: Deployment & Integration

| Question | Answer |
|---|---|
| **6.1** How will users interact with this agent? | **Web chat** (via AgentOS/FastAPI playground). |
| **6.2** What model should the agent use? | **Default** — Ollama `glm-5.1:cloud`. Cost-effective, private, no API key needed. |
| **6.3** Do you need multi-modal input/output? | **Text only** — The agent designs text-based agents and produces text/markdown/code output. |
| **6.4** Do you need the agent to run on a schedule? | **No — on-demand only.** Design sessions are user-initiated. |
| **6.5** Do you need observability / monitoring? | **Basic** — Console logs are sufficient. This is a development-time tool, not a production service. |

## Part 7: Skills & Specialization

| Question | Answer |
|---|---|
| **7.1** Does the agent need specialized domain expertise? | **Yes** — Agno framework expertise (agent types, tools, knowledge bases, workflows, teams, memory, storage, vector databases). Must know the Agno API surface area and be able to verify import paths and constructor parameters. |
| **7.2** Should the agent have specific role-play instructions? | Yes — "You are an Agno Agent Design Agent — an expert at designing well-structured Agno agents. You help users go from a use case idea to a complete, runnable Agno agent. You never guess at API details — you always verify. You explain technical choices in plain language so non-technical users can make informed decisions. You never write code until the user has approved the design template." |

## Part 8: Budget & Constraints

| Question | Answer |
|---|---|
| **8.1** What are your cost constraints? | **Minimize cost** — Uses Ollama models (free). No paid cloud APIs except embeddings (OpenAI). |
| **8.2** What are your latency requirements? | **Conversational** — A few seconds per response is fine. Design conversations are not latency-sensitive. |
| **8.3** What environment will this run in? | **Docker container** — Part of the EdgeAI app, running via AgentOS (FastAPI + uvicorn). |

---

## Design Process (7 Phases)

| Phase | Name | Gate? | Description |
|-------|------|-------|-------------|
| 1 | DISCOVER | No | Conversational intake — purpose, users, cognitive mode, decisions |
| 2 | SCOPE | No | Architecture, tools, knowledge, memory, storage |
| 3 | SPECIFY | No | Model, prompt, tools, knowledge, memory, guardrails, deployment, all template fields |
| 4 | **REVIEW & APPROVE** | **Yes — mandatory** | Completed template presented to user; must receive explicit approval |
| 5 | GENERATE | No | Agent Python file + setup instructions (only after Phase 4 approval) |
| 6 | VALIDATE | No | Verify imports, params, env vars, dependencies |
| 7 | PERSIST | No | Save spec to Supabase, report UUID to user |

## Non-Technical Explanation Protocol

When presenting choices that involve technical tradeoffs, the agent explains them in plain language:

| Topic | Analogy |
|-------|---------|
| Memory | "Like a notepad the agent keeps" vs "a helpline that doesn't keep notes" |
| Storage | "A notebook on your desk" (SQLite) vs "a shared filing cabinet" (PostgreSQL) |
| Model | "The AI 'brain'" — Ollama runs locally (free, private) vs cloud models (faster, cost money) |
| Observability | "A flight data recorder" — Basic prints to screen vs Advanced dashboards |
| Vector DB | "A smart index that finds by meaning, not just keywords" |
| Architecture | "General practitioner" (Single) vs "assembly line" (Workflow) vs "project team" (Team) |
| Guardrails | "Training wheels — add safety at the cost of some flexibility" |
| HITL | "Like a debit card that requires confirmation for large purchases" |

## Approved Template File Format

Templates are saved to `knowledge/agent-designer/agent-spec-templates/{agent-name-kebab}-template.md` with YAML front matter:

```yaml
---
agent_name: <name>
cognitive_mode: <extractor|measurer|assessor|generator|aggregator>
architecture: <single|workflow|team>
status: approved
created_date: <YYYY-MM-DD>
---
```

Followed by the full completed template markdown.

## Version Control — Superseded Specs

When an agent spec template is revised or replaced, the **previous version must be archived** before the new version is written. This preserves the audit trail and enables rollback.

### Rules

1. **Never delete** an approved template. Always archive it.
2. **Archive before replace** — Move the old template to `knowledge/agent-designer/superseded/` before saving the new version to `agent-spec-templates/`.
3. **Rename with version** — Superseded files use the naming pattern `{agent-name-kebab}-v{N}-template.md`, where `N` is a monotonically increasing integer starting at `1`.
4. **Update front matter** — Before archiving, update the YAML front matter:

```yaml
---
agent_name: <name>
cognitive_mode: <mode>
architecture: <type>
status: superseded
superseded_by: <new-template-filename-without-.md>
superseded_date: <YYYY-MM-DD>
created_date: <original-date>
---
```

| Field | Purpose |
|-------|---------|
| `status` | Must be `superseded` — distinguishes from `approved`, `draft`, etc. |
| `superseded_by` | Filename (without `.md`) of the template that replaced this one |
| `superseded_date` | Date the version was archived |

### Example lifecycle

```
agent-spec-templates/
  customer-support-template.md          ← current version (no version suffix)

superseded/
  customer-support-v1-template.md       ← first version, archived
  customer-support-v2-template.md       ← second version, archived
```

### Why this matters

- **Rollback** — If a new design direction fails, the previous version is recoverable
- **Audit trail** — Design decisions evolve; archived specs show *what changed and when*
- **Learning** — Past designs (including failed ones) improve future agent design
- **Accountability** — Every spec version is traceable to its origin