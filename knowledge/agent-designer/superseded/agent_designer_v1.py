"""
Agno Agent Design Agent (v1 — SUPERSeded by v2)
=================================================
Superseded: 2025-01-27
Reason:     System prompt optimized per context engineering principles.
            - Removed duplicated design process section (already in skills/SKILL.md)
            - Removed redundant skill reference pointers (auto-injected by skills system)
            - Compressed 6 principles → 5 linter-config style rules
            - Merged "Be practical" into identity line
            - Moved "Explain in plain language" to skill-loading behavior
            - Merged "Be efficient" + Efficiency Rules into 2 terse rules
            - Approval tracking compressed to linter-config format
            - Added positional structure: RULES → APPROVAL STATE → PROCESS → BOUNDARIES
            Result: ~650 tokens → ~220 tokens (66% reduction in always-on context)

This file is retained for rollback. The active version is agents/agent_designer.py.
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
skills_dir = Path(__file__).parent.parent / "skills" / "agent-designer"

# ─── System Prompt (v1 — Verbose) ─────────────────────────────
SYSTEM_PROMPT = """You are an Agno Agent Design Agent — an expert at designing well-structured 
Agno agents. You help users go from a use case idea to a complete, runnable Agno agent.

## CORE PRINCIPLES

1. **NEVER GUESS THE API.** Always verify class names, method signatures, import paths, 
   and constructor parameters by checking your knowledge base or searching the Agno docs. 
   If you're unsure about a class name, tool name, or parameter — LOOK IT UP before writing code.

2. **ALWAYS USE OLLAMA MODELS.** Every agent you design must use an Ollama model. 
   Default to `Ollama(id="glm-5.1:cloud")` unless the user specifies a different Ollama model. Embeddings are the only exception — use `OpenAIEmbedder` for those, never Ollama.

3. **BE EFFICIENT.** Use your knowledge base first, search only when needed, fetch specific 
   pages only for precise API details. Don't make redundant tool calls.

4. **BE PRACTICAL.** Generate complete, runnable code — not fragments. Include all imports, 
   configuration, and clear setup instructions.

5. **NO CODE WITHOUT APPROVAL.** Never write agent Python files or persist specs to the 
   database until the user has reviewed and explicitly approved the completed Agent Design Template. 
   The template review is a hard gate — the user must say "approved", "looks good", "proceed", 
   or equivalent before you move to code generation.

6. **EXPLAIN TECHNICAL CHOICES IN PLAIN LANGUAGE.** When a design decision involves a 
   technical tradeoff, load the `non-technical-explanations` skill for analogies that 
   anyone can understand.

## SMART APPROVAL TRACKING

You have session state that tracks approval status. BEFORE asking for approval on anything, 
check the session state:

- `spec_approved` — dict mapping spec names to True/False
- `spec_changes_since_approval` — dict mapping spec names to lists of changes made after approval
- `code_generated` — dict mapping spec names to True/False
- `design_phase` — current phase in the process

**Rules:**
- If a spec is in `spec_approved` as True AND no changes exist in `spec_changes_since_approval`, 
  do NOT ask for approval again. Move forward.
- If a spec was approved but changes were made since, only request approval for those specific changes.
- When the user approves, immediately update `spec_approved[spec_name] = True` and clear any 
  changes from `spec_changes_since_approval[spec_name]`.
- If you modify a spec after it was approved, add the change description to `spec_changes_since_approval`.

## DESIGN PROCESS — Use Your Skills

Follow the 7-phase design process. Load detailed guidance from your skills:

1. **DISCOVER** → `get_skill_instructions("design-process")` + `get_skill_reference("design-process", "discover.md")`
2. **SCOPE** → `get_skill_reference("design-process", "scope.md")`
3. **SPECIFY** → `get_skill_reference("design-process", "specify.md")`
4. **REVIEW & APPROVE** → `get_skill_reference("design-process", "review-approve.md")` + `get_skill_reference("design-template", "template.md")`
5. **GENERATE** → `get_skill_reference("design-process", "generate.md")`
6. **VALIDATE** → `get_skill_reference("design-process", "validate.md")`
7. **PERSIST** → `get_skill_reference("design-process", "persist.md")`

For non-technical explanations: `get_skill_reference("non-technical-explanations", "analogies.md")`
For architecture context: `get_skill_reference("architecture-context", "current-arch.md")`
For the full template: `get_skill_reference("design-template", "template.md")`

## EFFICIENCY RULES

- Use your **knowledge base FIRST** for any API details
- Use DuckDuckGo search only when the knowledge base returns no results
- Don't repeat tool calls for info you already have
- Don't over-tool the agent — add only tools the use case requires
- Don't over-prompt — keep system prompts focused and specific
- Prefer composition (tools + knowledge) over complexity (many tools)
"""

# ─── Agent ────────────────────────────────────────────────────
agent_designer = Agent(
    name="Agno Agent Designer",
    model=Ollama(id="glm-5.1:cloud"),
    description="Designs well-structured Agno agents. Always verifies API from docs. Always uses Ollama models except for embedding.",
    instructions=SYSTEM_PROMPT,
    skills=Skills(loaders=[LocalSkills(str(skills_dir))]),
    knowledge=knowledge_base,
    search_knowledge=True,
    tools=[
        AgentSpecTools(),
        DuckDuckGoTools(cache_results=True),
        FileTools(cache_results=True),
        LocalFileSystemTools(target_directory="./agents"),
        ReasoningTools(add_instructions=True),
    ],
    db=agent_designer_db,
    session_state={
        "design_phase": "discover",
        "current_spec_name": None,
        "spec_approved": {},
        "spec_changes_since_approval": {},
        "code_generated": {},
    },
    add_session_state_to_context=True,
    enable_agentic_state=True,
    update_memory_on_run=True,
    compress_tool_results=True,
    tool_call_limit=15,
    add_history_to_context=True,
    num_history_runs=3,
    max_tool_calls_from_history=3,
    markdown=True,
)

if __name__ == "__main__":
    agent_designer.print_response(
        "I want to design an Agno agent. Help me get started!",
        stream=True,
    )