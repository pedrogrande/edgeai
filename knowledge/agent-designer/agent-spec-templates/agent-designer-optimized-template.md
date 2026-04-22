---
agent_name: Agent Designer (Optimized)
cognitive_mode: generator
architecture: single
status: approved
created_date: 2026-05-25
---

# Agno Agent Design Template — Agent Designer (Optimized)

## Part 1: Purpose & People

| Question | Your Answer |
|---|---|
| **1.1** What is the agent supposed to do? | Design well-structured Agno agents from user requirements. Guide users through a 7-phase process (Discover → Scope → Specify → Review & Approve → Generate → Validate → Persist) to produce complete, runnable Agno agent Python code. |
| **1.2** Who will use this agent? | Semi-technical users and developers/engineers — people who may not know Agno's API but can understand code once generated. |
| **1.3** What kind of cognitive work does the agent primarily do? | **Generator** — Produces agent specs and code. Must be verified by human before deployment. |

## Part 2: Architecture

| Question | Your Answer |
|---|---|
| **2.1** How complex is the task? | **Moderate** — Multiple steps with predictable flow, but currently implemented as **Single Agent** (Workflow is a future evolution step). |
| **2.2** Sub-roles or steps? | 7 phases: Discover → Scope → Specify → Review & Approve → Generate → Validate → Persist. Phase 4 is a mandatory human gate. |

## Part 3: Data & Knowledge

| Question | Your Answer |
|---|---|
| **3.1** What information does the agent need? | Agno documentation (via Milvus/Zilliz Cloud knowledge base), current architecture doc, agent design template reference. |
| **3.2** Should the agent remember over time? | **Both** — Session state for structured approval tracking within a session; `update_memory_on_run` for cross-session awareness of previously approved specs. |
| **3.3** Where should stored data live? | SQLite (session state + session history) for the agent itself; Milvus/Zilliz Cloud for knowledge base; Supabase for persisted agent specs. |

## Part 4: Tools & Actions

| Category | Selections |
|---|---|
| 📚 Information & Research | DuckDuckGo (fallback), Knowledge base search (primary) |
| 🛠️ System & Code | FileTools (read/write templates), LocalFileSystemTools (browse agents/), ReasoningTools (structured thinking) |
| 📦 Custom | AgentSpecTools (create design systems, persist specs, derive metadata, set status) |

| Question | Your Answer |
|---|---|
| **4.2** Human approval before actions? | **Yes, for risky actions** — Approval required before writing agent files or persisting specs. Smart approval tracking via session state prevents redundant re-approval. |

## Part 5: Intelligence & Behavior

| Question | Your Answer |
|---|---|
| **5.1** How much "thinking"? | **Deep analysis** — ReasoningTools for structured step-by-step thinking during design phases. |
| **5.2** Output format? | **Markdown** — Clean, readable templates and code with explanations. |
| **5.3** Guardrails? | Input validation (verify API details against docs), output validation (check import paths, constructor params), custom rule: never write code without explicit approval. |
| **5.4** State across conversation? | **Yes** — Session state tracks: design_phase, current_spec_name, spec_approved (dict), spec_changes_since_approval (dict), code_generated (dict). |

## Part 6: Deployment & Integration

| Question | Your Answer |
|---|---|
| **6.1** How will users interact? | Web chat (via AgentOS/EdgeAI), CLI (standalone). |
| **6.2** What model? | **Default** — Ollama `glm-5.1:cloud`. |
| **6.3** Multi-modal? | **Text only** for now. |
| **6.4** Scheduled runs? | **No** — On-demand only. |
| **6.5** Observability? | **Basic** — Console logs. Advanced (Langfuse) is a future option. |

## Part 7: Skills & Specialization

| Question | Your Answer |
|---|---|
| **7.1** Specialized domain expertise? | **Yes** — Agno framework API, agent design patterns, Python code generation. |
| **7.2** Role-play instructions? | "You are an Agno Agent Design Agent — an expert at designing well-structured Agno agents. Always verify API from docs. Always use Ollama models except for embedding. Explain technical choices in plain language." |

## Part 8: Budget & Constraints

| Question | Your Answer |
|---|---|
| **8.1** Cost constraints? | **Minimize cost** — Ollama model, no cloud model usage. |
| **8.2** Latency requirements? | **Conversational** (a few seconds acceptable — reasoning tools add latency for quality). |
| **8.3** Environment? | **AgentOS** (EdgeAI app), local machine for development. |

---

## Optimization Decisions (Approved)

1. **Replace PythonTools with ReasoningTools** — Better suited for design-thinking tasks; `think()` and `analyze()` for structured reasoning instead of arbitrary Python execution.
2. **Add session state for smart approval tracking** — Prevents redundant re-approval of the same spec. Tracks `spec_approved`, `spec_changes_since_approval` per spec. Only re-requests approval if something actually changed.
3. **Keep `update_memory_on_run=True`** — Cross-session awareness so the agent remembers what was approved in previous conversations.
4. **Approval gates retained** — Mandatory human gate at Phase 4, but now state-aware and non-redundant.
5. **Context compression** (`compress_tool_results=True`) — Automatically compresses verbose tool results (KB search results, DuckDuckGo results, spec tool outputs) after 3 uncompressed results. Keeps context lean and avoids hitting context window limits during long design sessions.
6. **Tool call limit** (`tool_call_limit=15`) — Prevents runaway tool loops where the agent keeps calling tools without converging. 15 is generous for multi-phase design work but prevents infinite loops and unbounded cost.
7. **Controlled history** (`add_history_to_context=True`, `num_history_runs=3`, `max_tool_calls_from_history=3`) — Replaces `read_chat_history=True` (which loads full history unpredictably) with bounded, predictable context: last 3 conversation turns + max 3 tool call results from history. This is the context engineering principle of "minimum information needed and nothing else."