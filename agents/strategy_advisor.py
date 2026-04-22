"""
Business Strategy Advisor Agent (v2)
=====================================

A conversational agent that helps users develop business strategy through
collaborative dialogue. It saves strategic artifacts as markdown files with
YAML front matter to `artifacts/strategy/` for the Document Manager Agent
to ingest into its knowledge base.

Key changes from v1:
- Storage: PostgresDb (shared platform DB) instead of SqliteDb
- Vector DB: PgVector (shared platform DB) instead of LanceDb
- Artifact saving: StrategyArtifactTools (markdown files with front matter)
  instead of bare function → Knowledge.insert()
- Learning knowledge: Dedicated PgVector table instead of shared LanceDb
- Removed artifact Knowledge base (Document Manager handles KB ingestion)
- Embedder: Explicit OpenAIEmbedder(id="text-embedding-3-small")

Key Agno features used:
- ReasoningTools for step-by-step strategic analysis
- Agentic Memory (user context + preferences across sessions)
- Entity Memory (companies, competitors, market entities — shared globally)
- Learned Knowledge (strategic insights transferable across users — propose mode)
- PgVector for learning vector storage
- DuckDuckGo search (market research)
- FileTools (read/write local strategy documents)
- StrategyArtifactTools (save/list/read strategy artifact files)
- HITL confirmation before saving artifacts

Setup:
1. Install dependencies:  uv pip install -U "agno[all]" ddgs psycopg[binary] pgvector
2. Start PostgreSQL:      docker compose up -d edgeai-postgres
3. Install Ollama:        https://ollama.com/install
4. Pull the model:        ollama pull glm-5.1:cloud
5. Set API keys:          export OLLAMA_API_KEY=your_key
                          export OPENAI_API_KEY=your_key
6. Run standalone:        python agents/strategy_advisor.py
7. Run via AgentOS:       python edgeai.py
"""

import os
from pathlib import Path
from textwrap import dedent

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.learn import (
    EntityMemoryConfig,
    LearnedKnowledgeConfig,
    LearningMachine,
    LearningMode,
)
from agno.models.ollama import Ollama
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.file import FileTools
from agno.tools.reasoning import ReasoningTools
from agno.vectordb.pgvector import PgVector

# Import custom toolkit
from tools.strategy_artifact_tools import StrategyArtifactTools

# ---------------------------------------------------------------------------
# Database — shared platform PostgreSQL instance
# All storage (sessions, memory, learning) uses this one database.
# ---------------------------------------------------------------------------
_raw_db_url = os.environ.get(
    "DATABASE_URL", "postgresql+psycopg://edgeai:edgeai@localhost:5533/edgeai"
)
db_url = _raw_db_url.replace("postgresql://", "postgresql+psycopg://", 1)
agent_db = PostgresDb(db_url=db_url)

# ---------------------------------------------------------------------------
# Learning Knowledge Base — stores entity memory and learned knowledge vectors
# Uses PgVector (shared platform DB) with OpenAI embedder.
# This is separate from artifact storage — the Document Manager Agent handles
# artifact knowledge base ingestion.
# ---------------------------------------------------------------------------
learning_kb = Knowledge(
    name="Strategy Learning",
    description="Entity memory (companies, competitors) and learned strategic insights shared across all users",
    vector_db=PgVector(
        table_name="strategy_learning",
        db_url=db_url,
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    ),
    max_results=5,
    contents_db=agent_db,  # Track metadata in same PostgreSQL DB
)

# ---------------------------------------------------------------------------
# Agent Instructions
# ---------------------------------------------------------------------------
SYSTEM_INSTRUCTIONS = dedent(
    """\
    You are a collaborative strategy advisor — not a consultant who delivers answers,
    but a thinking partner who helps the user develop their own strategic clarity.

    ## Your Approach

    1. **Listen First**: Before offering frameworks or analysis, understand the user's
       context, goals, and constraints through thoughtful questions.
    2. **Surface Assumptions**: Make implicit assumptions explicit. Ask "What leads you
       to believe that?" and "What would have to be true for this to work?"
    3. **Offer Multiple Options**: Present 2-3 strategic alternatives rather than a single
       recommendation. Help the user weigh trade-offs.
    4. **Distinguish Analysis from Opinion**: Clearly label what is analysis (based on
       observable data) vs. opinion or speculation. Never present speculation as certainty.
    5. **Frame Strategy as Hypotheses**: Every strategy is a hypothesis to test, not a
       proven fact. Always suggest how to validate or invalidate strategic assumptions.

    ## Strategy Frameworks You Know

    You draw from these frameworks as appropriate:
    - Porter's Five Forces (industry analysis)
    - SWOT Analysis (strengths, weaknesses, opportunities, threats)
    - Blue Ocean Strategy (value innovation)
    - Business Model Canvas (9 building blocks)
    - Value Proposition Canvas (customer jobs, pains, gains)
    - Jobs-to-be-Done (customer motivation)
    - OKRs (objectives and key results)
    - Ansoff Matrix (growth strategies)
    - BCG Matrix (portfolio analysis)
    - VRIO Framework (competitive advantage)
    - Balanced Scorecard (performance measurement)
    - Lean Startup (build-measure-learn)

    Do NOT force frameworks on the user. Use them only when they genuinely clarify
    the strategic question at hand.

    ## Saving Artifacts

    When a conversation produces a useful artifact — a completed framework, a strategy
    document, a competitive analysis, a reusable template — follow this process:

    1. **Propose**: Present the artifact and ask "Would you like me to save this for
       future reference?"
    2. **Wait**: Do NOT call save_artifact until the user explicitly says yes.
    3. **Save**: Once confirmed, call the save_artifact tool with:
       - A descriptive title (e.g., "SWOT Analysis: Acme Corp Q4 2025")
       - The appropriate artifact_type: strategy, framework, analysis, template, or insight
       - The full markdown content (structured, specific, actionable)
       - Relevant tags (comma-separated)

    ## Guardrails

    - Never present a strategy as "proven" — always frame as a hypothesis to test
    - Always surface assumptions and risks alongside recommendations
    - Never make financial projections without explicit disclaimers
    - If you're unsure about something, say so rather than guessing
    - Focus on the user's specific context — avoid generic advice without grounding
"""
)

# ---------------------------------------------------------------------------
# Create the Agent
# ---------------------------------------------------------------------------
strategy_advisor = Agent(
    name="Strategy Advisor",
    model=Ollama(id="glm-5.1:cloud"),
    instructions=SYSTEM_INSTRUCTIONS,
    # --- Storage (PostgresDb instead of SqliteDb) ---
    db=agent_db,
    # --- Tools ---
    tools=[
        ReasoningTools(add_instructions=True),
        DuckDuckGoTools(),
        FileTools(base_dir=Path("artifacts/strategy")),
        StrategyArtifactTools(),
    ],
    # --- Learning Machine ---
    # Agentic memory: user preferences across sessions (backed by PostgresDb)
    # Entity memory: companies, competitors, market entities (shared globally)
    # Learned knowledge: strategic insights transferable across users (propose mode
    #   so the user confirms before saving)
    learning=LearningMachine(
        entity_memory=EntityMemoryConfig(
            mode=LearningMode.AGENTIC,  # Agent actively manages entities
            namespace="global",  # Shared across all users
        ),
        learned_knowledge=LearnedKnowledgeConfig(
            mode=LearningMode.PROPOSE,  # Agent proposes, user confirms
            namespace="global",  # Insights available to all users
        ),
        knowledge=learning_kb,  # Learned knowledge uses dedicated PgVector
    ),
    enable_agentic_memory=True,  # Agent manages user memories explicitly
    # --- Knowledge (learning only — no artifact knowledge base) ---
    # The agent uses search_knowledge to find previously learned entities/insights.
    # Artifact knowledge base ingestion is handled by the Document Manager Agent.
    knowledge=learning_kb,
    search_knowledge=True,  # Gives agent a search_knowledge_base() tool
    # --- Session State ---
    # Tracks evolving strategy context within a conversation
    session_state={
        "current_strategic_question": None,
        "draft_artifacts": [],  # Artifacts being developed this session
        "decisions_made": [],  # Decisions confirmed this session
        "open_items": [],  # Unresolved questions this session
    },
    add_session_state_to_context=True,
    enable_agentic_state=True,  # Agent can update state based on context
    # --- Context settings ---
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=10,  # Remember last 10 exchanges
    # --- Output ---
    markdown=True,
)

# ---------------------------------------------------------------------------
# Run the Agent (standalone mode)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Interactive conversation loop
    print("=" * 70)
    print("  Strategy Advisor Agent (v2)")
    print("  Type your strategic questions, or 'exit' to quit.")
    print("=" * 70)

    while True:
        user_input = input("\n🧑 You: ").strip()
        if user_input.lower() in ("exit", "quit", "bye"):
            print("Goodbye! Your conversation and artifacts are saved.")
            break

        if not user_input:
            continue

        strategy_advisor.print_response(user_input, stream=True)
