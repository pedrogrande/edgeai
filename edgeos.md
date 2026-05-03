# EdgeOS

A multi-agent console [Agno](https://agno.com).

![EdgeOS home](docs/agno-agentos-home.jpg)
![EdgeOS agent studio](docs/agno-agentos-agent.jpg)

## Quick start (Mac)

### 1. Clone the repo

```bash
git clone https://github.com/pedrogrande/edgeOS.git
cd edgeOS
```

### 2. Install Docker

EdgeOS uses Docker to run a local PostgreSQL database for offline-first operation and bidirectional sync with Neon cloud.

**If you already have Docker:** skip to step 3.

<details>
<summary><strong>Install Docker Desktop (recommended)</strong></summary>

1. Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
2. Open the `.dmg` file and drag Docker to your Applications folder
3. Launch Docker from Applications — you'll see the whale icon in your menu bar
4. Wait for Docker to start (the icon stops animating when it's ready)
5. Verify in Terminal:

```bash
docker --version
docker compose version
```

</details>

<details>
<summary><strong>Install Docker via Homebrew</strong></summary>

```bash
brew install --cask docker
```

Then open Docker from your Applications folder and wait for it to start.

</details>

<details>
<summary><strong>Install Docker CLI only (OrbStack, Colima, etc.)</strong></summary>

If you prefer a lighter-weight Docker runtime:

```bash
# Option A: OrbStack (fastest, most Mac-native)
brew install orbstack

# Option B: Colima (open source)
brew install colima docker docker-compose
colima start
```

</details>

### 3. Create a Neon database

EdgeOS needs a Neon Postgres database for cloud storage and sync.

1. Go to [console.neon.tech](https://console.neon.tech) and sign up (free tier works)
2. Create a new project — choose a region close to you
3. Copy the connection string from the dashboard (it looks like `postgresql://neondb_owner:...@ep-xxx.neon.tech/neondb`)
4. Enable logical replication: **Settings → Logical Replication → Enable**
5. Create a replication role: **Roles → Create Role** → name it `replication_user`, copy the password

### 4. Run the setup script

This installs `uv` (Python package manager), creates a virtual environment, installs dependencies, starts local Postgres in Docker, and runs the database migration.

```bash
bash setup.sh
```

### 5. Fill in your credentials

Open the `.env` file that was created and add your values:

```bash
# ── Required ──────────────────────────────────────────────────────────
DB_URL=postgresql+psycopg://replication_user:your_password@ep-xxx.neon.tech/neondb?sslmode=require
OLLAMA_API_KEY=...                 ← your Ollama Cloud key (see Appendix)
OPENAI_API_KEY=...                 ← [OpenAI key](https://developers.openai.com/)

# ── Local DB (auto-configured by setup.sh) ─────────────────────────────
LOCAL_DB_URL=postgresql+psycopg://edgeos:edgeos_local@localhost:5433/edgeos

# ── Optional tool API keys ─────────────────────────────────────────────
EXA_API_KEY=...                   ← [Exa AI web search](https://exa.ai/)
LINEAR_API_KEY=...                ← [Linear project management](https://linear.app/docs/api-and-webhooks)
LINKUP_API_KEY=...                ← [Linkup search](https://www.linkup.so/)
TAVILY_API_KEY=...                ← [Tavily agent orchestration](https://www.tavily.com/)
SERPER_API_KEY=...                ← [Serper search](https://serper.dev/)
```

### 6. Set up bidirectional sync

This configures replication between your local Postgres and Neon cloud:

```bash
bash scripts/setup-replication.sh
```

This sets up:
- **Neon → Local**: PostgreSQL logical replication (changes on Neon appear locally)
- **Local → Neon**: Pull-based sync via `sync-to-neon.py` (no tunnel needed!)

### 7. Run EdgeOS

```bash
source .venv/bin/activate
python edgeos.py
```

The server starts on **http://localhost:7777**.

### 8. Connect to Agno AgentOS

Go to [os.agno.com](https://os.agno.com) and log in with your Agno account (create one if you don't have one).

Connect EdgeOS using the **"Connect AgentOS"** button in the sidebar, and enter the URL `http://localhost:7777`.

See video and info here: https://docs.agno.com/agent-os/connect-your-os

Now you can start building agents and teams in the AgentOS Studio!

---

## Offline-first architecture

EdgeOS runs a local PostgreSQL database in Docker alongside a sync sidecar that keeps it in sync with Neon cloud:

```
┌─────────────────────────────────────────────────────┐
│  Docker Compose                                      │
│                                                      │
│  ┌──────────────┐    ┌────────────────────────────┐ │
│  │  postgres     │    │  sync (sync-to-neon.py)    │ │
│  │  (local DB)  │◄───│  Polls updated_at changes   │──┼──► Neon Cloud
│  │              │rep │  Pushes upserts/deletes     │ │    (DB_URL)
│  │  sub_from_   │    │  Every 5 seconds           │ │
│  │  neon (✅)   │    └────────────────────────────┘ │
│  └──────────────┘                                   │
└─────────────────────────────────────────────────────┘
```

| Direction | Mechanism | Needs tunnel? |
|-----------|-----------|---------------|
| Neon → Local | PostgreSQL logical replication | No |
| Local → Neon | Pull-based sync (`sync-to-neon.py`) | No |

**Benefits:**
- **Offline-first**: Your app reads/writes to local Postgres — works without internet
- **Low latency**: No cloud round-trip for reads/writes
- **Auto-sync**: Changes sync to Neon when you're back online
- **No extra apps**: Everything runs in Docker — no ngrok, Tailscale, etc.

### Sync commands

```bash
# Start everything (Postgres + sync sidecar)
docker compose up -d

# Check sync health
bash scripts/sync-status.sh

# Manual one-shot sync
python scripts/sync-to-neon.py --once

# View sync logs
docker compose logs -f sync

# Repair broken sync
bash scripts/repair-sync.sh
```

---

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `DB_URL` | ✅ | Neon Postgres connection string |
| `LOCAL_DB_URL` | ✅ | Local Postgres connection string (auto-configured) |
| `OLLAMA_API_KEY` | ✅ | Ollama Cloud API key |
| `OPENAI_API_KEY` | ✅ | OpenAI API key (embeddings) |
| `NEON_REPL_USER` | For sync | Neon replication role name |
| `NEON_REPL_PASSWORD` | For sync | Neon replication role password |
| `SYNC_INTERVAL` | Optional | Seconds between sync cycles (default: 5) |
| `EXA_API_KEY` | Optional | Exa AI web search |
| `LINEAR_API_KEY` | Optional | Linear project management |
| `LINKUP_API_KEY` | Optional | Linkup search |

See `.env.example` for the full list.

---

## Manual setup (if you prefer)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create venv and install deps
uv venv --python 3.12
source .venv/bin/activate
uv pip install -r requirements.txt

# Configure environment
cp .env.example .env
# edit .env with your values

# Start local Postgres
docker compose up -d

# Migrate local database
python scripts/migrate-local-db.py

# Set up bidirectional sync
bash scripts/setup-replication.sh

# Run
python edgeos.py
```

---

## Appendix: Setting up Ollama Cloud

1. Go to [Ollama Cloud](https://ollama.com/cloud) and create an account.
2. Create an API key in the dashboard and copy it to your `.env` file as `OLLAMA_API_KEY`.

![Ollama home](docs/Ollama-home.jpg)
![Ollama Cloud dashboard](docs/Ollama-cloud.jpg)
![Ollama API Key](docs/Ollama-keys.jpg)