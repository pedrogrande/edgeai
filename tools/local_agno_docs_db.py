"""
Agno Docs MCP Toolbox — factory and standalone CLI agent.

Import the async context manager in any agent that needs Agno docs access:

    from tools.local_agno_docs_db import agno_docs_toolbox

    async with agno_docs_toolbox() as docs_tools:
        agent = Agent(tools=[docs_tools], ...)

Run standalone for a CLI query session:
    python tools/local_agno_docs_db.py
"""

import asyncio
from contextlib import asynccontextmanager

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.mcp_toolbox import MCPToolbox

MCP_TOOLBOX_URL = "http://127.0.0.1:5001"

_ALL_TOOLSETS = ["agno-docs-search", "agno-docs-browse", "agno-docs-changes"]


@asynccontextmanager
async def agno_docs_toolbox(toolsets: list[str] | None = None):
    """
    Async context manager that yields a connected MCPToolbox for the Agno docs database.

    Args:
        toolsets: List of toolset names to load. Defaults to all three
                  (agno-docs-search, agno-docs-browse, agno-docs-changes).

    Usage:
        async with agno_docs_toolbox() as docs_tools:
            agent = Agent(tools=[docs_tools], ...)
    """
    async with MCPToolbox(
        url=MCP_TOOLBOX_URL,
        toolsets=toolsets or _ALL_TOOLSETS,
    ) as db_tools:
        yield db_tools


# ---------------------------------------------------------------------------
# Standalone CLI agent
# ---------------------------------------------------------------------------


async def _cli():
    async with agno_docs_toolbox() as db_tools:
        agent = Agent(
            name="Agno Docs Assistant",
            model=Ollama(id="glm-5.1:cloud"),
            tools=[db_tools],
            instructions=[
                "You are an expert assistant for Agno documentation.",
                "Use the available database tools to find features, doc pages,",
                "related pages, and recent changes.",
                "When a user asks about a feature, always check for colocated",
                "pages that cover the same topic from different perspectives.",
                "When reporting URLs, clearly indicate which are current.",
                "If a feature is marked experimental, say so.",
            ],
            markdown=True,
        )
        await agent.acli_app(stream=True)


if __name__ == "__main__":
    asyncio.run(_cli())
