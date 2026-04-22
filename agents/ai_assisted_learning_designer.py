"""
AI Assisted Learning Designer Agent
====================================

A generative conversational agent that helps users explore, ideate, and
strategise about AI-assisted learning platform design. It produces and
iterates on design artifacts through collaborative dialogue, with human
approval required before saving any file.

Key Agno features used:
- PgVector knowledge base — queries indexed artifacts via search_knowledge
  (populated by a separate document manager agent from saved files)
- FileTools for reading/listing artifact files — cached for deterministic reads
- Custom save_artifact tool with HITL confirmation (requires_confirmation=True)
- Custom update_artifact tool with HITL confirmation
- ReasoningTools for deep analysis and improvement suggestions
- DuckDuckGoTools for research when improving artifacts — cached
- Agentic Memory (user context, preferences, working style across sessions)
- Entity Memory (projects, artifact conventions)
- Agentic Session State (evolving artifact context within a conversation)

Cognitive mode: GENERATOR
This agent is not a passive aggregator — it actively proposes ideas,
connects concepts across domains, and structures thinking into actionable
artifacts. Everything it produces is a draft that the user verifies and
approves. The human is always the final decision-maker.

Artifact types supported:
- ideation           — Brainstorming outputs, idea lists, creative exploration
- strategy           — Strategic analyses, frameworks, competitive assessments
- use_case           — Use case explorations, user stories, scenario descriptions
- workflow           — Workflow specifications, process definitions, step sequences
- workflow_diagram   — Visual workflow representations (Mermaid or text diagrams)
- agent_spec         — Agent design specifications, capability definitions
- other              — Unclassified or novel artifact types not yet formalized

Storage structure:
    artifacts/ai-assisted-learning/
    ├── ideation/
    ├── strategy/
    ├── use_cases/
    ├── workflows/
    ├── workflow_diagrams/
    ├── agent_specs/
    └── other/              ← catch-all for artifact types not yet formalized

Each file uses YAML front matter:
    ---
    title: "Document Title"
    description: "One-line summary of what this artifact contains"
    artifact_type: ideation|strategy|use_case|workflow|workflow_diagram|agent_spec|other
    created: 2025-01-15T10:00:00Z
    updated: 2025-01-15T10:00:00Z
    status: draft|in_review|approved
    project: "Project Name"
    tags: []
    version: 1
    ---

Setup:
1. Install dependencies:  uv pip install -U agno duckduckgo-search ollama openai pyyaml
2. Install Ollama:        https://ollama.com/install
3. Pull the model:        ollama pull glm-5.1:cloud
4. Set API keys:          export OLLAMA_API_KEY=your_key_here
                           export OPENAI_API_KEY=your_key_here  (for embedder)
5. Create artifact dirs:  mkdir -p artifacts/ai-assisted-learning/{ideation,strategy,use_cases,workflows,workflow_diagrams,agent_specs,other}
6. Create data dir:       mkdir -p data
7. Run:                   python ai_assisted_learning_designer.py

Knowledge base note:
This agent queries a PgVector knowledge base (table: ai_learning_artifacts)
for indexed artifact content. The document manager agent handles the
file→vector pipeline — you do NOT need to load files into the vector DB
manually. When this agent saves an artifact, the document manager will
index it automatically.
"""

import os
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent

import yaml
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.learn import (
    EntityMemoryConfig,
    LearningMachine,
    LearningMode,
)
from agno.models.ollama import Ollama
from agno.tools import tool
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.file import FileTools
from agno.tools.reasoning import ReasoningTools
from agno.vectordb.pgvector import PgVector

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
ARTIFACT_BASE_DIR = Path(
    os.environ.get("ARTIFACT_BASE_DIR", "artifacts/ai-assisted-learning")
)
ARTIFACT_TYPES = [
    "ideation",
    "strategy",
    "use_case",
    "workflow",
    "workflow_diagram",
    "agent_spec",
    "other",  # catch-all for artifact types not yet formalized
]
TYPE_TO_DIR = {
    "ideation": "ideation",
    "strategy": "strategy",
    "use_case": "use_cases",
    "workflow": "workflows",
    "workflow_diagram": "workflow_diagrams",
    "agent_spec": "agent_specs",
    "other": "other",
}
VALID_STATUSES = ["draft", "in_review", "approved"]

# Ensure artifact directories exist
for dir_name in TYPE_TO_DIR.values():
    (ARTIFACT_BASE_DIR / dir_name).mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Storage — SQLite for sessions/memories, PgVector for knowledge
# ---------------------------------------------------------------------------
agent_db = SqliteDb(db_file="data/ai_assisted_learning_designer.db")

# PgVector knowledge base — populated by the document manager agent
# This agent queries it via search_knowledge; it does NOT load files itself
_pgvector_db_url = os.environ.get(
    "PGVECTOR_DB_URL",
    "postgresql+psycopg://edgeai:edgeai@localhost:5533/edgeai",
)
vector_db = PgVector(
    db_url=_pgvector_db_url,
    table_name="ai_learning_artifacts",
    embedder=OpenAIEmbedder(id="text-embedding-3-small"),
)
knowledge = Knowledge(
    name="AI Assisted Learning Artifacts",
    vector_db=vector_db,
)


# ---------------------------------------------------------------------------
# Helper: Build front matter + markdown content
# ---------------------------------------------------------------------------
def _build_artifact_content(
    title: str,
    artifact_type: str,
    content: str,
    description: str = "",
    project: str = "",
    tags: list[str] | None = None,
    status: str = "draft",
    version: int = 1,
    created: str | None = None,
    updated: str | None = None,
) -> str:
    """Build a complete markdown string with YAML front matter and content body."""
    now = datetime.now(timezone.utc).isoformat()
    created = created or now
    updated = updated or now

    front_matter = {
        "title": title.strip(),
        "description": description.strip() if description else "",
        "artifact_type": artifact_type,
        "created": created,
        "updated": updated,
        "status": status,
        "project": project.strip() if project else "",
        "tags": tags or [],
        "version": version,
    }

    return f"---\n{yaml.dump(front_matter, default_flow_style=False, sort_keys=False)}---\n\n{content.strip()}\n"


# ---------------------------------------------------------------------------
# Custom Tools
# ---------------------------------------------------------------------------

@tool(requires_confirmation=True)
def save_artifact(
    title: str,
    artifact_type: str,
    content: str,
    description: str = "",
    project: str = "",
    tags: str = "",
    status: str = "draft",
) -> str:
    """
    Save a new design artifact as a markdown file with YAML front matter.
    The user will be asked to confirm before the file is written.

    Args:
        title: Short descriptive title (e.g., "Ideation: AI Learning Platform Features")
        artifact_type: One of: ideation, strategy, use_case, workflow, workflow_diagram, agent_spec, other
        content: The full markdown body of the artifact (after front matter)
        description: One-line summary of what this artifact contains
        project: Optional project name for grouping artifacts
        tags: Comma-separated tags for categorization (e.g., "ai,learning,platform")
        status: One of: draft, in_review, approved (default: draft)

    Returns:
        Confirmation message with the file path
    """
    # Validate artifact_type
    artifact_type = artifact_type.strip().lower()
    if artifact_type not in ARTIFACT_TYPES:
        return f"Error: artifact_type must be one of {ARTIFACT_TYPES}. Got: '{artifact_type}'"

    # Validate status
    status = status.strip().lower()
    if status not in VALID_STATUSES:
        return f"Error: status must be one of {VALID_STATUSES}. Got: '{status}'"

    if not title or not title.strip():
        return "Error: title is required"
    if not content or not content.strip():
        return "Error: artifact content is required"

    # Parse tags
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []

    # Build full content with front matter
    full_content = _build_artifact_content(
        title=title.strip(),
        artifact_type=artifact_type,
        content=content.strip(),
        description=description.strip() if description else "",
        project=project.strip() if project else "",
        tags=tag_list,
        status=status,
    )

    # Generate safe filename
    safe_title = title.strip().lower().replace(" ", "_")[:60]
    # Remove characters unsafe for filenames
    safe_chars = []
    for ch in safe_title:
        if ch.isalnum() or ch in ("_", "-"):
            safe_chars.append(ch)
        else:
            safe_chars.append("_")
    safe_name = "".join(safe_chars).rstrip("_")
    filename = f"{safe_name}.md"

    # Determine output directory
    dir_name = TYPE_TO_DIR[artifact_type]
    output_dir = ARTIFACT_BASE_DIR / dir_name
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / filename

    # Write the file
    file_path.write_text(full_content, encoding="utf-8")

    return (
        f"✅ Saved artifact: '{title}' → {file_path} "
        f"(type: {artifact_type}, status: {status})"
    )


@tool(requires_confirmation=True)
def update_artifact(
    file_path: str,
    content: str = "",
    title: str = "",
    description: str = "",
    status: str = "",
    tags: str = "",
    project: str = "",
) -> str:
    """
    Update an existing artifact file. The user will be asked to confirm before
    the file is overwritten.

    Provide the relative file path (e.g., "ideation/my_idea.md") and at least
    one field to update. Fields left empty will keep their current values.

    Args:
        file_path: Relative path from artifacts/ai-assisted-learning/ directory
                   (e.g., "ideation/my_idea.md")
        content: New markdown body content (leave empty to keep existing)
        title: New title (leave empty to keep existing)
        description: New one-line description (leave empty to keep existing)
        status: New status: draft, in_review, approved (leave empty to keep existing)
        tags: New comma-separated tags (leave empty to keep existing)
        project: New project name (leave empty to keep existing)

    Returns:
        Confirmation message with the updated file path
    """
    # Resolve file path
    full_path = ARTIFACT_BASE_DIR / file_path
    if not full_path.exists():
        return f"Error: File not found: {file_path}"

    # Read existing file and parse front matter
    raw = full_path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        return f"Error: File does not have YAML front matter: {file_path}"

    # Split front matter and content
    parts = raw.split("---", 2)
    if len(parts) < 3:
        return f"Error: Could not parse front matter in: {file_path}"

    existing_meta = yaml.safe_load(parts[1]) or {}
    existing_content = parts[2].strip()

    # Apply updates
    new_title = title.strip() if title else existing_meta.get("title", "")
    new_description = (
        description.strip() if description else existing_meta.get("description", "")
    )
    new_status = (
        status.strip().lower() if status else existing_meta.get("status", "draft")
    )
    new_project = (
        project.strip() if project else existing_meta.get("project", "")
    )
    new_tags = (
        [t.strip() for t in tags.split(",") if t.strip()]
        if tags
        else existing_meta.get("tags", [])
    )
    new_content = content.strip() if content else existing_content
    new_version = existing_meta.get("version", 1) + 1
    created = existing_meta.get("created", datetime.now(timezone.utc).isoformat())

    if new_status and new_status not in VALID_STATUSES:
        return f"Error: status must be one of {VALID_STATUSES}. Got: '{new_status}'"

    # Rebuild file
    full_new = _build_artifact_content(
        title=new_title,
        artifact_type=existing_meta.get("artifact_type", "ideation"),
        content=new_content,
        description=new_description,
        project=new_project,
        tags=new_tags,
        status=new_status,
        version=new_version,
        created=created,
    )

    full_path.write_text(full_new, encoding="utf-8")

    return (
        f"✅ Updated artifact: '{new_title}' → {full_path} "
        f"(v{new_version}, status: {new_status})"
    )


def list_artifacts(artifact_type: str = "", project: str = "") -> str:
    """
    List all artifacts, optionally filtered by type and/or project.
    Returns a formatted list of artifact metadata.

    Args:
        artifact_type: Filter by type: ideation, strategy, use_case, workflow,
                       workflow_diagram, agent_spec, other
        project: Filter by project name

    Returns:
        Formatted list of artifacts with metadata
    """
    results = []
    dirs_to_search = []

    if artifact_type:
        artifact_type = artifact_type.strip().lower()
        if artifact_type not in ARTIFACT_TYPES:
            return (
                f"Error: artifact_type must be one of {ARTIFACT_TYPES}. "
                f"Got: '{artifact_type}'"
            )
        dirs_to_search = [TYPE_TO_DIR[artifact_type]]
    else:
        dirs_to_search = list(TYPE_TO_DIR.values())

    project_filter = project.strip().lower() if project else ""

    for dir_name in dirs_to_search:
        dir_path = ARTIFACT_BASE_DIR / dir_name
        if not dir_path.exists():
            continue
        for md_file in sorted(dir_path.glob("*.md")):
            raw = md_file.read_text(encoding="utf-8")
            if not raw.startswith("---"):
                continue
            parts = raw.split("---", 2)
            if len(parts) < 3:
                continue
            meta = yaml.safe_load(parts[1]) or {}

            # Apply project filter
            if project_filter and meta.get("project", "").lower() != project_filter:
                continue

            desc = meta.get("description", "")
            desc_display = f" — {desc}" if desc else ""
            results.append(
                f"- [{meta.get('status', '?')}] {meta.get('title', md_file.stem)}"
                f" ({meta.get('artifact_type', '?')}, v{meta.get('version', '?')},"
                f" project: {meta.get('project', '—')}){desc_display}"
                f" → {dir_name}/{md_file.name}"
            )

    if not results:
        not_found_msg = "No artifacts found"
        if artifact_type:
            not_found_msg += f" of type '{artifact_type}'"
        if project_filter:
            not_found_msg += f" in project '{project}'"
        return not_found_msg

    header = f"Found {len(results)} artifact(s):"
    return header + "\n" + "\n".join(results)


# ---------------------------------------------------------------------------
# Agent Instructions
# ---------------------------------------------------------------------------
SYSTEM_INSTRUCTIONS = dedent(
    """\
    You are an AI Assisted Learning Designer — a creative, generative thinking
    partner who helps users explore, ideate, and strategise about AI-assisted
    learning systems. You produce design artifacts through collaborative
    dialogue. You actively propose ideas, connect concepts across domains, and
    structure thinking into actionable artifacts.

    ## Your Role

    You are NOT a passive document factory. You are a generative exploration
    partner who:
    - Helps users think through what they want to capture
    - Actively proposes new angles, connections, and possibilities
    - Suggests structure, improvements, and relationships between artifacts
    - Proposes artifact contents and waits for approval before saving
    - Maintains context across sessions about the user's projects and preferences

    ## What Makes You a Generator, Not an Aggregator

    An aggregator combines existing inputs without adding beyond them. You do
    more than that — you:
    - Ideate: propose new ideas the user hasn't considered yet
    - Connect: spot relationships between concepts across different artifacts
    - Structure: organise raw thinking into coherent frameworks
    - Challenge: offer alternative perspectives and push back gently
    - Enrich: suggest improvements that go beyond what the user articulated

    Every suggestion you make is a DRAFT. The user verifies and decides. You
    never present speculation as confirmed fact. You surface assumptions
    explicitly.

    ## Artifact Types You Manage

    | Type | Description | Typical Contents |
    |------|-------------|-----------------|
    | ideation | Brainstorming outputs, idea lists | Ideas, possibilities, "what if" scenarios |
    | strategy | Strategic analyses, frameworks | SWOT, competitive analysis, market positioning |
    | use_case | Use case explorations | User stories, scenarios, persona-based needs |
    | workflow | Workflow specifications | Step sequences, process definitions, logic flows |
    | workflow_diagram | Visual workflow representations | Mermaid diagrams, sequence diagrams, flowcharts |
    | agent_spec | Agent design specifications | Purpose, capabilities, tools, guardrails |
    | other | Unclassified or novel types | Anything that doesn't fit the categories above |

    The "other" category exists for artifact types you haven't yet formalised.
    If a pattern emerges (e.g., three "other" artifacts are all persona
    documents), suggest creating a new dedicated type for them.

    ## Your Approach

    1. **Explore First**: Understand the user's context and what they're trying to
       capture before structuring anything. Ask clarifying questions.
    2. **Draft Collaboratively**: Build artifact content iteratively. Present drafts
       for review rather than final documents.
    3. **Generate Ideas**: Don't just reflect the user's input — actively propose
       new angles, missing considerations, and creative alternatives.
    4. **Suggest Improvements**: Propose enhancements:
       - Missing sections or considerations
       - Better structure or organisation
       - Connections to other artifacts
       - Alternative perspectives or approaches
    5. **Connect Artifacts**: Point out relationships between artifacts
       ("This use case connects to the workflow you defined last session").
    6. **Respect the User's Voice**: Your role is to enhance, not replace. The user's
       ideas, wording, and priorities take precedence over your suggestions.

    ## Knowledge Base

    You have access to a vector knowledge base of previously saved artifacts.
    Use search_knowledge to find relevant context when:
    - The user references something from a previous conversation
    - You want to connect the current discussion to existing artifacts
    - You need to check what's already been explored to avoid duplication

    The knowledge base is populated by a separate document manager that indexes
    saved artifact files. If you can't find something in the knowledge base, it
    may not have been indexed yet — use list_artifacts to check the file system
    directly.

    ## Saving Artifacts — ALWAYS Follow This Process

    1. **Draft**: Present the full artifact content in conversation first
    2. **Review**: Ask "Does this capture what you want? Any changes before I save?"
    3. **Save**: Only call save_artifact after the user explicitly approves

    The save_artifact tool requires your confirmation before writing. The framework
    will ask you to confirm — this is a safety gate, not a suggestion.

    ## Updating Artifacts — Same Process

    1. **Show Changes**: Present what you plan to change and why
    2. **Confirm**: Wait for user approval
    3. **Update**: Call update_artifact with the specific fields to change

    ## Front Matter — Always Include Description

    Every artifact must have a `description` field in its front matter — a
    one-line summary of what the artifact contains. This makes search, triage,
    and knowledge base indexing much more effective.

    ## Improvement Suggestions

    When you suggest improvements, be specific about:
    - WHAT you're suggesting (exact content or structural change)
    - WHY it would improve the artifact (reasoning, best practices)
    - ALTERNATIVES you considered and why this suggestion is preferred

    Never make vague suggestions like "consider adding more detail." Instead:
    "Consider adding a 'Risks & Mitigations' section because every strategy
    artifact benefits from explicitly surfacing what could go wrong."

    ## Guardrails

    - Never save an artifact without user approval — this is non-negotiable
    - Clearly distinguish your suggestions from the user's original content
    - If you're unsure about something, say so rather than guessing
    - Never present speculative content as factual
    - When working with agent specs, preserve technical precision — don't
      oversimplify model names, tool paths, or configuration details
    - Keep front matter accurate — status, version, and timestamps are metadata,
      not decoration
    - All artifacts are saved under artifacts/ai-assisted-learning/
"""
)

# ---------------------------------------------------------------------------
# Create the Agent
# ---------------------------------------------------------------------------
ai_assisted_learning_designer = Agent(
    name="AI Assisted Learning Designer",
    model=Ollama(id="glm-5.1:cloud"),
    instructions=SYSTEM_INSTRUCTIONS,
    # --- Storage ---
    db=agent_db,
    # --- Knowledge ---
    # PgVector knowledge base — queries indexed artifacts (populated by document manager)
    knowledge=knowledge,
    search_knowledge=True,
    # --- Tools ---
    # cache_results=True on deterministic/external tools to avoid redundant API calls
    tools=[
        # File browsing: read, list, search existing artifact files — deterministic, cache
        FileTools(base_dir=ARTIFACT_BASE_DIR, cache_results=True),
        # Deep analysis and improvement suggestions — stateful, no cache
        ReasoningTools(add_instructions=True),
        # Research for informed improvements — external API, cache
        DuckDuckGoTools(cache_results=True),
        # Custom artifact management tools — stateful (write files), no cache
        save_artifact,       # HITL-gated: requires user confirmation
        update_artifact,     # HITL-gated: requires user confirmation
        list_artifacts,      # Browse existing artifacts by type/project — fast local, no cache
    ],
    # --- Agentic Memory ---
    # Remembers user preferences, working style, project context across sessions
    learning=LearningMachine(
        entity_memory=EntityMemoryConfig(
            mode=LearningMode.AGENTIC,    # Agent actively manages entities
            namespace="global",            # Shared project knowledge
        ),
    ),
    enable_agentic_memory=True,  # User preferences across sessions
    update_memory_on_run=True,
    # --- Session State ---
    # Tracks evolving artifact context within a conversation
    session_state={
        "current_project": None,
        "current_artifact_types": [],
        "draft_artifacts": [],            # Artifacts being developed this session
        "recently_viewed": [],            # Artifact references read this session
        "improvements_proposed": [],      # Pending improvement suggestions
        "exploration_threads": [],        # Open ideation/exploration threads
    },
    add_session_state_to_context=True,
    enable_agentic_state=True,     # Agent can update state based on context
    # --- Context settings ---
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=15,  # Remember last 15 exchanges for continuity
    # --- Output ---
    markdown=True,
)

# ---------------------------------------------------------------------------
# Run the Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 70)
    print("  AI Assisted Learning Designer")
    print("  Type your design questions, or 'exit' to quit.")
    print("=" * 70)

    while True:
        user_input = input("\n🧑 You: ").strip()
        if user_input.lower() in ("exit", "quit", "bye"):
            print(
                "Goodbye! Your artifacts are saved in "
                "artifacts/ai-assisted-learning/."
            )
            break

        if not user_input:
            continue

        ai_assisted_learning_designer.print_response(user_input, stream=True)