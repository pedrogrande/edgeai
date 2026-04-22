# Current Architecture

## Runtime

| Component | Detail |
|-----------|--------|
| Framework | [Agno](https://docs.agno.com) (`agno[all]`) |
| App server | `AgentOS` — wraps FastAPI + auto-discovered agents |
| Entry point | `edgeai.py` → `uvicorn edgeai:app` |
| Agent discovery | Auto-loads every `.py` in `agents/` at startup |
| MCP auto-connect | Public `MCPTools` instances in agent files are connected/closed via FastAPI lifespan |

---

## Infrastructure (Docker)

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| `edgeai-postgres` | `pgvector/pgvector:pg17` | `5533` | Primary database — sessions, memory, pgvector knowledge |
| `edgeai-toolbox` | Google MCP Toolbox `1.1.0` | `5001` | MCP server exposing Agno docs DB tools via `tools.yaml` |

---

## Databases

| Store | Type | Used by | Purpose |
|-------|------|---------|---------|
| PostgreSQL (Docker) | `PostgresDb` + `PgVector` | `edgeai.py` | Shared session/memory storage + vector knowledge (OpenAI embedder, `text-embedding-3-small`) |
| SQLite (`data/agent_designer_memories.db`) | `SqliteDb` | `agent_designer` | Agent session memory |
| SQLite (`data/strategy_advisor.db`) | `SqliteDb` | `strategy_advisor` | Agent session + knowledge metadata |
| LanceDB (`tmp/lancedb_strategy`) | `LanceDb` | `strategy_advisor` | Local vector store for strategy artifacts |
| Milvus / Zilliz Cloud | `Milvus` | `agent_designer` | Cloud vector store for Agno docs knowledge |
| Supabase (PostgreSQL) | `psycopg` direct | `AgentSpecTools` | Stores completed agent specs |

---
## Knowledge Bases

| Name | Vector DB | Embedder | Used by |
|------|-----------|---------|---------|
| Agno Docs (EdgeAI) | `PgVector` (`agno_docs` table) | `OpenAIEmbedder` (`text-embedding-3-small`) | `edgeai.py` shared knowledge |
| Agno Docs (Agent Designer) | `Milvus` (`agno_docs` collection, Zilliz Cloud) | Default | `agent_designer` |
| Strategy Artifacts | `LanceDb` (`strategy_artifacts` table) | `OpenAIEmbedder` | `strategy_advisor` |

## Design Artifact Storage

| Directory | Format | Used by | Purpose |
|-----------|--------|---------|---------|
| `knowledge/agent-designer/agent-spec-templates/` | Markdown + YAML front matter | `agent_designer` | Approved agent design templates (saved after Phase 4 approval) |

---

## Agents

### `agent_designer` (`agents/agent_designer.py`)
Meta-agent that designs Agno agents from user requirements.

| Config | Value |
|--------|-------|
| Model | `Ollama(id="glm-5.1:cloud")` |
| Storage | `SqliteDb` |
| Knowledge | `Milvus` (Zilliz Cloud) |
| `search_knowledge` | `True` |
| `update_memory_on_run` | `True` |
| `read_chat_history` | `True` |

**Design Process (7 phases):**

| Phase | Name | Description |
|-------|------|-------------|
| 1 | DISCOVER | Conversational intake — purpose, users, cognitive mode |
| 2 | SCOPE | Architecture, tools, knowledge, memory, storage |
| 3 | SPECIFY | Model, prompt, tools, knowledge, memory, guardrails, deployment |
| 4 | **REVIEW & APPROVE** | **Mandatory human gate** — completed template presented for approval |
| 5 | GENERATE | Agent Python file + setup instructions (only after approval) |
| 6 | VALIDATE | Verify imports, params, env vars, dependencies |
| 7 | PERSIST | Save spec to Supabase via AgentSpecTools |

**Key behaviours:**
- Technical choices (storage, memory, model, etc.) are explained in plain language with analogies for non-technical users
- The completed Agent Design Template must be explicitly approved before code generation
- Approved templates are saved to `knowledge/agent-designer/agent-spec-templates/` as markdown with YAML front matter

**Tools:**

| `LocalFileSystemTools` | `agno.tools.local_file_system` | Browse `./agents` directory |

---
| `DuckDuckGoTools` | `agno.tools.duckduckgo` | Web search fallback |
| `FileTools` | `agno.tools.file` | Read/write files (incl. saving approved templates) |
| `PythonTools` | `agno.tools.python` | Execute Python snippets |
| `LocalFileSystemTools` | `agno.tools.local_file_system` | Browse `./agents` directory |
| `LocalFileSystemTools` | `agno.tools.local_file_system` | Browse `./agents` directory |

---

### `strategy_advisor` (`agents/strategy_advisor.py`)
Conversational business strategy advisor that saves artifacts to a knowledge base.

| Config | Value |
|--------|-------|
| Model | `Ollama(id="glm-5.1:cloud")` |
| Storage | `SqliteDb` |
| Knowledge | `LanceDb` (local) |
| Learning | `LearningMachine` with `EntityMemoryConfig` + `LearnedKnowledgeConfig` |

**Tools:**

| Tool | Source | Purpose |
|------|--------|---------|
| `ReasoningTools` | `agno.tools.reasoning` | Deep structured analysis |
| `DuckDuckGoTools` | `agno.tools.duckduckgo` | Market research search |
| `FileTools` | `agno.tools.file` | Read/write strategy documents |
| `save_artifact` | Custom function | HITL-gated save to knowledge base |

---

## Custom Tools (`tools/`)

### `AgentSpecTools` (`tools/agent_spec_tools.py`)
Agno `Toolkit` for persisting agent specs to Supabase. Used by `agent_designer`.

| Tool method | Purpose |
|-------------|---------|
| `create_design_system` | Create a named design system container |
| `create_agent_spec` | Persist a completed spec JSON |
| `derive_spec_metadata` | Auto-populate pip deps, env vars, setup notes |
| `set_spec_status` | Advance lifecycle: `draft → spec_complete` |

**Required env vars:** `SUPABASE_DB_URL`, `AGENT_SPEC_USER_ID`, `AGENT_SPEC_DESIGN_SYSTEM_ID`

### `local_agno_docs_db.py` (`tools/local_agno_docs_db.py`)
Async context manager wrapping `MCPToolbox` for the Agno docs MCP server.

| Toolset | Purpose |
|---------|---------|
| `agno-docs-search` | Search features/pages by keyword |
| `agno-docs-browse` | Get feature details, colocated pages |
| `agno-docs-changes` | Recent changelog entries |

---

## MCP Server (`db/tools.yaml` → `edgeai-toolbox`)

Exposes the local Agno docs PostgreSQL database as MCP tools.

| Tool | SQL target | Purpose |
|------|-----------|---------|
| `search-features` | `features` + `categories` | Keyword search on feature name/description |
| `get-feature-by-category` | `features` + `doc_pages` | All features + URLs in a category |
| `get-feature-details` | `features` + `doc_pages` | Full details for a single feature slug |
| `get-colocated-pages` | `doc_page_relations` | Related pages for a given URL |
| `search-doc-pages` | `doc_pages` | Search page titles/summaries |
| `get-recent-changes` | `changelog` | Recent DB changes |
| `list-categories` | `categories` | All top-level categories |

---

## Agno Docs Database Schema (`db/schema.sql`)

| Table | Purpose |
|-------|---------|
| `categories` | Top-level feature groupings (21 categories) |
| `features` | Individual Agno features with type + experimental flag |
| `doc_pages` | Doc page URLs with type, title, summary |
| `doc_page_relations` | Relations between pages (`colocated`, `related`, etc.) |
| `changelog` | Immutable append-only audit log |

**Seed scripts:**
- `db/seed_agno_docs.py` — seeds from `docs/agent-design/Agno-features.md`
- `db/seed_base_docs_csv.py` — seeds from `docs/agent-design/agno-base-docs.csv` (URL-inferred feature matching)

---

## Environment Variables

| Variable | Required by | Purpose |
|----------|------------|---------|
| `OPENAI_API_KEY` | `edgeai.py`, `strategy_advisor` | OpenAI embedder |
| `OLLAMA_API_KEY` | All agents | Ollama model access |
| `ZILLIZ_CLOUD_HOST` | `agent_designer` | Milvus/Zilliz Cloud URI |
| `ZILLIZ_CLOUD_TOKEN` | `agent_designer` | Milvus/Zilliz Cloud API key |
| `SUPABASE_DB_URL` | `AgentSpecTools` | Supabase PostgreSQL connection |
| `AGENT_SPEC_USER_ID` | `AgentSpecTools` | Owner UUID for saved specs |
| `AGENT_SPEC_DESIGN_SYSTEM_ID` | `AgentSpecTools` | Default design system UUID |

---

## Python Dependencies (`requirements.txt`)

| Package | Purpose |
|---------|---------|
| `agno[all]` | Core framework |
| `fastapi` + `uvicorn` | Web server |
| `sqlalchemy` | ORM / DB abstraction |
| `psycopg[binary]` | PostgreSQL driver |
| `pgvector` | pgvector extension support |
| `lancedb` | Local vector store |
| `openai` | OpenAI embedder + models |
| `ollama` | Ollama model client |
| `mcp` | MCP protocol |
| `toolbox-core` | Google MCP Toolbox client |
| `ddgs` | DuckDuckGo search |
| `python-dotenv` | `.env` loading |
| `pymilvus` | Milvus / Zilliz Cloud client |
