"""
Business Strategy Advisor Agent v2
===================================

A collaborative strategy advisor that helps users develop strategic clarity
through dialogue — not a consultant who delivers answers, but a thinking
partner who surfaces assumptions, offers multiple options, and frames
strategies as testable hypotheses.

Key upgrades from v1:
- PostgresDb storage (shared platform DB instead of local SQLite)
- PgVector for learning vectors (shared platform DB instead of LanceDb)
- StrategyArtifactTools Toolkit (saves files with front matter instead of
  inserting directly into a knowledge base — Document Manager handles KB)
- Dedicated PgVector table for learning data (strategy_learning)
- Removed agent-owned artifact knowledge base (artifacts are now files)
- Session state tracking (current_strategic_question, decisions, etc.)
- Tool result caching on deterministic/external tools

Key Agno features used:
- ReasoningTools for deep structured analysis
- Agentic Memory (user context + preferences across sessions)
- Entity Memory (companies, competitors, market entities — shared globally)
- Learned Knowledge (strategic insights transferable across users — propose mode)
- PgVector for learning vector storage
- DuckDuckGo search (market research) — cached to avoid repeated API calls
- FileTools (read/write local strategy documents) — cached for reads
- StrategyArtifactTools (save/list/read artifact markdown files)

Setup:
1. Install dependencies:  uv pip install -U "agno[all]" ddgs psycopg[binary] pgvector pyyaml ollama
2. Ensure PostgreSQL with pgvector is running on localhost:5533
3. Install Ollama:      https://ollama.com/install
4. Pull the model:       ollama pull glm-5.1:cloud
5. Set environment variables:
   export OLLAMA_API_KEY=your_key_here
   export OPENAI_API_KEY=your_key_here
6. Run:                   python strategy_advisor_v2.py
   Or via AgentOS:       agno serve (auto-discovered from agents/ directory)
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

from tools.strategy_artifact_tools import StrategyArtifactTools

# ---------------------------------------------------------------------------
# Database — shared PostgreSQL instance.
# DATABASE_URL is injected by Railway; normalise scheme for SQLAlchemy/Agno.
# ---------------------------------------------------------------------------
_raw_db_url = os.environ.get(
    "DATABASE_URL", "postgresql+psycopg://edgeai:edgeai@localhost:5533/edgeai"
)
DB_URL = _raw_db_url.replace("postgresql://", "postgresql+psycopg://", 1)
agent_db = PostgresDb(db_url=DB_URL)

# ---------------------------------------------------------------------------
# Learning Knowledge — PgVector for entity memory & learned knowledge vectors
# Uses OpenAI embedder (consistent with platform standard)
# Separate table from the shared agno_docs knowledge base
# ---------------------------------------------------------------------------
learning_vector_db = PgVector(
    db_url=DB_URL,
    table_name="strategy_learning",
    embedder=OpenAIEmbedder(id="text-embedding-3-small"),
)

learning_knowledge = Knowledge(
    name="Strategy Learning",
    description=(
        "Learned strategic insights, entity knowledge about companies and competitors, "
        "and user preferences. This knowledge base grows over time as the agent learns "
        "from conversations."
    ),
    vector_db=learning_vector_db,
    contents_db=agent_db,  # Track metadata in same PostgresDb
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
    3. **Offer Multiple Options**: Present 2–3 strategic alternatives rather than a single
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
    3. **Save**: Once confirmed, call the save_artifact tool with a descriptive title,
       the appropriate artifact_type, and the full content.

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
    # --- Storage (shared PostgreSQL) ---
    db=agent_db,
    # --- Tools ---
    # cache_results=True on external/deterministic tools to avoid redundant API calls
    # and speed up repeated queries during a conversation
    tools=[
        ReasoningTools(add_instructions=True),   # Structured analysis — stateful, no cache
        DuckDuckGoTools(cache_results=True),     # Market research — cache avoids repeat API calls
        FileTools(
            base_dir=Path("artifacts/strategy"),
            cache_results=True,                  # File reads are deterministic — cache them
        ),
        StrategyArtifactTools(),                 # Stateful — save/list/read, no cache
    ],
    # --- Learning ---
    # Agentic memory: user preferences across sessions
    # Entity memory: companies, competitors, market entities (shared globally)
    # Learned knowledge: strategic insights transferable across users (propose mode
    #   so the user confirms before learning something new)
    learning=LearningMachine(
        entity_memory=EntityMemoryConfig(
            mode=LearningMode.AGENTIC,  # Agent actively manages entities
            namespace="global",  # Shared across all users
        ),
        learned_knowledge=LearnedKnowledgeConfig(
            knowledge=learning_knowledge,  # Vector DB for learned insights
            mode=LearningMode.PROPOSE,  # Agent proposes, user confirms
            namespace="global",  # Insights available to all users
        ),
    ),
    enable_agentic_memory=True,  # Agent manages user memories explicitly
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
    print("=" * 70)
    print("  Strategy Advisor Agent v2")
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