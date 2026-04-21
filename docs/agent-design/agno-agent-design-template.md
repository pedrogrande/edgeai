# Agno Agent Design Template

> **Purpose:** A structured questionnaire that makes it easy for *any* user — technical or not — to collaborate with an Agno Agent Design Agent. The answers map directly to Agno capabilities, so nothing is missed and no feature is overlooked.

---

## How to Use This Template

1. **Share this template** with the person who wants an agent built.
2. They fill in the **Your Answer** column — short answers are fine; "I don't know" is a valid answer.
3. The Design Agent reads the answers and maps each one to specific Agno features, tools, knowledge bases, memory, storage, etc.
4. The Design Agent proposes a complete architecture and generates runnable code.

> 💡 **Each question includes a "Why we ask" note** that explains which Agno capability it maps to, so you understand the value of your answer.

---

## Part 1: Purpose & People

| Question | Your Answer |
|---|---|
| **1.1** What is the agent supposed to do? *In 1–3 sentences, describe the job this agent performs. What problem does it solve? What does a successful outcome look like?* | |
| **1.2** Who will use this agent? *Choose one or describe: Non-technical end users · Semi-technical users · Developers/engineers · Other agents/automated systems · Internal team members* | |
| **1.3** What kind of cognitive work does the agent primarily do? *Pick one: **Extractor** — Gathers/collects information. Never judges. · **Measurer** — Quantifies/measures against criteria. Never interprets. · **Assessor** — Evaluates against standards. Human makes the final call. · **Generator** — Produces content/drafts. Must be verified. · **Aggregator** — Combines/synthesizes. Must not add beyond inputs.* | |

> **Why we ask:**
> - **1.1** — Drives everything: model choice, tools, knowledge, memory, and whether you need a single Agent, a Team, or a Workflow.
> - **1.2** — User type determines output format (plain language vs. structured data), error tolerance, and whether we need Human-in-the-Loop confirmation steps.
> - **1.3** — Cognitive classification determines appropriate guardrails, system prompt framing, and whether we need reasoning capabilities. For example, an Extractor should never interpret; a Generator should always include a human review step.

---

## Part 2: Architecture

| Question | Your Answer |
|---|---|
| **2.1** How complex is the task? *Pick one: **Simple** — One focused task → Single Agent · **Moderate** — Multiple steps, predictable flow → Workflow · **Complex** — Multiple specialists coordinating dynamically → Team · **Very complex** — Mix of predictable and dynamic → Workflow with Teams inside* | |
| **2.2** If you chose "Team" or "Workflow," what are the sub-roles or steps? *List each role/step and what it's responsible for. E.g., Researcher → searches web; Analyst → evaluates credibility; Writer → produces report.* | |

> **Why we ask:**
> - **2.1** — Agno offers three orchestration patterns: **Agent** (single specialist), **Team** (dynamic collaboration with a leader who delegates), and **Workflow** (predictable pipeline with sequential/parallel/conditional steps). Choosing the wrong pattern leads to either over-engineering or under-capability.
> - **2.2** — Each role becomes a separate Agent in a Team, or a step in a Workflow. This helps us assign the right model, tools, and instructions to each.

---

## Part 3: Data & Knowledge

| Question | Your Answer |
|---|---|
| **3.1** What information does the agent need to know about? *Choose all that apply: Company documents · Product documentation · Website content (specify URLs) · Database data (SQL, CSVs) · Real-time web search · Research papers (arXiv, PubMed) · Code repositories (GitHub, GitLab) · Legal/regulatory texts · Customer support tickets/FAQs · Other (describe)* | |
| **3.2** Should the agent be able to learn and remember over time? *Pick one: **No** — Each conversation starts fresh · **Remember user preferences** — Recall things about individual users across sessions · **Remember organizational knowledge** — Accumulate insights for all users · **Both** — Per-user and per-organization memory* | |
| **3.3** Where should stored data live? *Pick one: Local file (SQLite) · PostgreSQL · MongoDB · Redis · Don't know / Recommend for me* | |

> **Why we ask:**
> - **3.1** — Maps directly to Agno's **Knowledge** system and **Readers**: PDF → `PDFReader`, Websites → `WebsiteReader`, CSV → `CSVReader`, JSON → `JSONReader`, Markdown → `MarkdownReader`, YouTube → `YouTubeReader`. Real-time search maps to **search toolkits** (DuckDuckGo, Tavily, Exa, etc.)
> - **3.2** — Maps to Agno's **Memory** and **Learning** systems: `update_memory_on_run=True` (auto-creates memories per user) · `enable_agentic_memory=True` (agent decides what to remember using tools) · `learning=True` (full learning machine with user profiles, entity memory, decision logs, knowledge transfer)
> - **3.3** — Agno supports multiple database backends for both **session storage** (conversation history) and **vector databases** (knowledge embeddings). The right choice depends on scale, infrastructure, and whether you need vector search.

---

## Part 4: Tools & Actions

### 4.1 What external actions should the agent be able to take?

| Category | Available Actions | Your Selections |
|---|---|---|
| 📚 Information & Research | Web search · Website scraping · ArXiv/PubMed · HackerNews · Wikipedia | |
| 💬 Communication | Email · Slack · Discord · Telegram · WhatsApp · SMS (Twilio) | |
| 📊 Data & Databases | SQL queries · Spreadsheets · Pandas (DataFrames) | |
| 🛠️ Productivity & PM | GitHub/GitLab · Jira/Linear · Notion · ClickUp/Trello/Todoist · Google Calendar · Confluence | |
| 💰 Finance | Stock data (Yahoo Finance) · OpenBB | |
| 🎨 Media Generation | Image generation (DALL-E, Fal, Replicate) · Audio (ElevenLabs, Cartesia) · Video (LumaLabs, Replicate) | |
| 🔧 System & Code | Shell commands · Python execution · File system · Docker · AWS Lambda | |
| 🌐 Web & APIs | Custom API calls · MCP servers · Web browsing (BrowserBase, BrowserUse) · Google Maps | |
| 📦 Other | Calculator · Weather (OpenWeather) · Something else (describe) | |

| Question | Your Answer |
|---|---|
| **4.2** Should the agent need human approval before taking certain actions? *Examples: before sending an email, before making a database change, before spending money. Pick one: Yes · No · Only for risky actions (specify which)* | |

> **Why we ask:**
> - **4.1** — Agno has 120+ pre-built toolkits. Each is a `from agno.tools.X import YTools` import. If we don't have a pre-built toolkit for your need, you can always create a **custom tool** (any Python function can be a tool).
> - **4.2** — Maps to Agno's **Human-in-the-Loop (HITL)** system — `UserConfirmation`, `UserInput`, and `ExternalExecution` requirements that pause the agent until a human approves.

---

## Part 5: Intelligence & Behavior

| Question | Your Answer |
|---|---|
| **5.1** How much "thinking" does the agent need to do? *Pick one: **Quick responses** — Fast, no deep reasoning · **Moderate reasoning** — Think step-by-step before answering · **Deep analysis** — Reason carefully through complex, multi-step problems* | |
| **5.2** What should the output look like? *Pick one: Free-form text · Markdown · Structured data (JSON, Pydantic) · Mixed (depends on the question)* | |
| **5.3** What guardrails or safety rules should the agent follow? *Choose all that apply: PII detection · Prompt injection defense · Content moderation · Input validation · Output validation · Custom rules (describe) · None needed* | |
| **5.4** Should the agent maintain state across a conversation? *Examples: a shopping cart, a to-do list, a draft document being built up over multiple turns. Pick one: Yes (describe the state) · No — each response is independent* | |

> **Why we ask:**
> - **5.1** — Maps to Agno's **Reasoning** capabilities: Quick → Standard model, no reasoning features · Moderate → **Reasoning Tools** (`think()` and `analyze()` for any model) · Deep → **Reasoning Models** (models that natively chain thoughts, like DeepSeek-R1) or **Reasoning + Response Model** combo
> - **5.2** — Maps to Agno's **Output** system: `markdown=True` for formatted output · `output_schema=MyPydanticModel` for structured output · both can be combined
> - **5.3** — Agno has built-in **Guardrails** as pre-hooks/post-hooks: `PIIDetectionGuardrail`, `PromptInjectionGuardrail`, `OpenAIModerationGuardrail`, plus custom guardrails you can write
> - **5.4** — Maps to Agno's **State Management** (`session_state`) — a dictionary that persists across runs within a session. Tools can read and update it.

---

## Part 6: Deployment & Integration

| Question | Your Answer |
|---|---|
| **6.1** How will users interact with this agent? *Choose all that apply: Web chat · Slack bot · Discord bot · Telegram bot · WhatsApp bot · REST API · MCP Server · CLI · Custom (describe)* | |
| **6.2** What model should the agent use? *Pick one: **Default** — Ollama `glm-5.1:cloud` (recommended) · Different Ollama model (specify) · OpenAI (requires API key) · Anthropic Claude (requires API key) · Google Gemini (requires API key) · Other (specify) · Recommend for me* | |
| **6.3** Do you need multi-modal input/output? *Choose all that apply: Images · Audio · Video · Files (PDFs, docs, spreadsheets) · Text only* | |
| **6.4** Do you need the agent to run on a schedule? *Examples: daily report generation, weekly summaries, periodic data checks. Pick one: Yes (describe schedule) · No — on-demand only* | |
| **6.5** Do you need observability / monitoring? *Pick one: Yes — trace runs, monitor costs, debug issues · Basic — just console logs · Advanced — full tracing (Langfuse, LangSmith, Arize, etc.)* | |

> **Why we ask:**
> - **6.1** — Agno's **AgentOS** supports deployment as web apps, Slack bots, Discord bots, MCP servers, and custom FastAPI interfaces. Each has specific setup requirements.
> - **6.2** — Model choice affects cost, speed, reasoning ability, and multimodal support. Agno supports 20+ model providers. For local/private deployments, Ollama is the go-to. For highest quality, cloud models like OpenAI or Anthropic are common.
> - **6.3** — Agno supports **multimodal I/O** — passing images, audio, video, and files as input to agents. This requires a model that supports those modalities.
> - **6.4** — Agno's **Scheduler** supports cron-like scheduling for agents, teams, and workflows.
> - **6.5** — Agno integrates with 12+ observability platforms (Langfuse, LangSmith, Arize, LangWatch, etc.) for tracing, cost tracking, and debugging.

---

## Part 7: Skills & Specialization

| Question | Your Answer |
|---|---|
| **7.1** Does the agent need specialized domain expertise? *Examples: Legal knowledge, medical guidelines, coding standards, company policies. Pick one: Yes (describe domain) · No — general knowledge is sufficient · Multiple domains (list them)* | |
| **7.2** Should the agent have specific role-play instructions? *Describe the agent's persona, tone, and behavioral rules. E.g., "You are a helpful but concise technical support agent" · "You are a strict compliance auditor who never makes assumptions" · "You are a creative brainstorming partner who always offers multiple options"* | |

> **Why we ask:**
> - **7.1** — Agno's **Skills** system lets you load domain expertise (instructions, scripts, reference docs) that the agent can progressively discover and use. This keeps the context window efficient while providing deep knowledge on demand.
> - **7.2** — This becomes the **system prompt / instructions** — the most important context engineering element. It shapes everything the agent says and does.

---

## Part 8: Budget & Constraints

| Question | Your Answer |
|---|---|
| **8.1** What are your cost constraints? *Pick one: Minimize cost · Balanced · Performance first* | |
| **8.2** What are your latency requirements? *Pick one: Real-time (sub-second) · Conversational (a few seconds) · Batch (minutes/hours acceptable)* | |
| **8.3** What environment will this run in? *Pick one: Local machine · Docker container · Cloud server (AWS, GCP, Azure) · AgentOS · Don't know / Recommend for me* | |

> **Why we ask:**
> - **8.1** — Model choice and tool usage directly affect cost. We can also use **response models** (a cheaper model for final output) and **token caching** to reduce expenses.
> - **8.2** — Affects model choice, streaming options, and whether we can use reasoning capabilities (which add latency for better quality).
> - **8.3** — Determines database choices, local tool access (file system, shell), and deployment configuration.

---

## Quick Reference: Answer → Agno Feature Map

| Your Answer | Agno Feature |
|---|---|
| "It needs to search the web" | `DuckDuckGoTools`, `TavilyTools`, `ExaTools`, etc. |
| "It needs to read PDFs/documents" | Knowledge with `PDFReader`, `DoclingReader` |
| "It needs to remember users" | `update_memory_on_run=True` or `enable_agentic_memory=True` |
| "It needs to learn and improve" | `learning=True` with Learning Stores |
| "It needs to query a database" | `PostgresTools`, `DuckDBTools`, etc. |
| "It should think before answering" | Reasoning: `ReasoningTools` or `reasoning_model=` |
| "Multiple specialists needed" | `Team` with member `Agent`s |
| "Predictable pipeline needed" | `Workflow` with sequential/conditional steps |
| "Need human approval for actions" | HITL: `UserConfirmation`, `ExternalExecution` |
| "Need structured output" | `output_schema=MyPydanticModel` |
| "Need to detect PII" | `PIIDetectionGuardrail` |
| "Need to block prompt injection" | `PromptInjectionGuardrail` |
| "Need to track state across turns" | `session_state={"key": "value"}` |
| "Need domain expertise loaded on demand" | `Skills` with `LocalSkills` |
| "Need to schedule runs" | AgentOS `Scheduler` |
| "Need to deploy as Slack bot" | AgentOS `Slack` interface |
| "Need to deploy as API" | AgentOS custom `FastAPI` or CLI |
| "Need to connect external tools" | `MCPTools` |
| "Need observability" | Langfuse, LangSmith, Arize, etc. |
| "Need to validate input" | Custom `pre_hooks` |
| "Need to validate output" | Custom `post_hooks` |
| "Need multimodal input" | Image/Audio/Video in input model |
| "Need a vector database" | 20+ options: LanceDB, pgvector, ChromaDB, Pinecone, etc. |
| "Need session persistence" | `db=SqliteDb()` / `PostgresDb()` / etc. |

---

## Filled-Out Example

> Here's what a completed template looks like for a **customer support agent**:

| Question | Answer |
|---|---|
| **1.1** Purpose | Customer support agent that answers questions about our product using documentation and past tickets. |
| **1.2** Users | Non-technical end users (customers). |
| **1.3** Cognitive mode | Aggregator — combines info from docs + tickets, doesn't add beyond sources. |
| **2.1** Complexity | Simple — one focused task → Single Agent. |
| **3.1** Knowledge sources | Product documentation (website URLs), past support tickets (CSV), FAQ (markdown). |
| **3.2** Memory | Remember user preferences (e.g., product tier, language). |
| **3.3** Storage | Recommend for me. |
| **4.1** Tools | Web search (for when docs don't cover it), calculator (for pricing questions). |
| **4.2** Human approval | No — the agent should be autonomous for answers, but flag uncertain responses. |
| **5.1** Reasoning | Moderate — think step-by-step when troubleshooting. |
| **5.2** Output | Markdown with structured sections. |
| **5.3** Guardrails | PII detection, prompt injection defense. |
| **5.4** State | Track the current issue category and resolution status. |
| **6.1** Interface | Web chat. |
| **6.2** Model | Default Ollama (glm-5.1:cloud). |
| **6.3** Multimodal | Text only. |
| **6.4** Schedule | No. |
| **6.5** Observability | Basic console logs. |
| **7.1** Skills | Customer support best practices. |
| **7.2** Persona | "You are a friendly, patient customer support agent. Always cite your sources. If you're unsure, say so rather than guessing." |
| **8.1** Cost | Balanced. |
| **8.2** Latency | Conversational (a few seconds). |
| **8.3** Environment | Cloud server. |

---

*This template ensures no Agno capability is overlooked and makes the design process accessible to non-technical users while producing precise, implementable specifications.*