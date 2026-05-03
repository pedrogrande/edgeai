#!/usr/bin/env bash
# =============================================================================
# EdgeAI setup — runs everything needed to start the app from scratch.
# Usage: bash setup.sh
# =============================================================================

set -euo pipefail

# ── Colours ──────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Colour

ok()   { echo -e "${GREEN}  ✓ $*${NC}"; }
info() { echo -e "${YELLOW}  → $*${NC}"; }
fail() { echo -e "${RED}  ✗ $*${NC}"; exit 1; }

echo ""
echo "╔══════════════════════════════╗"
echo "║    EdgeAI — First-time setup  ║"
echo "╚══════════════════════════════╝"
echo ""

# ── 1. Install uv if not present ─────────────────────────────────────────────
if ! command -v uv &>/dev/null; then
    info "uv not found — installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
    ok "uv installed"
else
    ok "uv already installed ($(uv --version))"
fi

# ── 2. Create virtual environment with Python 3.12 ────────────────────────────
if [ ! -d ".venv" ]; then
    info "Creating virtual environment (.venv)..."
    uv venv --python 3.12
    ok "Virtual environment created"
else
    ok "Virtual environment already exists"
fi

# ── 3. Install dependencies ───────────────────────────────────────────────────
info "Installing dependencies..."
uv pip install -r requirements.txt
ok "Dependencies installed"

# ── 4. Create .env from .env.example if it doesn't exist ─────────────────────
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ""
    echo -e "${YELLOW}  → Created .env from .env.example${NC}"
    echo -e "${RED}    ➜  Open .env and fill in your API keys before running.${NC}"
else
    ok ".env already exists"
fi

# ── 5. Prerequisites check ────────────────────────────────────────────────────
info "Checking prerequisites..."

command -v docker  >/dev/null 2>&1 || fail "Docker is not installed. Install it from https://www.docker.com/get-started"
command -v python3 >/dev/null 2>&1 || fail "Python 3 is not installed. Install it from https://www.python.org/downloads/"

# psql is optional — we can fall back to running schema via Python/psycopg
HAVE_PSQL=false
command -v psql >/dev/null 2>&1 && HAVE_PSQL=true

ok "Prerequisites OK"

# ── 6. Start Docker services ─────────────────────────────────────────────────
info "Starting Docker services (postgres + toolbox)..."

docker compose up -d

ok "Docker services started"

# ── 7. Wait for PostgreSQL to be ready ───────────────────────────────────────
info "Waiting for PostgreSQL to be ready..."

MAX_WAIT=60
ELAPSED=0
until docker compose exec -T postgres pg_isready -U edgeai -d edgeai >/dev/null 2>&1; do
    if [ "$ELAPSED" -ge "$MAX_WAIT" ]; then
        fail "PostgreSQL did not become ready within ${MAX_WAIT}s. Check: docker compose logs postgres"
    fi
    printf "."
    sleep 2
    ELAPSED=$((ELAPSED + 2))
done
echo ""

ok "PostgreSQL is ready"

# ── 8. Apply schema ──────────────────────────────────────────────────────────
info "Applying database schema..."

if [ "$HAVE_PSQL" = true ]; then
    psql postgresql://edgeai:edgeai@localhost:5533/edgeai -f db/schema.sql -q
else
    # Fall back to Python if psql is not installed
    python3 - <<'PYEOF'
import psycopg, pathlib, sys
sql = pathlib.Path("db/schema.sql").read_text()
try:
    with psycopg.connect("postgresql://edgeai:edgeai@localhost:5533/edgeai") as conn:
        conn.execute(sql)
        conn.commit()
except Exception as e:
    print(f"Schema error: {e}", file=sys.stderr)
    sys.exit(1)
PYEOF
fi

ok "Schema applied"

# ── 9. Seed the database ─────────────────────────────────────────────────────
# info "Seeding Agno docs data..."

# python3 db/seed_agno_docs.py

# ok "Database seeded"

# ── 10. Wait for MCP Toolbox to be ready ────────────────────────────────────
info "Waiting for MCP Toolbox to be ready..."

MAX_WAIT=60
ELAPSED=0
until curl -sf http://localhost:5001/api/toolsets >/dev/null 2>&1; do
    if [ "$ELAPSED" -ge "$MAX_WAIT" ]; then
        echo ""
        echo -e "${YELLOW}  ⚠ MCP Toolbox is not responding yet. It may still be starting.${NC}"
        echo "    Check with: docker compose logs toolbox"
        break
    fi
    printf "."
    sleep 2
    ELAPSED=$((ELAPSED + 2))
done

if curl -sf http://localhost:5001/api/toolsets >/dev/null 2>&1; then
    echo ""
    ok "MCP Toolbox is ready"
fi

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}╔══════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Setup complete! Run EdgeAI with: ║${NC}"
echo -e "${GREEN}║                                    ║${NC}"
echo -e "${GREEN}║   python3 edgeai.py                ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════╝${NC}"
echo ""
