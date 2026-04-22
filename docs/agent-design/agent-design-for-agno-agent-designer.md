# Agent design: Agno Agent Designer

## Part 1: Purpose & People

| Question | Your Answer |
|---|---|
| **1.1** What is the agent supposed to do? | Takes a user's completed template (or walks them through it interactively) and produces a complete, runnable Agno agent — including the Python file, required dependencies, environment variable setup instructions, and any external tasks the user needs to complete (e.g., getting API keys). It maps every user answer to the correct Agno class, import path, constructor, and configuration. A successful outcome is: user gets a `python agent.py` that runs on the first try, with zero guesswork about Agno's API. |
| **1.2** Who will use this agent? | Semi-technical users — people who can run Python and edit a `.env` file, but who don't want to read Agno docs to figure out which class, toolkit, or knowledge backend to use. May also be used by developers/engineers who want to scaffold an agent quickly without hand-coding every import. |
| **1.3** What kind of cognitive work does the agent primarily do? | **Generator** — Produces content/drafts that must be verified. The agent generates Python code and architecture decisions. The human must review the output before running it (especially for production use). Secondary: **Assessor** — evaluates user requirements against Agno capabilities to determine the right architecture. |

> **Design note on 1.3:** Because this is primarily a Generator, the agent should always include a human review step. It should never auto-execute the code it generates. It should also validate its own output against the Agno docs knowledge base before presenting it, reducing (but not eliminating) the need for human verification.

---

## Part 2: Architecture

| Question | Your Answer |
|---|---|
| **2.1** How complex is the task? | **Moderate — Multiple steps, predictable flow → Workflow.** The design process has a clear pipeline: (1) intake user requirements → (2) map requirements to Agno capabilities → (3) validate mappings against Agno docs → (4) generate code → (5) generate setup instructions. Each step is sequential with conditional branching (e.g., if the user wants a Team, branch to Team-specific generation). |
| **2.2** Sub-roles/steps: | **Step 1 — Intake Agent**: Receives the user's template answers (or asks follow-up questions if answers are incomplete). Normalizes inputs into a structured `AgentSpec` Pydantic model. **Step 2 — Mapper Agent**: Reads the `AgentSpec` and maps each field to specific Agno classes, imports, tools, knowledge backends, and storage. Consults the Agno docs knowledge base to verify every import path and constructor signature. **Step 3 — Code Generator Agent**: Takes the validated mapping and produces a complete Python file with all imports, the agent/team/workflow definition, and inline comments. **Step 4 — Setup Instructions Agent**: Produces the `pip install` commands, `.env` template, and any "you need to do X before running" instructions. **Conditional**: If the user requests HITL, guardrails, or scheduled runs, additional branches add those configurations. |

> **Design note on 2.1:** While a Team *could* work (dynamic delegation to specialists), a Workflow is better here because the process is fundamentally a pipeline — each step produces a structured artifact that the next step consumes. The predictability of the flow makes a Workflow more reliable and easier to debug than a Team. However, if we later want the agent to *iteratively* refine the design with the user (going back and forth), a Team with coordinate mode would be better. For v1, Workflow.

---

## Part 3: Data & Knowledge

| Question | Your Answer |
|---|---|
| **3.1** What information does the agent need to know about? | **Agno documentation** — all class references, constructor parameters, import paths, tool lists, knowledge base types, vector store options, memory configurations, guardrail options, storage backends, and deployment patterns. This is the *primary* knowledge source. **Code templates** — example agent definitions for common patterns (single agent, team, workflow) that serve as scaffolding. **Real-time web search** — as a fallback when the local knowledge base is insufficient or when the user asks about a very new Agno feature not yet in the indexed docs. |
| **3.2** Should the agent be able to learn and remember over time? | **Both — Per-user and per-organization memory.** **User memory**: Remember that this user prefers YAML output, or always uses PostgreSQL, or likes detailed comments. This saves re-asking on return visits. **Agent/Organizational memory**: Accumulate patterns — e.g., "most users who ask for a Team actually need a Workflow" or "the Ollama `glm-5.1:cloud` model is the default recommendation." This improves mapping quality over time. |
| **3.3** Where should stored data live? | **PostgreSQL** with PgVector. This serves dual purpose: (1) session storage for conversation history, and (2) vector storage for the Agno docs knowledge base. One database, two uses. PgVector supports the metadata filtering and vector search needed for doc retrieval. For local/development use, **SQLite** with LanceDB for vectors is the lightweight fallback. |

> **Design note on 3.1:** The Agno docs knowledge base is the single most important piece. Every import path, constructor parameter, and default value must be verified against it. The agent should never guess — it should always look it up. This is why we need `KnowledgeTools` (search/retrieve from knowledge base) as a tool for the Mapper Agent step.

---

## Part 4: Tools & Actions

### 4.1 What external actions should the agent be able to take?

| Category | Available Actions | Your Selections |
|---|---|---|
| 📚 Information & Research | Web search · Website scraping · ArXiv/PubMed · HackerNews · Wikipedia | ✅ **Web search** (DuckDuckGo — for looking up new Agno features or checking latest docs online when local KB is insufficient) · ✅ **Website scraping** (to fetch specific Agno doc pages for verification) |
| 💬 Communication | Email · Slack · Discord · Telegram · WhatsApp · SMS | ❌ Not needed |
| 📊 Data & Databases | SQL queries · Spreadsheets · Pandas | ❌ Not needed for v1 |
| 🛠️ Productivity & PM | GitHub/GitLab · Jira/Linear · Notion · ClickUp · Google Calendar | ❌ Not needed for v1 |
| 💰 Finance | Stock data · OpenBB | ❌ Not needed |
| 🎨 Media Generation | Image · Audio · Video | ❌ Not needed |
| 🔧 System & Code | Shell commands · Python execution · File system · Docker | ✅ **Python execution** (to validate generated code runs without syntax errors) · ✅ **File system** (to write the generated agent file to disk) |
| 🌐 Web & APIs | Custom API calls · MCP servers · Web browsing · Google Maps | ✅ **MCP servers** (if we want to connect to an external Agno docs MCP server in the future) |
| 📦 Other | Calculator · Weather | ❌ Not needed |

| Question | Your Answer |
|---|---|
| **4.2** Human approval before certain actions? | **Yes — only for risky actions.** Specifically: before writing any file to disk (the generated agent Python file) and before executing any generated Python code (validation step). The user should confirm the file path and review the code before it's saved or run. |

> **Design note:** The core tools are: (1) **DuckDuckGo** for web search fallback, (2) **WebsiteTools** for fetching specific doc pages, (3) **KnowledgeTools** for searching the local Agno docs knowledge base, (4) **PythonTools** for code validation, (5) **FileTools** for writing output. Everything else is noise for this use case.

---

## Part 5: Intelligence & Behavior

| Question | Your Answer |
|---|---|
| **5.1** How much "thinking" does the agent need to do? | **Deep analysis** — Reason carefully through complex, multi-step problems. The Mapper step especially needs deep reasoning: it must cross-reference user requirements with Agno capabilities, check import paths, verify constructor signatures, and determine the right architecture pattern. A wrong import path or missing parameter means the generated code won't run. **Reasoning Tools** (`think()` and `analyze()`) for the Mapper and Code Generator steps are essential. |
| **5.2** What should the output look like? | **Mixed (depends on the step).** The `AgentSpec` output from Step 1 is **structured data (Pydantic/JSON)**. The code output from Step 3 is a **Python code block** with inline **Markdown** comments. The setup instructions from Step 4 are **Markdown**. The final deliverable is a **Markdown document** containing the code, setup instructions, and a checklist of external tasks. |
| **5.3** Guardrails or safety rules? | ✅ **Prompt injection defense** — critical since the agent processes user-provided template text that could be adversarial. ✅ **Output validation** — the generated code must be validated (syntax check, import path check against knowledge base). ✅ **Custom rule: Never auto-execute generated agent code.** Always present it for human review first. |
| **5.4** Maintain state across a conversation? | **Yes** — the `AgentSpec` (the structured user requirements) is built up incrementally. If the user provides answers in multiple turns, the spec accumulates. Also: the mapping results, code drafts, and setup instructions are all state that persists within the session as the workflow progresses step by step. |

---

## Part 6: Deployment & Integration

| Question | Your Answer |
|---|---|
| **6.1** How will users interact? | ✅ **Web chat** (AgentOS playground — primary) · ✅ **CLI** (for developers who want to pipe template answers in and get code out) · ✅ **MCP Server** (so other agents can call the Agent Designer as a tool — e.g., "design me an agent that does X") |
| **6.2** What model should the agent use? | **Default — Ollama `glm-5.1:cloud`** for all steps. If reasoning quality is insufficient for the Mapper step, consider upgrading that specific step to a reasoning-capable model. But start with the default and measure. |
| **6.3** Multi-modal input/output? | **Text only** for v1. The template is text, the output is code + markdown. No images, audio, or video needed. |
| **6.4** Run on a schedule? | **No — on-demand only.** Users request agent designs when they need them. No periodic generation needed. |
| **6.5** Observability / monitoring? | **Advanced — full tracing.** This agent generates code that other people will run. If it produces a bad import path or wrong constructor, that's a trust-breaking failure. We need Langfuse or equivalent to trace every step, catch regressions, and debug mapping failures. Also: tracing helps us improve the knowledge base by showing which doc lookups failed. |

---

## Part 7: Skills & Specialization

| Question | Your Answer |
|---|---|
| **7.1** Specialized domain expertise? | **Yes — the Agno framework.** This agent needs deep, precise knowledge of: all Agno agent types (Agent, Team, Workflow), all 120+ toolkits and their import paths, all knowledge readers and vector stores, memory and learning configurations, guardrail types and their parameters, storage backends, HITL mechanisms, session state, output schemas, and deployment patterns. This is a *single domain* but it's a wide one. The Agno docs knowledge base is the primary skill. |
| **7.2** Role-play instructions? | "You are an Agno Agent Design Architect — an expert at translating user requirements into complete, runnable Agno agent code. You **never guess** at import paths, class names, or constructor parameters. You **always verify** against the Agno documentation knowledge base before including any class or parameter in your output. If you cannot find a class or parameter in the docs, you flag it explicitly and suggest the user verify manually. You produce code that runs on the first try. You explain every design decision. You are methodical, thorough, and honest about what you know vs. what you're inferring." |

---

## Part 8: Budget & Constraints

| Question | Your Answer |
|---|---|
| **8.1** Cost constraints? | **Minimize cost.** This agent uses Ollama models (local/free). The only external cost is vector storage if we use a cloud-hosted PgVector, and observability if we use a cloud Langfuse. Keep it local-first. |
| **8.2** Latency requirements? | **Conversational (a few seconds).** The user is waiting for a design, not a real-time response. Deep reasoning is acceptable if it produces better output. The knowledge base lookup adds a bit of latency, but it's necessary for accuracy. |
| **8.3** Environment? | **Local machine** for development. **AgentOS** for deployment (since we want web chat + MCP server interfaces). Docker container for production isolation. |

---

## Architecture Summary

Based on the above, here's the proposed architecture:

```
┌─────────────────────────────────────────────────────┐
│              Agno Agent Designer Workflow            │
│                                                      │
│  ┌──────────┐    ┌──────────┐    ┌────────────────┐  │
│  │ Step 1:  │───▶│ Step 2:  │───▶│   Step 3:     │  │
│  │ Intake   │    │ Mapper   │    │ Code Generator │  │
│  │ Agent    │    │ Agent    │    │    Agent       │  │
│  └──────────┘    └──────────┘    └────────────────┘  │
│       │               │                  │           │
│   AgentSpec       ValidatedMap      Python code      │
│   (Pydantic)      + notes           + comments      │
│                                          │           │
│                               ┌────────────────┐    │
│                               │   Step 4:      │    │
│                               │   Setup        │───▶│ Final output:
│                               │   Instructions  │    │ .py file
│                               └────────────────┘    │ + setup.md
│                                                      │ + checklist
└─────────────────────────────────────────────────────┘
```

**Key Agno features used:**

| Feature | Agno Class/Config | Purpose |
|---|---|---|
| Orchestration | `Workflow` with `Step` | Predictable pipeline |
| Knowledge | `AgentKnowledge` + `MarkdownReader` + `PDFReader` + `PgVector` | Agno docs indexed for retrieval |
| Knowledge Tools | `KnowledgeTools` | Mapper step searches docs to verify APIs |
| Memory | `update_memory_on_run=True` + `enable_agentic_memory=True` | Remember user preferences + accumulate patterns |
| Reasoning | `ReasoningTools` (think + analyze) | Deep reasoning for Mapper + Code Generator |
| Tools | `DuckDuckGoTools`, `WebsiteTools`, `PythonTools`, `FileTools` | Search, verify, validate, write |
| Output | `output_schema=AgentSpec` (Step 1) · `markdown=True` (Steps 3-4) | Structured then formatted |
| Guardrails | `PromptInjectionGuardrail` | Protect against adversarial templates |
| Storage | `PostgresStorage` (session) + `PgVector` (knowledge) | Dual-purpose PostgreSQL |
| HITL | `UserConfirmation` on `FileTools.write` and `PythonTools.run` | Human approves before write/execute |

---
