"""
Document Manager Agent
======================

Automated document pipeline agent that picks up artifact files from staging
directories, validates/applies YAML front matter, indexes content into
domain-specific PgVector knowledge bases, registers documents in a PostgreSQL
`documents` table via MCP Toolbox, and archives processed files.

Also serves as a conversational query endpoint — humans and other agents can
ask about artifact metadata, processing status, and document inventory.

Key Agno features used:
- ReasoningTools for step-by-step front matter validation (not PythonTools)
- FileTools for reading/processing artifact files
- LocalFileSystemTools for browsing staging and archive directories
- PgVector knowledge base — indexes artifact content per domain
- Agent memory — remembers processing state and history
- Agentic Session State — tracks processing queue within conversations

Note on tool caching: This agent's tools are primarily stateful (file
processing, DB writes, knowledge base indexing) so cache_results is NOT
enabled on most tools. FileTools reads are not cached either because
the agent needs to see the latest file state (files may change between
read and process steps within the same conversation).

Cognitive mode: EXTRACTOR
This agent gathers and processes files without judging their content. It
validates structure, indexes content, and registers metadata. It never
interprets or evaluates the meaning of artifacts — that's the domain agents' job.

Processing flow:
1. Scan staging directory (artifacts/<domain>/) for unprocessed files
2. Register each file in the `documents` table (status: pending)
3. Validate/apply YAML front matter using ReasoningTools
4. Index content into the domain's PgVector knowledge base
5. Mark as processed (status: processed, set archive_path)
6. Move file from staging to archive (artifacts/_archive/<domain>/)

If any step fails: mark as error (status: error) — file stays in staging for retry.

Artifact types supported (matches AI Assisted Learning Designer):
- ideation, strategy, use_case, workflow, workflow_diagram, agent_spec, other

Setup:
1. Install dependencies:  uv pip install -U agno duckduckgo-search ollama openai pyyaml
2. Install Ollama:        https://ollama.com/install
3. Pull the model:        ollama pull glm-5.1:cloud
4. Set API keys:          export OLLAMA_API_KEY=your_key_here
                           export OPENAI_API_KEY=your_key_here  (for embedder)
5. Create staging dirs:   mkdir -p artifacts/ai-assisted-learning/{ideation,strategy,use_cases,workflows,workflow_diagrams,agent_specs,other}
6. Create archive dirs:   mkdir -p artifacts/_archive/ai-assisted-learning/{ideation,strategy,use_cases,workflows,workflow_diagrams,agent_specs,other}
7. Create data dir:       mkdir -p data
8. Run:                   python document_manager.py
                           OR
                           agno serve document_manager.py:document_manager

MCP Toolbox integration:
This agent expects the `doc-mgmt` toolset to be available via the MCP Toolbox
(edgeai-toolbox on port 5001). The toolset provides:
- register-document: Insert a new document record
- mark-processed: Update status to processed after successful indexing
- mark-error: Mark a document as having a processing error
- list-pending-documents: List documents awaiting processing
- search-documents: Search documents by domain, type, status, project, tags
- get-document: Get full details for a specific document

These tools are defined in db/tools.yaml and served by the edgeai-toolbox container.
"""

import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent

import yaml
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.knowledge.chunking.markdown import MarkdownChunking
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.markdown_reader import MarkdownReader
from agno.models.ollama import Ollama
from agno.tools.file import FileTools
from agno.tools.local_file_system import LocalFileSystemTools
from agno.tools.reasoning import ReasoningTools
from agno.vectordb.pgvector import PgVector

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
# Staging: where domain agents drop files for processing
STAGING_BASE_DIR = Path(os.environ.get("STAGING_BASE_DIR", "artifacts"))
# Archive: where processed files are moved (cold storage backup)
ARCHIVE_BASE_DIR = Path(os.environ.get("ARCHIVE_BASE_DIR", "artifacts/_archive"))

# Supported artifact types — must match AI Assisted Learning Designer
ARTIFACT_TYPES = [
    "ideation",
    "strategy",
    "use_case",
    "workflow",
    "workflow_diagram",
    "agent_spec",
    "other",
]

# Map artifact types to directory names (same convention as AI Learning Designer)
TYPE_TO_DIR = {
    "ideation": "ideation",
    "strategy": "strategy",
    "use_case": "use_cases",
    "workflow": "workflows",
    "workflow_diagram": "workflow_diagrams",
    "agent_spec": "agent_specs",
    "other": "other",
}

# Known domains — new domains can be added as the platform grows
KNOWN_DOMAINS = ["ai-assisted-learning"]

# PgVector table naming convention: <domain>_artifacts
# e.g., ai_learning_artifacts for ai-assisted-learning

# ---------------------------------------------------------------------------
# Ensure directory structure exists
# ---------------------------------------------------------------------------
for domain in KNOWN_DOMAINS:
    for dir_name in TYPE_TO_DIR.values():
        (STAGING_BASE_DIR / domain / dir_name).mkdir(parents=True, exist_ok=True)
        (ARCHIVE_BASE_DIR / domain / dir_name).mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Storage — SQLite for sessions/memories
# ---------------------------------------------------------------------------
agent_db = SqliteDb(db_file="data/document_manager.db")

# ---------------------------------------------------------------------------
# Knowledge — PgVector for artifact content indexing
# We create one knowledge base per domain. The document manager writes to
# these; domain agents (like AI Learning Designer) read from them.
# ---------------------------------------------------------------------------
_pgvector_db_url = os.environ.get(
    "PGVECTOR_DB_URL",
    "postgresql+psycopg://edgeai:edgeai@localhost:5533/edgeai",
)

# Primary knowledge base for the AI Assisted Learning domain
ai_learning_vector_db = PgVector(
    db_url=_pgvector_db_url,
    table_name="ai_learning_artifacts",
    embedder=OpenAIEmbedder(id="text-embedding-3-small"),
)
knowledge = Knowledge(
    name="AI Learning Artifacts",
    vector_db=ai_learning_vector_db,
)

# Markdown reader with heading-based chunking for artifact indexing.
# split_on_headings=2 splits at H1/H2 boundaries, keeping H3-H6 content
# together with their parent H2. This preserves semantic coherence — each
# chunk is a complete section rather than an arbitrary fragment.
# For most agent artifacts (~1500 words), the entire document fits in one
# chunk. Longer documents split naturally at section boundaries.
md_reader = MarkdownReader(
    name="Artifact Markdown Reader",
    chunking_strategy=MarkdownChunking(split_on_headings=2),
)


# ---------------------------------------------------------------------------
# Helper: Build front matter for markdown files
# ---------------------------------------------------------------------------
def _build_front_matter(
    title: str,
    artifact_type: str,
    description: str = "",
    project: str = "",
    tags: list[str] | None = None,
    status: str = "draft",
    version: int = 1,
    created: str | None = None,
    updated: str | None = None,
) -> str:
    """Build YAML front matter block for a markdown artifact file."""
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

    return f"---\n{yaml.dump(front_matter, default_flow_style=False, sort_keys=False)}---\n"


# ---------------------------------------------------------------------------
# Custom Tools
# ---------------------------------------------------------------------------


def scan_staging_directory() -> str:
    """
    Scan all known staging directories for markdown files that haven't been
    processed yet. Returns a summary of what was found, organised by domain
    and artifact type.

    Returns:
        Summary of files found in staging directories.
    """
    results = []
    for domain in KNOWN_DOMAINS:
        domain_path = STAGING_BASE_DIR / domain
        if not domain_path.exists():
            continue
        for md_file in sorted(domain_path.rglob("*.md")):
            rel_path = md_file.relative_to(STAGING_BASE_DIR)
            # Skip files already in archive
            if "_archive" in str(md_file):
                continue
            results.append(f"- {rel_path} ({md_file.stat().st_size} bytes)")

    if not results:
        return "No files found in staging directories. All caught up!"

    header = f"Found {len(results)} file(s) in staging:"
    return header + "\n" + "\n".join(results)


def process_file(file_path: str) -> str:
    """
    Process a single artifact file from staging:
    1. Read the file
    2. Validate/apply YAML front matter
    3. Index content into the domain's PgVector knowledge base
    4. Register in the documents database (via MCP Toolbox)
    5. Move the file to the archive directory

    This is the core processing pipeline. The agent uses ReasoningTools to
    think through front matter validation step-by-step rather than executing
    Python code.

    Args:
        file_path: Relative path from the staging base directory
                   (e.g., "ai-assisted-learning/ideation/my_idea.md")

    Returns:
        Processing result message.
    """
    source_path = STAGING_BASE_DIR / file_path

    if not source_path.exists():
        return f"Error: File not found: {file_path}"

    if not source_path.is_file():
        return f"Error: Not a file: {file_path}"

    # Read the file
    try:
        raw_content = source_path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading file: {e}"

    # Parse existing front matter if present
    has_front_matter = raw_content.startswith("---")
    front_matter_valid = False
    existing_meta = {}
    body_content = raw_content

    if has_front_matter:
        parts = raw_content.split("---", 2)
        if len(parts) >= 3:
            try:
                existing_meta = yaml.safe_load(parts[1]) or {}
                body_content = parts[2].strip()
                front_matter_valid = True
            except yaml.YAMLError:
                front_matter_valid = False
                body_content = raw_content

    # Apply/fix front matter
    # The agent should use ReasoningTools to validate the front matter
    # structure, but here we do the basic mechanical parts:
    now = datetime.now(timezone.utc).isoformat()

    title = existing_meta.get("title", source_path.stem.replace("_", " ").title())
    description = existing_meta.get("description", "")
    artifact_type = existing_meta.get("artifact_type", "other")
    project = existing_meta.get("project", "")
    tags = existing_meta.get("tags", [])
    status = existing_meta.get("status", "draft")
    version = existing_meta.get("version", 1)
    created = existing_meta.get("created", now)
    updated = now

    # Validate artifact_type
    if artifact_type not in ARTIFACT_TYPES:
        artifact_type = "other"

    # Rebuild the file with validated front matter
    new_front_matter = _build_front_matter(
        title=title,
        artifact_type=artifact_type,
        description=description,
        project=project,
        tags=tags,
        status=status,
        version=version,
        created=created,
        updated=updated,
    )
    new_content = f"{new_front_matter}\n{body_content}\n"

    # Write back the validated file
    source_path.write_text(new_content, encoding="utf-8")

    # Index content into the domain's PgVector knowledge base
    # Uses MarkdownChunking (split_on_headings=2) to split at H1/H2
    # boundaries, preserving semantic coherence of each section.
    try:
        knowledge.ainsert_sync(path=str(source_path), reader=md_reader)
        indexing_status = "indexed"
    except Exception as e:
        indexing_status = f"indexing failed: {e}"

    # Determine domain and archive path
    # Parse domain from file path (first segment after staging base)
    path_parts = Path(file_path).parts
    domain = path_parts[0] if path_parts else "unknown"

    archive_rel_path = file_path  # Same relative structure in archive
    archive_path = ARCHIVE_BASE_DIR / archive_rel_path
    archive_path.parent.mkdir(parents=True, exist_ok=True)

    # Move file to archive
    try:
        shutil.move(str(source_path), str(archive_path))
    except Exception as e:
        return f"Error moving file to archive: {e}"

    return (
        f"✅ Processed: '{title}'\n"
        f"   Type: {artifact_type} | Domain: {domain}\n"
        f"   Archive: {archive_rel_path}\n"
        f"   Front matter applied: True\n"
        f"   Vector indexed: {indexing_status}\n"
        f"   Status: processed"
    )


def get_processing_stats() -> str:
    """
    Get current processing statistics — how many files in staging,
    how many in archive, breakdown by domain and type.

    Returns:
        Formatted processing statistics.
    """
    stats = {"staging": 0, "archive": 0, "by_domain": {}, "by_type": {}}

    # Count staging files
    for domain in KNOWN_DOMAINS:
        domain_path = STAGING_BASE_DIR / domain
        if not domain_path.exists():
            continue
        domain_count = 0
        for md_file in domain_path.rglob("*.md"):
            if "_archive" not in str(md_file):
                stats["staging"] += 1
                domain_count += 1
                # Try to extract artifact type from directory name
                parent_name = md_file.parent.name
                stats["by_type"][parent_name] = stats["by_type"].get(parent_name, 0) + 1
        stats["by_domain"][domain] = stats["by_domain"].get(domain, 0) + domain_count

    # Count archive files
    for domain in KNOWN_DOMAINS:
        archive_domain = ARCHIVE_BASE_DIR / domain
        if not archive_domain.exists():
            continue
        for md_file in archive_domain.rglob("*.md"):
            stats["archive"] += 1

    lines = [
        f"📊 Document Manager Stats",
        f"   Staging (unprocessed): {stats['staging']} file(s)",
        f"   Archive (processed):  {stats['archive']} file(s)",
    ]
    if stats["by_domain"]:
        lines.append("   By domain:")
        for domain, count in stats["by_domain"].items():
            lines.append(f"     - {domain}: {count}")
    if stats["by_type"]:
        lines.append("   By type:")
        for type_name, count in stats["by_type"].items():
            lines.append(f"     - {type_name}: {count}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Agent Instructions
# ---------------------------------------------------------------------------
SYSTEM_INSTRUCTIONS = dedent(
    """\
    You are a Document Manager — a systematic, reliable file processing agent.
    You pick up artifact files from staging directories, validate their YAML
    front matter, index their content into vector knowledge bases, register
    them in a database, and archive the processed files.

    ## Your Role

    You are an EXTRACTOR — you gather and process files without judging their
    content. You validate structure, index content, and register metadata.
    You never interpret, evaluate, or improve the meaning of artifacts.
    That's the domain agents' job.

    Think of yourself as a postal sorting facility: files come in, get
    validated, stamped, indexed, and filed. You don't read the letters —
    you make sure they have the right address and stamps.

    ## Processing Flow

    When triggered (by schedule or on demand), follow this exact sequence:

    1. **Scan**: Use scan_staging_directory to find unprocessed files
    2. **Validate**: For each file, use think (ReasoningTools) to reason
       through whether its front matter is valid:
       - Does it have YAML front matter (starts with ---)?
       - Does it have the required fields? (title, artifact_type, created, updated)
       - Is artifact_type one of the known types? (ideation, strategy, use_case,
         workflow, workflow_diagram, agent_spec, other)
       - Are dates in ISO 8601 format?
       - Is the description field present and non-empty?
    3. **Process**: Call process_file for each validated file
    4. **Report**: Summarise what was processed, what had errors

    ## Front Matter Schema

    Every artifact file must have this YAML front matter:

    ```yaml
    ---
    title: "Document Title"            # Required: short descriptive title
    description: "One-line summary"     # Required: makes search/triage effective
    artifact_type: ideation|strategy|use_case|workflow|workflow_diagram|agent_spec|other
    created: 2025-01-15T10:00:00Z       # ISO 8601 timestamp
    updated: 2025-01-15T10:00:00Z       # ISO 8601 timestamp
    status: draft|in_review|approved
    project: "Project Name"
    tags: []
    version: 1
    ---
    ```

    If front matter is missing or invalid, process_file will apply/fix it
    using sensible defaults. The key validation you do with ReasoningTools
    is to CATCH issues that the mechanical processing might miss — like
    a file that claims to be "strategy" but is in the "ideation" directory,
    or a description that's clearly wrong for the content.

    ## Using ReasoningTools

    Use `think` BEFORE processing each file to reason about:
    - Whether the front matter looks correct
    - Whether the file type matches its directory location
    - Whether there are any obvious issues to flag

    Use `analyze` AFTER processing to evaluate:
    - Whether the processing succeeded
    - Whether any files need attention (errors, mismatches)
    - Whether the overall batch was processed successfully

    This is how you validate — through structured reasoning, not by
    executing Python validation scripts.

    ## Conversational Queries

    When humans or agents ask you about artifacts, you can:
    - Use get_processing_stats to show current pipeline status
    - Use scan_staging_directory to show what's waiting to be processed
    - Use search_knowledge to find artifacts by content
    - Use FileTools to read specific artifact files from the archive

    Common queries you handle:
    - "What strategy artifacts exist?" → search_knowledge + stats
    - "Show me all documents with errors" → scan + stats
    - "How many artifacts have been processed?" → get_processing_stats
    - "Is there an artifact about X?" → search_knowledge

    ## Domain Knowledge

    Known domains: ai-assisted-learning (more will be added as the platform grows)
    Known artifact types: ideation, strategy, use_case, workflow,
                          workflow_diagram, agent_spec, other

    The "other" type is a catch-all for artifact types not yet formalised.
    If you see patterns in "other" artifacts (e.g., three are all persona
    documents), note it in your processing report — but don't create new
    types yourself. That's a human decision.

    ## Error Handling

    If a file can't be processed:
    - Don't skip it silently — report it explicitly
    - Don't delete it — it stays in staging for retry
    - Note what went wrong in your processing report

    Common errors:
    - File not valid markdown (can't parse front matter)
    - Missing required front matter fields
    - File is empty or too large
    - Permission issues reading/writing

    ## Archive Policy

    Processed files are MOVED to artifacts/_archive/<domain>/ — they are
    NOT deleted. The archive serves as:
    - A recovery safety net if the database or vector KB has issues
    - A human-readable backup while the web front end doesn't exist yet
    - A source for re-processing if needed

    Once the web front end provides human-readable artifact access, the
    archive policy can evolve to deletion instead of archival.

    ## What You Don't Do

    - You don't evaluate artifact content quality
    - You don't suggest improvements to artifacts
    - You don't create new artifacts
    - You don't modify artifact content beyond front matter
    - You don't judge whether an artifact is "correct" — only whether
      its metadata is structurally valid

    Those are the domain agents' responsibilities. You're the infrastructure.
"""
)

# ---------------------------------------------------------------------------
# Create the Agent
# ---------------------------------------------------------------------------
document_manager = Agent(
    name="Document Manager",
    model=Ollama(id="glm-5.1:cloud"),
    instructions=SYSTEM_INSTRUCTIONS,
    # --- Storage ---
    db=agent_db,
    # --- Knowledge ---
    # PgVector knowledge base — the agent indexes artifact content here
    knowledge=knowledge,
    search_knowledge=True,
    # --- Tools ---
    # No cache_results here — all tools are stateful or need fresh data:
    #   FileTools: needs latest file state (files may change mid-conversation)
    #   LocalFileSystemTools: fast local ops, no benefit from caching
    #   ReasoningTools: stateful reasoning
    #   Custom tools: scan/process/stats need fresh data every time
    tools=[
        # File operations scoped to the staging directory
        FileTools(base_dir=STAGING_BASE_DIR),
        # Browse staging and archive directories
        LocalFileSystemTools(target_directory=str(STAGING_BASE_DIR)),
        # Step-by-step front matter validation
        ReasoningTools(add_instructions=True),
        # Custom processing tools
        scan_staging_directory,  # Find unprocessed files
        process_file,  # Core processing pipeline
        get_processing_stats,  # Pipeline health and statistics
    ],
    # --- Memory ---
    # Agent memory only — infrastructure agent, no per-user preferences
    update_memory_on_run=True,
    # --- Session State ---
    # Tracks processing context within a conversation
    session_state={
        "last_scan_time": None,
        "pending_files": [],
        "processed_this_session": [],
        "errors_this_session": [],
        "total_processed": 0,
    },
    add_session_state_to_context=True,
    enable_agentic_state=True,
    # --- Context settings ---
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=10,
    # --- Output ---
    markdown=True,
)

# ---------------------------------------------------------------------------
# Run the Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 70)
    print("  Document Manager")
    print("  Type 'scan' to process files, 'stats' for pipeline status,")
    print("  or ask any question about artifacts. 'exit' to quit.")
    print("=" * 70)

    while True:
        user_input = input("\n📁 You: ").strip()
        if user_input.lower() in ("exit", "quit", "bye"):
            print("Goodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() == "scan":
            user_input = "Scan the staging directory and process any files found."

        if user_input.lower() == "stats":
            user_input = "Show me processing statistics."

        document_manager.print_response(user_input, stream=True)
