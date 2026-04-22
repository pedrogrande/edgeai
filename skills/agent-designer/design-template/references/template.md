# Agno Agent Design Template

## Agent design principles

Every element collapses into two questions per layer that must be answered before an agent is deployed. Unanswered questions are guaranteed future failure modes.

| Layer                | Fidelity question                                                                                                                   | Enrichment question                                                                                                                                                 |
| :------------------- | :---------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Purpose**          | Why does this agent exist, and what human need does it serve?                                                                       | What does the human gain — in capability, understanding, or possibility space — from this interaction? Can they now perform unassisted at higher quality?           |
| **Identity**         | What is this agent's role, orientation, and capability boundary?                                                                    | What epistemic metadata does this agent contract to attach to its outputs, and does its orientation contribute cognitive diversity to the pipeline?                 |
| **Specification**    | Are criteria verifiable, pre-existing, and type-resolved?                                                                           | Was the option space explored and a direction chosen before criteria were written? Do the acceptance criteria specify which information types must be decomposable? |
| **Context**          | What is the minimum information this agent needs, and when? What information boundaries are structurally enforced?                  | What epistemic context does the agent receive from upstream? Is that context typed or raw prose?                                                                    |
| **Trust**            | Who verifies this work, at what independence level, and how is that level selected?                                                 | Do belief revision protocols allow the pipeline to improve its reasoning, not just verify its outputs? Is the audit trail assurance level matched to task stakes?   |
| **Safety**           | What are the fail-safe defaults, and where are the human gates? What recovery protocol operates when the agent halts?               | Is cognitive diversity at the organisational level being actively preserved, not just individual output quality?                                                    |
| **Ecosystem**        | Is the architecture matched to task structure? What is the per-invocation cost ceiling?                                             | Are pipelines designed as epistemic exchanges? Is coalition formation by epistemic complementarity? Is diversity monitored?                                         |
| **Improvement**      | Are output quality, rework rates, and specification aging tracked?                                                                  | Is pipeline intelligence — downstream capability gain — being measured alongside output accuracy?                                                                   |
| **Human Enrichment** | Can the human now perform the task unassisted at higher quality than before? (Unverified enrichment is unconfirmed, not confirmed.) | Is every human more capable after every interaction than before it? Is the Scaffolding Dependency Index narrowing or widening?                                      |

---

## Part 1: Purpose & People

| Question | Your Answer |
|---|---|
| **1.1** What is the agent supposed to do? *In 1–3 sentences, describe the job this agent performs. What problem does it solve? What does a successful outcome look like?* | |
| **1.2** Who will use this agent? *Choose one or describe: Non-technical end users · Semi-technical users · Developers/engineers · Other agents/automated systems · Internal team members* | |
| **1.3** What kind of cognitive work does the agent primarily do? *Pick one: **Extractor** — Gathers/collects information. Never judges. · **Measurer** — Quantifies/measures against criteria. Never interprets. · **Assessor** — Evaluates against standards. Human makes the final call. · **Generator** — Produces content/drafts. Must be verified. · **Aggregator** — Combines/synthesizes. Must not add beyond inputs.* | |

## Part 2: Architecture

| Question | Your Answer |
|---|---|
| **2.1** How complex is the task? *Pick one: **Simple** — One focused task → Single Agent · **Moderate** — Multiple steps, predictable flow → Workflow · **Complex** — Multiple specialists coordinating dynamically → Team · **Very complex** — Mix of predictable and dynamic → Workflow with Teams inside* | |
| **2.2** If you chose "Team" or "Workflow," what are the sub-roles or steps? *List each role/step and what it's responsible for. E.g., Researcher → searches web; Analyst → evaluates credibility; Writer → produces report.* | |

## Part 3: Data & Knowledge

| Question | Your Answer |
|---|---|
| **3.1** What information does the agent need to know about? *Choose all that apply: Company documents · Product documentation · Website content (specify URLs) · Database data (SQL, CSVs) · Real-time web search · Research papers (arXiv, PubMed) · Code repositories (GitHub, GitLab) · Legal/regulatory texts · Customer support tickets/FAQs · Other (describe)* | |
| **3.2** Should the agent be able to learn and remember over time? *Pick one: **No** — Each conversation starts fresh · **Remember user preferences** — Recall things about individual users across sessions · **Remember organizational knowledge** — Accumulate insights for all users · **Both** — Per-user and per-organization memory* | |
| **3.3** Where should stored data live? *Pick one: Local file (SQLite) · PostgreSQL · MongoDB · Redis · Don't know / Recommend for me* | |

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

## Part 5: Intelligence & Behavior

| Question | Your Answer |
|---|---|
| **5.1** How much "thinking" does the agent need to do? *Pick one: **Quick responses** — Fast, no deep reasoning · **Moderate reasoning** — Think step-by-step before answering · **Deep analysis** — Reason carefully through complex, multi-step problems* | |
| **5.2** What should the output look like? *Pick one: Free-form text · Markdown · Structured data (JSON, Pydantic) · Mixed (depends on the question)* | |
| **5.3** What guardrails or safety rules should the agent follow? *Choose all that apply: PII detection · Prompt injection defense · Content moderation · Input validation · Output validation · Custom rules (describe) · None needed* | |
| **5.4** Should the agent maintain state across a conversation? *Examples: a shopping cart, a to-do list, a draft document being built up over multiple turns. Pick one: Yes (describe the state) · No — each response is independent* | |

## Part 6: Deployment & Integration

| Question | Your Answer |
|---|---|
| **6.1** How will users interact with this agent? *Choose all that apply: Web chat · Slack bot · Discord bot · Telegram bot · WhatsApp bot · REST API · MCP Server · CLI · Custom (describe)* | |
| **6.2** What model should the agent use? *Pick one: **Default** — Ollama `glm-5.1:cloud` (recommended) · Different Ollama model (specify) · OpenAI (requires API key) · Anthropic Claude (requires API key) · Google Gemini (requires API key) · Other (specify) · Recommend for me* | |
| **6.3** Do you need multi-modal input/output? *Choose all that apply: Images · Audio · Video · Files (PDFs, docs, spreadsheets) · Text only* | |
| **6.4** Do you need the agent to run on a schedule? *Examples: daily report generation, weekly summaries, periodic data checks. Pick one: Yes (describe schedule) · No — on-demand only* | |
| **6.5** Do you need observability / monitoring? *Pick one: Yes — trace runs, monitor costs, debug issues · Basic — just console logs · Advanced — full tracing (Langfuse, LangSmith, Arize, etc.)* | |

## Part 7: Skills & Specialization

| Question | Your Answer |
|---|---|
| **7.1** Does the agent need specialized domain expertise? *Examples: Legal knowledge, medical guidelines, coding standards, company policies. Pick one: Yes (describe domain) · No — general knowledge is sufficient · Multiple domains (list them)* | |
| **7.2** Should the agent have specific role-play instructions? *Describe the agent's persona, tone, and behavioral rules. E.g., "You are a helpful but concise technical support agent" · "You are a strict compliance auditor who never makes assumptions" · "You are a creative brainstorming partner who always offers multiple options"* | |

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