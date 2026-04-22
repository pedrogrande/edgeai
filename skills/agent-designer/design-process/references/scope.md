# Phase 2: SCOPE

## Goal
Determine the agent's architecture, tooling, knowledge needs, memory, and storage.

## Decisions to Make

### 2.1 Architecture
- **Simple** → Single Agent (one focused task)
- **Moderate** → Workflow (multiple steps, predictable flow)
- **Complex** → Team (multiple specialists coordinating dynamically)
- **Very complex** → Workflow with Teams inside

Recommendation: Start simple. Only add complexity when the task genuinely needs it.

If Team or Workflow: list the sub-roles/steps and what each is responsible for.

### 2.2 Tools
Check the Agno docs for available tools. Key categories:
- 📚 Information & Research (web search, scraping, ArXiv, HackerNews, Wikipedia)
- 💬 Communication (Email, Slack, Discord, Telegram)
- 📊 Data & Databases (SQL, spreadsheets, Pandas)
- 🛠️ Productivity (GitHub, Jira, Notion, Google Calendar)
- 💰 Finance (Yahoo Finance, OpenBB)
- 🎨 Media (DALL-E, Fal, ElevenLabs)
- 🔧 System & Code (Shell, Python, File system, Docker)
- 🌐 Web & APIs (Custom APIs, MCP, Browser tools)

Don't over-tool — add only what the use case requires.

### 2.3 Knowledge
What information does the agent need?
- Company documents, product docs, website content
- Database data, real-time web search, research papers
- Code repositories, legal texts, support tickets

Check Agno docs for knowledge base types (PgVector, LanceDB, Pinecone, Milvus, etc.).

### 2.4 Memory
- **No memory** — each conversation starts fresh
- **User memory** — recall preferences across sessions
- **Organizational memory** — accumulate shared insights
- **Both**

### 2.5 Storage
- Local file (SQLite) — simple, free, one machine
- PostgreSQL — shared, scalable, multi-user
- MongoDB — good for unstructured JSON
- Redis — fast, temporary/cached data

## Tips
- Present options with tradeoffs explained plainly for non-technical users.
- If the user is unsure, make a recommendation and explain why.
- Verify tool availability in Agno docs BEFORE recommending.