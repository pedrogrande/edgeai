"""
EdgeAI - AgnoOS

Prerequisites:
uv pip install -U fastapi uvicorn sqlalchemy pgvector psycopg ollama mcp python-dotenv openai ddgs toolbox-core

Add agents by dropping .py files into the agents/ directory.
Each file should expose at least one module-level Agent or Team instance.
Expose MCPTools instances as public module-level variables (no leading underscore)
to have them auto-connected during startup and disconnected on shutdown.
"""

import importlib
import inspect
import pkgutil
import sys
from contextlib import AsyncExitStack, asynccontextmanager
from pathlib import Path

import os
from dotenv import load_dotenv

load_dotenv()

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.os import AgentOS
from agno.team import Team
from agno.tools.mcp import MCPTools
from agno.vectordb.pgvector import PgVector
from fastapi import FastAPI

# Database connection
db_url = "postgresql+psycopg://edgeai:edgeai@localhost:5533/edgeai"

# Create Postgres-backed memory store
db = PostgresDb(db_url=db_url)

# Create Postgres-backed vector store with OpenAI embedder
vector_db = PgVector(
    db_url=db_url,
    table_name="agno_docs",
    embedder=OpenAIEmbedder(id="text-embedding-3-small"),
)
knowledge = Knowledge(
    name="Agno Docs",
    contents_db=db,
    vector_db=vector_db,
)


def discover_agents(agents_dir: str = "agents") -> tuple[list, list]:
    """Auto-discover Agent/Team instances and MCPTools instances from the agents directory.

    Drop any .py file into agents/ and it will be registered automatically.
    - Agent/Team instances are registered with AgentOS.
    - MCPTools instances (public names, no leading underscore) are connected
      during startup via the FastAPI lifespan.
    """
    agents = []
    toolboxes = []
    agents_path = Path(agents_dir)
    repo_root = str(Path(__file__).parent)

    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    for module_info in pkgutil.iter_modules([str(agents_path)]):
        try:
            module = importlib.import_module(f"{agents_dir}.{module_info.name}")
            for name, obj in inspect.getmembers(module):
                if name.startswith("_"):
                    continue
                if isinstance(obj, (Agent, Team)):
                    agents.append(obj)
                elif isinstance(obj, MCPTools):
                    toolboxes.append(obj)
        except Exception as e:
            print(
                f"[edgeai] Warning: could not load agents/{module_info.name}.py — {e}"
            )

    return agents, toolboxes


_agents, _toolboxes = discover_agents("agents")


@asynccontextmanager
async def _lifespan(app: FastAPI):
    """Connect MCPTools instances on startup; close them on shutdown."""
    async with AsyncExitStack() as stack:
        for tb in _toolboxes:
            try:
                await stack.enter_async_context(tb)
                print(f"[edgeai] Connected MCP tool: {tb}")
            except Exception as e:
                print(
                    f"[edgeai] Warning: MCP tool failed to connect ({e}) — continuing without it"
                )
        yield


_base_app = FastAPI(lifespan=_lifespan)


# Create the AgentOS
agent_os = AgentOS(
    id="edgeai",
    db=db,
    agents=_agents,
    base_app=_base_app,
)
app = agent_os.get_app()


if __name__ == "__main__":
    agent_os.serve(app="edgeai:app", port=8000)
