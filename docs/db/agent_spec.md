# Schema: `agent_spec`

> **Purpose:** Captures a completed agent design template as a single, structured database record. Every column maps directly to an Agno API parameter or a code-generation decision. A code generator reads one row and produces a complete, runnable Python agent file + setup instructions.

---

## Design Principles

1. **One row = one agent.** All features for a single agent design live in one record. No joins needed for code generation.
2. **Every column drives a decision.** If a column doesn't affect the generated Python file, setup instructions, or required assets, it doesn't belong here.
3. **JSON columns for variable-length lists.** Tools, knowledge sources, guardrails, and sub-agents vary per agent — stored as JSON arrays/objects, not separate tables.
4. **Template Q# → Column traceability.** Every column is annotated with which template question(s) it derives from, so the pipeline is auditable.
5. **Code-gen ready.** Column names and value vocabularies align with Agno API names where possible (e.g., `architecture_type` values = `agent` / `team` / `workflow`).

---

## Table Definition

| Column | Type | Nullable | Default | Template Source | Description |
|--------|------|----------|---------|-----------------|-------------|
| `id` | UUID PK | No | `gen_random_uuid()` | — | Unique identifier |
| `design_system_id` | UUID FK → design_system | No | — | — | Links to the parent design system |
| `agent_name` | TEXT | No | — | Q1.1 (derived) | Human-readable agent name (slug-safe) |
| `purpose` | TEXT | No | — | Q1.1 | 1–3 sentence description of what the agent does |
| `target_users` | TEXT | No | — | Q1.2 | Who uses this agent (free text) |
| `user_type` | TEXT | No | — | Q1.2 | Normalized: `non_technical` / `semi_technical` / `developer` / `agent` / `internal` |
| `cognitive_mode` | TEXT | No | — | Q1.3 | `extractor` / `measurer` / `assessor` / `generator` / `aggregator` |
| `architecture_type` | TEXT | No | `'agent'` | Q2.1 | `agent` / `team` / `workflow` |
| `sub_roles` | JSONB | Yes | `NULL` | Q2.2 | Array of `{role, responsibility}` objects (only for team/workflow) |
| `knowledge_sources` | JSONB | Yes | `NULL` | Q3.1 | Array of `{type, details}` — type ∈ {`pdf`, `website`, `csv`, `json`, `markdown`, `youtube`, `arxiv`, `pubmed`, `web_search`, `code_repo`, `database`, `custom`} |
| `memory_type` | TEXT | No | `'none'` | Q3.2 | `none` / `user_memory` / `org_memory` / `both` |
| `enable_agentic_memory` | BOOLEAN | No | `FALSE` | Q3.2 | Whether the agent gets memory management tools |
| `update_memory_on_run` | BOOLEAN | No | `FALSE` | Q3.2 | Whether memory auto-updates after each run |
| `storage_type` | TEXT | No | `'sqlite'` | Q3.3 | `sqlite` / `postgres` / `mongodb` / `redis` / `in_memory` |
| `storage_db_url` | TEXT | Yes | `NULL` | Q3.3 | Connection string if not local default |
| `vector_db_type` | TEXT | Yes | `NULL` | Q3.1 | `lancedb` / `pgvector` / `chroma` / `pinecone` / `qdrant` / `milvus` / `weaviate` / `redis` / `none` (only needed if knowledge_sources is non-null) |
| `tools` | JSONB | Yes | `NULL` | Q4.1 | Array of `{toolkit_name, config}` objects — toolkit_name matches Agno import names (e.g., `DuckDuckGoTools`, `PostgresTools`) |
| `custom_tools` | JSONB | Yes | `NULL` | Q4.1 | Array of `{name, description, code_stub}` for any non-toolkit tools |
| `hitl_enabled` | BOOLEAN | No | `FALSE` | Q4.2 | Whether human-in-the-loop confirmation is needed |
| `hitl_actions` | JSONB | Yes | `NULL` | Q4.2 | Array of action names requiring human approval (if hitl_enabled) |
| `reasoning_level` | TEXT | No | `'none'` | Q5.1 | `none` / `moderate` / `deep` |
| `output_format` | TEXT | No | `'markdown'` | Q5.2 | `text` / `markdown` / `structured` / `mixed` |
| `output_schema` | JSONB | Yes | `NULL` | Q5.2 | Pydantic model definition as JSON schema (if output_format = `structured`) |
| `guardrails` | JSONB | Yes | `NULL` | Q5.3 | Array of `{type, config}` — type ∈ {`pii_detection`, `prompt_injection`, `content_moderation`, `input_validation`, `output_validation`, `custom`} |
| `session_state_schema` | JSONB | Yes | `NULL` | Q5.4 | Description of state that persists across conversation turns |
| `enable_agentic_state` | BOOLEAN | No | `FALSE` | Q5.4 | Whether the agent gets tools to update session_state |
| `deployment_interfaces` | JSONB | No | `'["web_chat"]'` | Q6.1 | Array of: `web_chat` / `slack` / `discord` / `telegram` / `whatsapp` / `rest_api` / `mcp_server` / `cli` |
| `model_provider` | TEXT | No | `'ollama'` | Q6.2 | `ollama` / `openai` / `anthropic` / `google` / `other` |
| `model_id` | TEXT | No | `'glm-5.1:cloud'` | Q6.2 | Model identifier string (e.g., `glm-5.1:cloud`, `gpt-4o`, `claude-sonnet-4-20250514`) |
| `multimodal_inputs` | JSONB | Yes | `NULL` | Q6.3 | Array of: `image` / `audio` / `video` / `file` (NULL = text only) |
| `schedule_enabled` | BOOLEAN | No | `FALSE` | Q6.4 | Whether the agent runs on a schedule |
| `schedule_cron` | TEXT | Yes | `NULL` | Q6.4 | Cron expression if schedule_enabled |
| `observability_level` | TEXT | No | `'basic'` | Q6.5 | `none` / `basic` / `advanced` |
| `observability_provider` | TEXT | Yes | `NULL` | Q6.5 | `langfuse` / `langsmith` / `arize` / `langwatch` / `none` |
| `skills_domains` | JSONB | Yes | `NULL` | Q7.1 | Array of domain names for specialized knowledge |
| `system_prompt` | TEXT | Yes | `NULL` | Q7.2 | Full system prompt / persona instructions |
| `instructions` | JSONB | Yes | `NULL` | Q7.2 | Array of instruction strings (Agno `instructions` param) |
| `description` | TEXT | Yes | `NULL` | Q7.2 | Short description added to system message start |
| `expected_output` | TEXT | Yes | `NULL` | Q5.2 / Q7.2 | Description of expected output format/quality |
| `cost_preference` | TEXT | No | `'balanced'` | Q8.1 | `minimize` / `balanced` / `performance_first` |
| `latency_requirement` | TEXT | No | `'conversational'` | Q8.2 | `realtime` / `conversational` / `batch` |
| `runtime_environment` | TEXT | No | `'local'` | Q8.3 | `local` / `docker` / `cloud` / `agent_os` |
| `required_env_vars` | JSONB | Yes | `NULL` | Auto-derived | Array of `{var_name, description, required_by}` — auto-populated from tool/model choices |
| `pip_dependencies` | JSONB | Yes | `NULL` | Auto-derived | Array of pip package strings — auto-populated from tool/model/storage choices |
| `additional_setup_notes` | TEXT | Yes | `NULL` | Auto-derived | Free-text notes for the user about external tasks (get API key, start Ollama, create DB, etc.) |
| `status` | TEXT | No | `'draft'` | — | `draft` / `spec_complete` / `code_generated` / `tested` / `deployed` |
| `created_at` | TIMESTAMPTZ | No | `now()` | — | Record creation time |
| `updated_at` | TIMESTAMPTZ | No | `now()` | — | Last update time |
| `created_by` | UUID FK → users | No | — | — | Who created this spec |

---

## JSONB Column Schemas

### `sub_roles` (Q2.2)
```json
[
  {"role": "Researcher", "responsibility": "Searches web for relevant sources"},
  {"role": "Writer", "responsibility": "Produces the final report"}
]
```

### `knowledge_sources` (Q3.1)
```json
[
  {"type": "pdf", "details": "company_handbook.pdf"},
  {"type": "website", "details": "https://docs.example.com"},
  {"type": "csv", "details": "support_tickets.csv"},
  {"type": "web_search", "details": "DuckDuckGo"}
]
```

### `tools` (Q4.1)
```json
[
  {"toolkit_name": "DuckDuckGoTools", "config": {}},
  {"toolkit_name": "CalculatorTools", "config": {}},
  {"toolkit_name": "PostgresTools", "config": {"db_url": "postgresql+psycopg://..."}}
]
```

### `custom_tools` (Q4.1)
```json
[
  {
    "name": "lookup_trust_token_balance",
    "description": "Returns the trust token balance for a given member address",
    "code_stub": "def lookup_trust_token_balance(member_address: str) -> int:\n    ..."
  }
]
```

### `hitl_actions` (Q4.2)
```json
["send_email", "database_write", "spend_money"]
```

### `output_schema` (Q5.2)
```json
{
  "title": "ResearchReport",
  "type": "object",
  "properties": {
    "summary": {"type": "string"},
    "sources": {"type": "array", "items": {"type": "string"}},
    "confidence": {"type": "number", "minimum": 0, "maximum": 1}
  },
  "required": ["summary", "sources", "confidence"]
}
```

### `guardrails` (Q5.3)
```json
[
  {"type": "pii_detection", "config": {}},
  {"type": "prompt_injection", "config": {}},
  {"type": "custom", "config": {"name": "NoFinancialAdvice", "description": "Blocks any output that could be construed as financial advice"}}
]
```

### `session_state_schema` (Q5.4)
```json
{
  "current_issue_category": "string",
  "resolution_status": "open | in_progress | resolved",
  "items_discussed": "array of strings"
}
```

### `deployment_interfaces` (Q6.1)
```json
["web_chat", "slack"]
```

### `multimodal_inputs` (Q6.3)
```json
["image", "file"]
```

### `skills_domains` (Q7.1)
```json
["customer_support_best_practices", "product_troubleshooting"]
```

### `instructions` (Q7.2)
```json
[
  "Always cite your sources",
  "If you are unsure, say so rather than guessing",
  "Format responses in clear sections"
]
```

### `required_env_vars` (auto-derived)
```json
[
  {"var_name": "OPENAI_API_KEY", "description": "Required for OpenAI model", "required_by": "model_provider=openai"},
  {"var_name": "TAVILY_API_KEY", "description": "Required for Tavily web search", "required_by": "TavilyTools"}
]
```

### `pip_dependencies` (auto-derived)
```json
["agno[openai]", "agno[tavily]", "duckdb", "lancedb"]
```

---

## Auto-Derivation Logic

Some columns are **not filled by the user** — they're computed from other answers. The code generator (or a spec-processor agent) populates these:

| Column | Derivation Logic |
|--------|-----------------|
| `required_env_vars` | Model provider → API key env var; Tools → API key env vars (e.g., `TavilyTools` → `TAVILY_API_KEY`, `ExaTools` → `EXA_API_KEY`) |
| `pip_dependencies` | Model provider → `agno[provider]`; Tools → their pip extras; Storage → `agno[postgres]` etc.; Vector DB → its package |
| `additional_setup_notes` | "Start Ollama first" if model_provider=ollama; "Create Postgres database" if storage_type=postgres; "Set up vector DB" if vector_db_type needs infra |
| `vector_db_type` | If knowledge_sources includes non-search types, defaults to `lancedb` for local / `pgvector` if storage_type=postgres |
| `enable_agentic_memory` | Set TRUE if memory_type ∈ {`user_memory`, `both`} and reasoning_level ≥ moderate |
| `storage_db_url` | Defaults: SQLite → local file path; Postgres → needs user to provide |

---

## Status Lifecycle

```
draft → spec_complete → code_generated → tested → deployed
```

| Status | Meaning |
|--------|---------|
| `draft` | Template answers still being collected |
| `spec_complete` | All required columns filled; ready for code generation |
| `code_generated` | Python file + assets generated; not yet tested |
| `tested` | Generated agent has been run and validated |
| `deployed` | Agent is running in production |

---

## Code Generation Flow

```
┌─────────────┐     ┌─────────────┐     ┌──────────────────┐     ┌──────────────┐
│  Template    │────▶│  agent_spec │────▶│  Code Generator  │────▶│  Outputs     │
│  Answers    │     │  (DB row)   │     │  (Agent or AI)   │     │              │
└─────────────┘     └─────────────┘     └──────────────────┘     ├──────────────┤
                                                                   │ agent.py     │
                                                                   │ .env.example │
                                                                   │ requirements │ │
                                                                   │ setup.md     │
                                                                   └──────────────┘
```

1. **User fills template** → answers stored in `agent_spec` row
2. **Auto-derivation** fills `required_env_vars`, `pip_dependencies`, `additional_setup_notes`
3. **Code generator** reads the row and produces:
   - `agent.py` — complete, runnable Agno agent
   - `.env.example` — env vars the user must set
   - `requirements.txt` — pip dependencies
   - `setup.md` — step-by-step instructions for external tasks

---

## Validation Rules (CHECK constraints)

| Constraint | Expression |
|------------|------------|
| Valid cognitive mode | `cognitive_mode IN ('extractor','measurer','assessor','generator','aggregator')` |
| Valid architecture | `architecture_type IN ('agent','team','workflow')` |
| Valid memory type | `memory_type IN ('none','user_memory','org_memory','both')` |
| Valid reasoning level | `reasoning_level IN ('none','moderate','deep')` |
| Valid output format | `output_format IN ('text','markdown','structured','mixed')` |
| Valid cost preference | `cost_preference IN ('minimize','balanced','performance_first')` |
| Valid latency | `latency_requirement IN ('realtime','conversational','batch')` |
| Valid runtime | `runtime_environment IN ('local','docker','cloud','agent_os')` |
| Valid status | `status IN ('draft','spec_complete','code_generated','tested','deployed')` |
| Sub-roles required for team/workflow | `(architecture_type = 'agent') OR (sub_roles IS NOT NULL)` |
| Knowledge requires vector DB | `(knowledge_sources IS NULL) OR (vector_db_type IS NOT NULL)` |
| Schedule needs cron | `(NOT schedule_enabled) OR (schedule_cron IS NOT NULL)` |
| Advanced observability needs provider | `(observability_level != 'advanced') OR (observability_provider IS NOT NULL)` |
| Structured output needs schema | `(output_format != 'structured') OR (output_schema IS NOT NULL)` |
| HITL enabled needs actions | `(NOT hitl_enabled) OR (hitl_actions IS NOT NULL)` |

---

## Indexes

| Index | Columns | Purpose |
|-------|---------|---------|
| `ix_agent_spec_design_system` | `design_system_id` | Look up all specs for a design system |
| `ix_agent_spec_status` | `status` | Filter by lifecycle stage |
| `ix_agent_spec_cognitive_mode` | `cognitive_mode` | Filter by agent type |
| `ix_agent_spec_architecture` | `architecture_type` | Filter by architecture |
| `ix_agent_spec_created_by` | `created_by` | Look up specs by creator |

---

## Relationship to Existing Platform Schemas

| Existing Table | Relationship |
|---------------|--------------|
| `design_system` | **Parent** — each `agent_spec` belongs to one `design_system` |
| `response` | **Source** — template answers are initially captured as `response` rows; the `agent_spec` row is a **computed view** of those responses, restructured for code generation |
| `generated_document` | **Consumer** — once code is generated, it can be stored as a `generated_document` row |
| `users` | **Owner** — `created_by` references `users.id` |