"""
Business Strategy Advisor Agent
================================

A conversational agent that helps users develop business strategy through
collaborative dialogue. It saves strategic artifacts (frameworks, analyses,
templates) to a knowledge base for future retrieval.

Key Agno features used:
- ReasoningTools for deep analysis
- Agentic Memory (user context + preferences across sessions)
- Entity Memory (companies, competitors, market entities)
- Learned Knowledge (strategic insights that transfer across users)
- Knowledge Base with LanceDB (saved artifacts via custom tool)
- Agentic Session State (evolving strategy context within a conversation)
- DuckDuckGo search (market research)
- FileTools (read/write local strategy documents)
- HITL confirmation before saving artifacts

Setup:
1. Install dependencies:  uv pip install -U agno lancedb duckduckgo-search ollama
2. Install Ollama:       https://ollama.com/install
3. Pull the model:       ollama pull glm-5.1:cloud
4. Set API key:          export OLLAMA_API_KEY=your_key_here
5. Run:                   python strategy_advisor.py
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.text_reader import TextReader
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
from agno.vectordb.lancedb import LanceDb

# ---------------------------------------------------------------------------
# Storage — SQLite for sessions/memories, LanceDB for knowledge vectors
# ---------------------------------------------------------------------------
agent_db = SqliteDb(db_file="../data/strategy_advisor.db")

# ---------------------------------------------------------------------------
# Knowledge Base — stores strategy artifacts for semantic retrieval
# Uses LanceDB (local, no external DB needed) with Ollama embedder
# ---------------------------------------------------------------------------
artifacts_kb = Knowledge(
    name="Strategy Artifacts",
    description="Saved strategy documents, frameworks, analyses, and templates",
    vector_db=LanceDb(
        table_name="strategy_artifacts",
        uri="tmp/lancedb_strategy",
        embedder=OpenAIEmbedder(),  # Uses Ollama's embedding model locally
    ),
    max_results=5,
    contents_db=agent_db,  # Track metadata in same SQLite DB
)


# ---------------------------------------------------------------------------
# Custom Tool: Save Artifact
# ---------------------------------------------------------------------------
def save_artifact(title: str, artifact_type: str, content: str) -> str:
    """
    Save a strategy artifact to the knowledge base for future retrieval.
    Use this when the user explicitly confirms they want to save a strategic
    insight, framework, analysis, or template that emerged from the conversation.

    ALWAYS propose the artifact first and wait for user confirmation before calling this tool.

    Args:
        title: Short descriptive title (e.g., "SWOT Analysis: Acme Corp Q4 2025")
        artifact_type: One of: "strategy", "framework", "analysis", "template", "insight"
        content: The full content to save — be specific, structured, and actionable

    Returns:
        Confirmation message with the saved artifact title
    """
    if not title or not title.strip():
        return "Cannot save: title is required"
    if not content or not content.strip():
        return "Cannot save: artifact content is required"

    valid_types = ["strategy", "framework", "analysis", "template", "insight"]
    if artifact_type not in valid_types:
        return f"Cannot save: artifact_type must be one of {valid_types}"

    # Build the payload with metadata
    payload = {
        "title": title.strip(),
        "artifact_type": artifact_type,
        "content": content.strip(),
        "saved_at": datetime.now(timezone.utc).isoformat(),
    }

    # Save to knowledge base using TextReader for plain text content
    artifacts_kb.insert(
        name=payload["title"],
        text_content=json.dumps(payload, ensure_ascii=False),
        reader=TextReader(),
        skip_if_exists=True,
    )

    return f"✅ Saved artifact: '{title}' (type: {artifact_type})"


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
    # --- Storage ---
    db=agent_db,
    # --- Reasoning ---
    tools=[
        ReasoningTools(add_instructions=True),
        DuckDuckGoTools(),
        FileTools(base_dir=Path("tmp/strategy_files")),
        save_artifact,  # Custom tool for saving artifacts to knowledge base
    ],
    # --- Knowledge (artifact retrieval) ---
    knowledge=artifacts_kb,
    search_knowledge=True,  # Gives agent a search_knowledge_base() tool
    # --- Learning Machine ---
    # Agentic memory: user preferences across sessions
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
        knowledge=artifacts_kb,  # Learned knowledge uses same vector DB
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
# Run the Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Interactive conversation loop
    print("=" * 70)
    print("  Strategy Advisor Agent")
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
