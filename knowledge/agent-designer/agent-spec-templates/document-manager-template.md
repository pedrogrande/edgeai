---
agent_name: Document Manager
cognitive_mode: extractor
architecture: single
status: approved
created_date: 2026-04-21
---

# Agno Agent Design Template — Document Manager

## Part 1: Purpose & People

| Question | Answer |
|---|---|
| **1.1** What is the agent supposed to do? | Automated document pipeline agent that picks up artifact files from staging directories (`artifacts/<domain>/`), validates and applies YAML front matter, indexes content into domain-specific PgVector knowledge bases, registers documents in a PostgreSQL `documents` table via MCP Toolbox, and archives processed files. Also serves as a conversational query endpoint — humans and other agents can ask "What strategy artifacts exist for AI Assisted Learning?" or "Show me all documents with errors." |
| **1.2** Who will use this agent? | Internal team members + other agents (domain agents like AI Assisted Learning Designer). Dual audience: automated (domain agents trigger processing) and conversational (humans query artifact metadata). |
| **1.3** Cognitive mode | **Extractor** — Gathers and processes files without judging their content. Validates structure, indexes content, registers metadata. Never interprets or evaluates the *meaning* of artifacts. |

## Part 2: Architecture

| Question | Answer |
|---|---|
| **2.1** How complex is the task? | **Simple** — One focused task (pick up → process → register → archive). Single Agent. Future Workflow upgrade path: Scanner → Processor → Indexer → Archiver. |
| **2.2** Sub-roles/steps | N/A — Single Agent. Future Workflow steps: Scanner (find files) → Processor (validate front matter) → Indexer (embed into PgVector) → Archiver (move to archive + update DB status). |

## Part 3: Data & Knowledge

| Question | Answer |
|---|---|
| **3.1** What information does the agent need? | Database data (`documents` table via MCP Toolbox), file system (staging + archive directories), PgVector (domain-specific knowledge base tables). |
| **3.2** Memory | Agent memory only — remembers processing state and history. No per-user preferences (infrastructure agent, not personal). |
| **3.3** Storage | PostgreSQL (via MCP Toolbox for document registry) + PgVector (for knowledge indexing) + SQLite (for agent session/memory). PostgreSQL is the registry of record. |

## Part 4: Tools & Actions

### 4.1 External Actions

| Category | Selections |
|---|---|
| 📊 Data & Databases | MCP Toolbox — `doc-mgmt` toolset |
| 🔧 System & Code | FileTools, ReasoningTools, LocalFileSystemTools |

| Question | Answer |
|---|---|
| **4.2** Human approval before actions? | **No** — Fully automated pipeline. Archive directory + error logging are the safety nets. |

## Part 5: Intelligence & Behavior

| Question | Answer |
|---|---|
| **5.1** Thinking depth | Moderate reasoning — step-by-step front matter validation via ReasoningTools. |
| **5.2** Output format | Markdown — processing logs, status reports, conversational query responses. |
| **5.3** Guardrails | Input validation (valid markdown check) + output validation (front matter structure). No PII or content moderation concerns. |
| **5.4** State across conversation | Yes — processing queue/state: pending files, processing status, error count, last scan time. |

## Part 6: Deployment & Integration

| Question | Answer |
|---|---|
| **6.1** Interaction mode | REST API (AgentOS) + Scheduled polling (5 min) + Web chat (human queries). |
| **6.2** Model | Default — Ollama `glm-5.1:cloud` (Recommended). Local/free ideal for frequent background processing. |
| **6.3** Multi-modal | Text only — processes markdown files. |
| **6.4** Schedule | Yes — every 5 minutes for file scanning + on-demand triggers from domain agents. |
| **6.5** Observability | Basic — console logs + database status tracking. |

## Part 7: Skills & Specialization

| Question | Answer |
|---|---|
| **7.1** Specialized domain expertise | Yes — document management and artifact processing. Knows artifact type taxonomy, front matter schema, domain directory structure. |
| **7.2** Role-play instructions | Systematic, reliable processor. Like a postal sorting facility: files come in, get validated, stamped, indexed, and filed. Doesn't judge content, just ensures correct format and routing. |

## Part 8: Budget & Constraints

| Question | Answer |
|---|---|
| **8.1** Cost | Minimize cost — Ollama = free, no paid API calls. |
| **8.2** Latency | Batch — minutes acceptable (5-minute polling). Conversational queries a few seconds. |
| **8.3** Environment | Docker container (EdgeAI AgentOS). |

## Design Decisions Summary

| Decision | Choice | Why |
|----------|--------|-----|
| Architecture | Single Agent | Processing is simple now; Workflow is the future upgrade path |
| Cognitive mode | Extractor | Gathers/processes without judging content |
| Database registry | Via MCP Toolbox | Structured queries, single source of truth, same infra |
| File lifecycle | Archive, don't delete | Recovery safety net + human readability while web UI doesn't exist |
| Reasoning tool | ReasoningTools (not PythonTools) | Step-by-step front matter validation via model reasoning |
| HITL | None | Fully automated; archive + error logging are safety nets |
| Domain agent changes | None needed now | They still write to staging; Document Manager handles the rest |
| Knowledge | PgVector per domain | Same pattern as AI Learning Designer; Document Manager indexes into domain tables |
| Memory | Agent memory only | Infrastructure agent; no per-user preferences needed |