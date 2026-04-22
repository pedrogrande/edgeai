"""
Agno Agent Design Agent (v2 — Optimized Prompt)
=================================================
A meta-agent that helps users design well-structured Agno agents.
Always verifies API details from Agno docs. Always uses Ollama models.

v2 Changes (vs v1):
  - System prompt reduced from ~650 to ~220 tokens (66% cut)
  - Removed duplicated design process section (already in skills/SKILL.md)
  - Removed redundant skill reference pointers (auto-injected by skills system)
  - Compressed 6 prose principles → 5 linter-config rules
  - Merged "Be practical" into identity, "Be efficient" + Efficiency Rules into 2 terse rules
  - Moved "Explain in plain language" to implied skill-loading behavior
  - Approval tracking compressed to linter-config format
  - Positional structure: RULES (critical → boundary) → STATE → PROCESS

Retained from v1:
  - Skills (Progressive Disclosure): design-process, non-technical-explanations,
    architecture-context, design-template — loaded on demand, not inlined
  - Tool Result Caching: cache_results=True on deterministic/external tools
  - ReasoningTools (not PythonTools) for design-thinking
  - Session state tracks approval status (no redundant re-approval)
  - Context compression, tool call limit, controlled history

Setup:
  1. uv pip install agno ddgs ollama pymilvus
  2. export OLLAMA_API_KEY=your_key
  3. export ZILLIZ_CLOUD_HOST=your_host
  4. export ZILLIZ_CLOUD_TOKEN=your_token
  5. agno serve agent_designer.py:agent_designer
     OR
     python agent_designer.py
"""

from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.ollama import Ollama
from agno.skills import Skills, LocalSkills
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.file import FileTools
from agno.tools.local_file_system import LocalFileSystemTools
from agno.tools.reasoning import ReasoningTools
from tools.agent_spec_tools import AgentSpecTools
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.milvus import Milvus

# ─── Database ────────────────────────────────────────────────
agent_designer_db = SqliteDb(
    db_file=str(Path(__file__).parent.parent / "data" / "agent_designer_memories.db")
)

# ─── Knowledge Base (Agno docs) ──────────────────────────────
vector_db = Milvus(
    collection="agno_docs",
    uri=os.environ["ZILLIZ_CLOUD_HOST"],
    token=os.environ["ZILLIZ_CLOUD_TOKEN"],
)
knowledge_base = Knowledge(
    vector_db=vector_db,
)

# ─── Skills ───────────────────────────────────────────────────
# 4 skill groups loaded on demand (progressive disclosure):
#   design-process/       — 7-phase process with per-phase references
#   non-technical-explanations/ — analogies for non-technical users
#   architecture-context/ — current EdgeAI infrastructure reference
#   design-template/      — full 8-part agent design template
#
# Skill summaries are auto-injected into the system prompt (~200 tokens).
# Full content loads only when the agent calls get_skill_instructions/reference.
# This replaces inlining ~4KB of architecture docs + template into the prompt.
skills_dir = Path(__file__).parent.parent / "skills" / "agent-designer"

# ─── System Prompt (v2 — Optimized) ──────────────────────────
# Structure: RULES (critical → boundary) → APPROVAL STATE → PROCESS
# ~220 tokens, down from ~650 in v1.
# Substantive content lives in skill files, not here.
SYSTEM_PROMPT = """You design well-structured Agno agents — from idea to complete, runnable code.

## RULES (critical → boundary)

1. **NEVER GUESS THE API.** Unsure about a class, method, import, or parameter? Look it up (KB → search). Wrong imports > no imports.
2. **ALWAYS OLLAMA.** Default: `Ollama(id="glm-5.1:cloud")`. Exception: `OpenAIEmbedder` for embeddings, never Ollama.
3. **NO CODE WITHOUT APPROVAL.** User must approve the completed Agent Design Template before you generate code or persist specs. Hard gate.
4. **MINIMUM TOOLS.** Only add tools the use case requires. Prefer composition over complexity.
5. **KB FIRST, SEARCH SECOND.** Knowledge base → DuckDuckGo only if KB returns nothing. No redundant calls.

## APPROVAL STATE (avoids redundant asks)

Before requesting approval, check session state:
- `spec_approved[name] == True` AND `spec_changes_since_approval[name]` empty → already approved, proceed
- Approved but changes since → request approval only for those changes
- On approval → set `spec_approved[name] = True`, clear `spec_changes_since_approval[name]`
- After modifying an approved spec → append change to `spec_changes_since_approval[name]`

## PROCESS

Follow the 7-phase design process via your skills (design-process, design-template, non-technical-explanations, architecture-context). Load each phase's guidance when you reach it — not before.
"""

# ─── Agent ────────────────────────────────────────────────────
agent_designer = Agent(
    name="Agent Engineer",
    model=Ollama(id="glm-5.1:cloud"),
    description="Designs well-structured Agno agents. Always verifies API from docs. Always uses Ollama models except for embedding.",
    instructions=SYSTEM_PROMPT,
    # ─── Skills (Progressive Disclosure) ─────────────────────
    # Replaces ~4KB of inlined architecture docs + template.
    # Agent sees skill summaries in prompt (~200 tokens),
    # loads full content on demand via get_skill_instructions/reference.
    skills=Skills(loaders=[LocalSkills(str(skills_dir))]),
    # ─── Knowledge Base (Agno docs) ────────────────────────
    knowledge=knowledge_base,
    search_knowledge=True,
    # ─── Tools ───────────────────────────────────────────────
    tools=[
        AgentSpecTools(),  # Persist specs to Supabase (stateful — no cache)
        DuckDuckGoTools(
            cache_results=True
        ),  # Web search — cache to avoid repeated API calls
        FileTools(cache_results=True),  # Read/write files — cache read results
        LocalFileSystemTools(
            target_directory="./agents"
        ),  # Browse agents dir — fast local ops, no cache needed
        ReasoningTools(
            add_instructions=True
        ),  # Structured analysis — stateful, no cache
    ],
    db=agent_designer_db,
    # ─── Session State: Smart Approval Tracking ────────────────
    session_state={
        "design_phase": "discover",
        "current_spec_name": None,
        "spec_approved": {},  # {"spec-name": True/False}
        "spec_changes_since_approval": {},  # {"spec-name": ["changed model", ...]}
        "code_generated": {},  # {"spec-name": True/False}
    },
    add_session_state_to_context=True,
    enable_agentic_state=True,
    # ─── Memory: Cross-Session Awareness ──────────────────────
    update_memory_on_run=True,
    # ─── Context Compression ────────────────────────────────
    compress_tool_results=True,
    # ─── Tool Call Limit ─────────────────────────────────────
    tool_call_limit=15,
    # ─── History Management ──────────────────────────────────
    add_history_to_context=True,
    num_history_runs=3,
    max_tool_calls_from_history=3,
    # ─── Output ──────────────────────────────────────────────
    markdown=True,
)

# ─── Run ───────────────────────────────────────────────────────
if __name__ == "__main__":
    agent_designer.print_response(
        "I want to design an Agno agent. Help me get started!",
        stream=True,
    )
