"""
AgentOS Demo

Prerequisites:
uv pip install -U fastapi uvicorn sqlalchemy pgvector psycopg ollama mcp python-dotenv openai
"""

import os

from dotenv import load_dotenv

load_dotenv()

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.ollama import OllamaResponses
from agno.os import AgentOS
from agno.registry import Registry
from agno.team import Team
from agno.tools.calculator import CalculatorTools
from agno.tools.hackernews import HackerNewsTools
from agno.tools.mcp import MCPTools
from agno.vectordb.pgvector import PgVector

# Database connection — override AGNO_DB_URL for Supabase, defaults to local Docker
db_url = os.environ.get("postgresql+psycopg://edgeai:edgeai@localhost:5532/edgeai")

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

# Create your agents
agno_agent = Agent(
    name="Agno Agent",
    model=OllamaResponses(id="glm-5.1:cloud"),
    tools=[MCPTools(transport="streamable-http", url="https://docs.agno.com/mcp")],
    db=db,
    update_memory_on_run=True,
    knowledge=knowledge,
    markdown=True,
)

simple_agent = Agent(
    name="Simple Agent",
    role="Simple agent",
    id="simple_agent",
    model=OllamaResponses(id="glm-5.1:cloud"),
    instructions=["You are a simple agent"],
    db=db,
    update_memory_on_run=True,
)

research_agent = Agent(
    name="Research Agent",
    role="Research agent",
    id="research_agent",
    model=OllamaResponses(id="glm-5.1:cloud"),
    instructions=["You are a research agent"],
    tools=[HackerNewsTools()],
    db=db,
    update_memory_on_run=True,
)

# Create a team
research_team = Team(
    name="Research Team",
    description="A team of agents that research the web",
    members=[research_agent, simple_agent],
    model=OllamaResponses(id="glm-5.1:cloud"),
    id="research_team",
    instructions=[
        "You are the lead researcher of a research team! 🔍",
    ],
    db=db,
    update_memory_on_run=True,
    add_datetime_to_context=True,
    markdown=True,
)

# Create the Registry for AgentOS Studio
registry = Registry(
    name="AgentOS Demo Registry",
    tools=[
        HackerNewsTools(),
        CalculatorTools(),
        MCPTools(transport="streamable-http", url="https://docs.agno.com/mcp"),
    ],
    models=[OllamaResponses(id="glm-5.1:cloud")],
    dbs=[db],
    vector_dbs=[vector_db],
)

# Create the AgentOS
agent_os = AgentOS(
    id="agentos-demo",
    agents=[agno_agent],
    teams=[research_team],
    registry=registry,
    db=db,
)
app = agent_os.get_app()


if __name__ == "__main__":
    agent_os.serve(app="demo:app", port=7777)
