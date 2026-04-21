# AgnoOS — Local Agent Runtime

A local AI agent platform built on the [Agno](https://docs.agno.com) framework.  
Run AI agents on your machine, manage them through [os.agno.com](https://os.agno.com), and design new agents with the built-in **Agent Designer**.

---

## What's included

| Component | What it does |
|-----------|-------------|
| **Agent Designer** | A conversational agent that helps you design, specify, and save new Agno agents |
| **Agno Docs Database** | A local, queryable knowledge base of Agno API docs — used by the Agent Designer to look up correct APIs |
| **AgentOS Runtime** | A FastAPI server that auto-discovers and serves all agents in the `agents/` folder |
| **os.agno.com UI** | Web control plane for chatting with, monitoring, and managing your agents |

---

## Before you start

Make sure you have these installed:

- **[Docker Desktop](https://www.docker.com/products/docker-desktop/)** — runs the local database and toolbox
- **[Python 3.12+](https://www.python.org/downloads/)** — runs the agent server
- **[Ollama](https://ollama.com/download)** — runs the AI models locally
- **[uv](https://docs.astral.sh/uv/getting-started/installation/)** — fast Python package manager (the setup script installs this automatically if missing)

You'll also need these accounts/keys:

- **[OpenAI API key](https://platform.openai.com/api-keys)** — used for document embeddings (knowledge search)
- **[Ollama Cloud API key](https://ollama.com)** — needed if you use Ollama's hosted models
- **[Supabase](https://supabase.com) project** — stores agent specs (free tier works fine)

---

## Setup

### 1. Pull the model

Open a terminal and pull the default model:

```bash
ollama pull glm-5.1:cloud
```

> You can use any Ollama model — `glm-5.1:cloud` is the default used by all agents in this project.

---

### 2. Configure your environment

Copy the example env file and fill in your keys:

```bash
cp .env.example .env
```

Open `.env` in a text editor and fill in:

```
OPENAI_API_KEY=sk-...              # From platform.openai.com/api-keys
OLLAMA_API_KEY=...                 # From your Ollama account
SUPABASE_DB_URL=postgresql://...   # From your Supabase project (see below)
AGENT_SPEC_USER_ID=...             # Your Supabase auth user UUID (see below)
AGENT_SPEC_DESIGN_SYSTEM_ID=       # Leave blank for now — the Agent Designer creates this
```

**Getting your Supabase values:**

1. Go to your [Supabase dashboard](https://supabase.com/dashboard) → select your project
2. Go to **Project Settings → Database → Connection string**
3. Choose **Session pooler** (port 5432) and copy the URL — it looks like:
   `postgresql://postgres.[ref]:[password]@aws-1-[region].pooler.supabase.com:5432/postgres`
4. For `AGENT_SPEC_USER_ID`: go to **Authentication → Users**, find your user, and copy the UUID

---

### 3. Run the database migrations on Supabase

Go to your Supabase project → **SQL Editor** and run these two files **in order**:

1. Paste and run the contents of `db/migrations/001_create_design_system.sql`
2. Paste and run the contents of `db/migrations/002_create_agent_spec.sql`

> These create the tables the Agent Designer uses to save completed agent designs.

---

### 4. Run the setup script

This installs dependencies, starts the local database, and seeds the Agno docs knowledge base:

```bash
bash setup.sh
```

What it does:
- Installs `uv` if you don't have it
- Creates a Python virtual environment
- Installs all Python dependencies
- Starts Docker containers (local Postgres + MCP Toolbox)
- Applies the Agno docs database schema
- Seeds the database with Agno feature and documentation data

This takes a few minutes the first time. You'll see checkmarks as each step completes.

---

### 5. Activate the virtual environment

```bash
source .venv/bin/activate
```

> You need to do this each time you open a new terminal.

---

## Running the app

Start the AgentOS server:

```bash
uvicorn edgeai:app --host 0.0.0.0 --port 8000 --reload
```

You should see output like:
```
[edgeai] Connected MCP tool: ...
INFO:     Uvicorn running on http://0.0.0.0:8000
```

The server auto-discovers all agents in the `agents/` folder — no registration needed.

> To stop the server: press `Ctrl+C`

---

## Connecting to os.agno.com

[os.agno.com](https://os.agno.com) is the web UI for chatting with and managing your agents. It connects directly from your browser to the server running on your machine — no data goes through Agno's servers.

1. Go to [os.agno.com](https://os.agno.com) and sign in (or create a free account)
2. Click **"Add new OS"**
3. Fill in the connection form:
   - **Environment**: Local
   - **Endpoint URL**: `http://localhost:8000`
   - **OS Name**: e.g. `My Local AgentOS`
4. Click **CONNECT**

If the connection succeeds, your OS appears in the dashboard with status **"Running"** and your agents appear in the chat interface.

> **Note:** os.agno.com connects from your browser to `localhost:8000` — both need to be on the same machine. If you want to access the UI from a different device, you'll need to expose port 8000 using a tool like [ngrok](https://ngrok.com/): `ngrok http 8000`, then use the ngrok HTTPS URL as the Endpoint URL.

---

## Using the Agent Designer

The Agent Designer is a conversational agent that guides you through designing a new Agno agent and saves the completed spec to your Supabase database.

Chat with it in the os.agno.com UI (it appears as **"Agno Agent Designer"** in your agent list).

**The design process has 6 phases:**

| Phase | What happens |
|-------|-------------|
| **Discover** | The agent asks about your use case, users, and goals |
| **Scope** | Determines whether you need a single agent, team, or workflow |
| **Specify** | Defines model, tools, memory, knowledge, and output format |
| **Generate** | Produces a complete, runnable Python file + setup instructions |
| **Validate** | Checks all imports and API usage against the Agno docs |
| **Persist** | Saves the completed spec to Supabase and returns a spec UUID |

At the end of a design session you'll have:
- A Python agent file ready to drop into the `agents/` folder
- A saved spec row in Supabase (for future reference and code regeneration)
- Auto-derived pip dependencies, required env vars, and setup notes

---

## Adding a new agent

1. Save your agent Python file into the `agents/` folder
2. Make sure it has a module-level `Agent` or `Team` instance
3. Restart the server — it will be auto-discovered and appear in os.agno.com

---

## Project structure

```
agents/               Drop agent .py files here — auto-discovered on startup
db/
  migrations/         SQL migrations — run these on Supabase
  schema.sql          Agno docs database schema (for local Postgres)
  seed_agno_docs.py   Seeds the local Agno docs knowledge base
  tools.yaml          MCP Toolbox query definitions
tools/
  agent_spec_tools.py  Database tools used by the Agent Designer
docs/                  Design templates, principles, and schema documentation
data/                  Local SQLite files for agent memory
.env                   Your secrets (never commit this)
.env.example           Template — copy to .env and fill in
setup.sh               First-time setup script
edgeai.py              AgentOS server entry point
docker-compose.yml     Local Postgres + MCP Toolbox services
```

---

## Troubleshooting

**Docker containers not starting**
```bash
docker compose up -d
docker compose logs postgres
docker compose logs toolbox
```

**"MCP tool failed to connect" on startup**
The MCP Toolbox (port 5001) may still be starting. Wait 10–15 seconds and restart the server.
Check: `curl http://localhost:5001/api/toolsets`

**os.agno.com shows "Connection failed"**
- Confirm the server is running: `curl http://localhost:8000/health`
- Confirm you're using `http://localhost:8000` (not https)
- Check the browser console for CORS errors

**Agent Designer can't save specs**
- Confirm `SUPABASE_DB_URL` and `AGENT_SPEC_USER_ID` are set in `.env`
- Confirm you ran both SQL migrations on Supabase
- Check the terminal where the server is running for error output

**Ollama model not found**
```bash
ollama pull glm-5.1:cloud
ollama list   # confirm it appears
```

**Reset everything and start fresh**
```bash
docker compose down -v   # removes containers AND data volumes
bash setup.sh            # re-runs full setup
```
