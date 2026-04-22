---
agent_name: strategy-advisor-v2
cognitive_mode: assessor
architecture: single
status: approved
created_date: 2025-06-17
---

# Strategy Advisor v2 — Agent Design Template

## Part 1: Purpose & People

| Question | Your Answer |
|---|---|
| **1.1** What is the agent supposed to do? | A collaborative business strategy advisor that helps users develop strategic clarity through dialogue — not a consultant who delivers answers, but a thinking partner who surfaces assumptions, offers multiple options, and frames strategies as testable hypotheses. It saves strategic artifacts (frameworks, analyses, templates) as markdown files to `artifacts/strategy/` for the Document Manager Agent to ingest into its knowledge base. |
| **1.2** Who will use this agent? | Semi-technical to non-technical business users — founders, strategists, product managers, consultants. They need strategic clarity, not code. |
| **1.3** What kind of cognitive work does the agent primarily do? | **Assessor** — Evaluates strategies against standards (Porter's Five Forces, SWOT, etc.) and surfaces assumptions. The human makes the final strategic decision. |

## Part 2: Architecture

| Question | Your Answer |
|---|---|
| **2.1** How complex is the task? | **Simple** — One focused task (collaborative strategy advising). Single Agent. The workflow pattern (Researcher → Analyst → Writer) is deferred as a future evolution. |
| **2.2** Sub-roles/steps? | N/A — Single agent. |

## Part 3: Data & Knowledge

| Question | Your Answer |
|---|---|
| **3.1** What information does the agent need? | • Real-time web search (market research via DuckDuckGo) • Local files (reading/writing strategy documents via FileTools) • Learning data (entity memory for companies/competitors, learned knowledge for strategic insights) — stored in PgVector |
| **3.2** Should the agent learn and remember? | **Both** — User memory (agentic memory for individual preferences across sessions) + Organizational learning (entity memory for companies/competitors shared globally, learned knowledge for strategic insights shared globally). Artifact knowledge is NOT stored here — that's the Document Manager Agent's job. |
| **3.3** Where should stored data live? | **PostgreSQL** — Shared `edgeai-postgres` instance (`postgresql+psycopg://edgeai:edgeai@localhost:5533/edgeai`). Sessions, user memory, entity memory, learned knowledge metadata, and learning vector data all use this one database. PgVector handles the vector storage for learning data. |

## Part 4: Tools & Actions

### 4.1 External Actions

| Category | Selections |
|---|---|
| 📚 Information & Research | DuckDuckGo (web search) |
| 🛠️ System & Code | FileTools (read/write local strategy files to `artifacts/strategy/`) |
| 🔧 Custom | StrategyArtifactTools (save artifact, list artifacts, read artifact — saves to `artifacts/strategy/` as markdown with front matter, lists/reads existing artifacts from that directory) |

| Question | Your Answer |
|---|---|
| **4.2** Human approval before actions? | **Only for risky actions** — The `save_artifact` function in `StrategyArtifactTools` requires user confirmation (HITL). The agent proposes an artifact, waits for the user to say "yes," then saves. Web search and file reading happen freely. |

## Part 5: Intelligence & Behavior

| Question | Your Answer |
|---|---|
| **5.1** How much "thinking"? | **Moderate reasoning** — Uses `ReasoningTools(add_instructions=True)` for step-by-step strategic analysis. Not every question needs deep reasoning, but frameworks and tradeoff analysis benefit from structured thinking. |
| **5.2** Output format? | **Markdown** — Strategy artifacts are naturally structured (headers, tables, bullet lists). The agent renders all output as Markdown. |
| **5.3** Guardrails? | • **Content moderation** — Never present speculation as certainty; always frame strategies as hypotheses to test • **Output validation** — Always surface assumptions and risks alongside recommendations • **Custom rules** — Never make financial projections without disclaimers; distinguish analysis from opinion; focus on user's specific context, avoid generic advice |
| **5.4** State across conversation? | **Yes** — Session state tracks evolving strategy context: `current_strategic_question`, `draft_artifacts`, `decisions_made`, `open_items`. The agent updates these as the conversation progresses. |

## Part 6: Deployment & Integration

| Question | Your Answer |
|---|---|
| **6.1** How will users interact? | **Web chat** (via AgentOS) and **CLI** (standalone `python strategy_advisor.py`). |
| **6.2** Model? | **Default — Ollama `glm-5.1:cloud`** (Recommended). |
| **6.3** Multi-modal? | **Text only** for now. |
| **6.4** Scheduled? | **No** — On-demand only. |
| **6.5** Observability? | **Basic** — Console logs. |

## Part 7: Skills & Specialization

| Question | Your Answer |
|---|---|
| **7.1** Domain expertise? | **Yes — Business strategy.** Porter's Five Forces, SWOT, Blue Ocean, Business Model Canvas, Value Proposition Canvas, Jobs-to-be-Done, OKRs, Ansoff Matrix, BCG Matrix, VRIO, Balanced Scorecard, Lean Startup. |
| **7.2** Role-play instructions? | "You are a collaborative strategy advisor — not a consultant who delivers answers, but a thinking partner who helps the user develop their own strategic clarity. Listen first, surface assumptions, offer multiple options, distinguish analysis from opinion, and frame every strategy as a hypothesis to test. Never present a strategy as proven. Always suggest how to validate assumptions. When the conversation produces a useful artifact, propose saving it and wait for explicit confirmation before calling save_artifact." |

## Part 8: Budget & Constraints

| Question | Your Answer |
|---|---|
| **8.1** Cost? | **Minimize cost** — Ollama model, local vector DB, no cloud API calls for core functionality. |
| **8.2** Latency? | **Conversational (a few seconds)** |
| **8.3** Environment? | **AgentOS** — Runs as part of the EdgeAI platform. |

## Technical Specification Summary

| Component | Choice | Import Path |
|---|---|---|
| Model | `Ollama(id="glm-5.1:cloud")` | `agno.models.ollama.Ollama` |
| Storage | `PostgresDb(db_url=...)` | `agno.db.postgres.PostgresDb` |
| Vector DB (Learning) | `PgVector(db_url=..., table_name="strategy_learning", embedder=OpenAIEmbedder(...))` | `agno.vectordb.pgvector.PgVector` |
| Knowledge (Learning) | `Knowledge(name="Strategy Learning", vector_db=..., contents_db=...)` | `agno.knowledge.knowledge.Knowledge` |
| Learning | `LearningMachine(entity_memory=EntityMemoryConfig(...), learned_knowledge=LearnedKnowledgeConfig(...), knowledge=...)` | `agno.learn.LearningMachine`, `agno.learn.EntityMemoryConfig`, `agno.learn.LearnedKnowledgeConfig`, `agno.learn.LearningMode` |
| Embedder | `OpenAIEmbedder(id="text-embedding-3-small")` | `agno.knowledge.embedder.openai.OpenAIEmbedder` |
| Tools | `ReasoningTools(add_instructions=True)` | `agno.tools.reasoning.ReasoningTools` |
| | `DuckDuckGoTools()` | `agno.tools.duckduckgo.DuckDuckGoTools` |
| | `FileTools(base_dir=Path("artifacts/strategy"))` | `agno.tools.file.FileTools` |
| | `StrategyArtifactTools()` | `tools.strategy_artifact_tools.StrategyArtifactTools` (custom) |

## Key Design Changes from v1

| What Changed | v1 (Current) | v2 (Upgraded) |
|---|---|---|
| **Storage** | `SqliteDb` (local file) | `PostgresDb` (shared platform DB) |
| **Vector DB** | `LanceDb` (local, separate) | `PgVector` (shared platform DB) |
| **Artifact Knowledge** | `Knowledge` with `LanceDb` (agent-owned) | Removed — artifacts saved as files, Document Manager handles KB |
| **Learning Knowledge** | Same LanceDb as artifacts | Dedicated `PgVector` table (`strategy_learning`) |
| **Save Artifact** | Bare function → `Knowledge.insert()` | `StrategyArtifactTools` Toolkit → saves markdown files with front matter |
| **LearningMachine** | Shared LanceDb for learning + artifacts | Dedicated PgVector for learning only; artifacts are files |
| **Agent Memory** | `enable_agentic_memory=True` | Same, but backed by PostgresDb instead of SqliteDb |
| **Embedder** | `OpenAIEmbedder()` (default id) | `OpenAIEmbedder(id="text-embedding-3-small")` (explicit, consistent with platform) |

## Environment Variables Required

- `OLLAMA_API_KEY` — Ollama model access
- `OPENAI_API_KEY` — OpenAI embedder for PgVector

## Python Dependencies (beyond `agno[all]`)

- `ddgs` — DuckDuckGo search
- `psycopg[binary]` — PostgreSQL driver
- `pgvector` — PgVector extension support