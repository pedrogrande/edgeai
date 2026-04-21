"""
Agent Spec Tools — Agno Toolkit for creating and managing agent_spec rows in Supabase.

Provides tools for the agent_designer to persist completed specs, track lifecycle
status, and auto-derive pip dependencies, env vars, and setup notes.

Required environment variables:
    SUPABASE_DB_URL              PostgreSQL connection URL (Supabase session pooler)
                                 Format: postgresql://postgres.[ref]:[password]@aws-1-[region].pooler.supabase.com:5432/postgres
    AGENT_SPEC_USER_ID           UUID of the Supabase auth user (owner of specs)
    AGENT_SPEC_DESIGN_SYSTEM_ID  UUID of the default design system (optional — can pass per call)

Usage in agent_designer.py:
    from tools.agent_spec_tools import AgentSpecTools
    tools=[AgentSpecTools(), ...]
"""

import json
import os
from datetime import datetime
from typing import Any

import psycopg
import psycopg.rows
from agno.tools import Toolkit
from agno.utils.log import logger

# ─── Derivation maps ──────────────────────────────────────────────────────────

_MODEL_DEPS: dict[str, list[str]] = {
    "openai":    ["agno[openai]", "openai"],
    "anthropic": ["agno[anthropic]", "anthropic"],
    "google":    ["agno[google]", "google-generativeai"],
    "ollama":    ["agno[ollama]", "ollama"],
    "other":     ["agno"],
}

_MODEL_ENV_VARS: dict[str, list[dict]] = {
    "openai":    [{"var_name": "OPENAI_API_KEY",    "description": "OpenAI API key",    "required_by": "model_provider=openai"}],
    "anthropic": [{"var_name": "ANTHROPIC_API_KEY", "description": "Anthropic API key", "required_by": "model_provider=anthropic"}],
    "google":    [{"var_name": "GOOGLE_API_KEY",    "description": "Google AI API key", "required_by": "model_provider=google"}],
    "ollama":    [],
    "other":     [],
}

_STORAGE_DEPS: dict[str, list[str]] = {
    "postgres":  ["psycopg[binary]"],
    "mongodb":   ["pymongo"],
    "redis":     ["redis"],
    "sqlite":    [],
    "in_memory": [],
}

_VECTOR_DB_DEPS: dict[str, list[str]] = {
    "lancedb":  ["lancedb"],
    "pgvector": ["pgvector", "psycopg[binary]"],
    "chroma":   ["chromadb"],
    "pinecone": ["pinecone"],
    "qdrant":   ["qdrant-client"],
    "milvus":   ["pymilvus"],
    "weaviate": ["weaviate-client"],
    "redis":    ["redis"],
}

_TOOL_DEPS: dict[str, list[str]] = {
    "DuckDuckGoTools":   ["ddgs"],
    "TavilyTools":       ["tavily-python"],
    "ExaTools":          ["exa-py"],
    "PostgresTools":     ["psycopg[binary]"],
    "YFinanceTools":     ["yfinance"],
    "PandasTools":       ["pandas"],
    "SpiderTools":       ["spider-client"],
    "GitHubTools":       ["PyGithub"],
    "TwilioTools":       ["twilio"],
    "SlackTools":        ["slack-sdk"],
    "WikipediaTools":    ["wikipedia"],
    "ArxivTools":        ["arxiv"],
    "SerpApiTools":      ["google-search-results"],
    "GoogleSearchTools": ["google-api-python-client"],
    "NewsApiTools":      ["newsapi-python"],
}

_TOOL_ENV_VARS: dict[str, list[dict]] = {
    "TavilyTools":    [{"var_name": "TAVILY_API_KEY",      "description": "Tavily search API key",          "required_by": "TavilyTools"}],
    "ExaTools":       [{"var_name": "EXA_API_KEY",         "description": "Exa search API key",             "required_by": "ExaTools"}],
    "BraveTools":     [{"var_name": "BRAVE_API_KEY",       "description": "Brave search API key",           "required_by": "BraveTools"}],
    "SpiderTools":    [{"var_name": "SPIDER_API_KEY",      "description": "Spider crawler API key",         "required_by": "SpiderTools"}],
    "SerpApiTools":   [{"var_name": "SERPAPI_API_KEY",     "description": "SerpAPI key",                    "required_by": "SerpApiTools"}],
    "NewsApiTools":   [{"var_name": "NEWS_API_KEY",        "description": "NewsAPI key",                    "required_by": "NewsApiTools"}],
    "GitHubTools":    [{"var_name": "GITHUB_TOKEN",        "description": "GitHub personal access token",  "required_by": "GitHubTools"}],
    "SlackTools":     [{"var_name": "SLACK_BOT_TOKEN",     "description": "Slack bot token",                "required_by": "SlackTools"}],
    "TwilioTools": [
        {"var_name": "TWILIO_ACCOUNT_SID", "description": "Twilio account SID",  "required_by": "TwilioTools"},
        {"var_name": "TWILIO_AUTH_TOKEN",  "description": "Twilio auth token",   "required_by": "TwilioTools"},
    ],
    "ZendeskTools": [
        {"var_name": "ZENDESK_SUBDOMAIN", "description": "Zendesk subdomain", "required_by": "ZendeskTools"},
        {"var_name": "ZENDESK_API_KEY",   "description": "Zendesk API key",   "required_by": "ZendeskTools"},
    ],
}

_OBS_DEPS: dict[str, list[str]] = {
    "langfuse":  ["langfuse"],
    "langsmith": ["langsmith"],
    "arize":     ["arize-phoenix"],
    "langwatch": ["langwatch"],
}

_OBS_ENV_VARS: dict[str, list[dict]] = {
    "langfuse": [
        {"var_name": "LANGFUSE_PUBLIC_KEY", "description": "Langfuse public key",  "required_by": "observability=langfuse"},
        {"var_name": "LANGFUSE_SECRET_KEY", "description": "Langfuse secret key",  "required_by": "observability=langfuse"},
        {"var_name": "LANGFUSE_HOST",       "description": "Langfuse host URL",    "required_by": "observability=langfuse"},
    ],
    "langsmith": [
        {"var_name": "LANGCHAIN_API_KEY",    "description": "LangSmith API key",            "required_by": "observability=langsmith"},
        {"var_name": "LANGCHAIN_TRACING_V2", "description": "Enable tracing (set to true)", "required_by": "observability=langsmith"},
    ],
    "arize": [
        {"var_name": "PHOENIX_API_KEY", "description": "Arize Phoenix API key", "required_by": "observability=arize"},
    ],
    "langwatch": [
        {"var_name": "LANGWATCH_API_KEY", "description": "LangWatch API key", "required_by": "observability=langwatch"},
    ],
}

# JSONB columns — values must be json.dumps()'d before INSERT/UPDATE
_JSONB_COLUMNS: frozenset[str] = frozenset({
    "sub_roles", "knowledge_sources", "tools", "custom_tools", "hitl_actions",
    "output_schema", "guardrails", "session_state_schema", "deployment_interfaces",
    "multimodal_inputs", "skills_domains", "instructions", "required_env_vars",
    "pip_dependencies",
})

# Whitelist of writable columns — prevents SQL injection via column names
_WRITABLE_COLUMNS: frozenset[str] = frozenset({
    "agent_name", "purpose", "target_users", "user_type", "cognitive_mode",
    "architecture_type", "sub_roles", "knowledge_sources", "memory_type",
    "enable_agentic_memory", "update_memory_on_run", "storage_type", "storage_db_url",
    "vector_db_type", "tools", "custom_tools", "hitl_enabled", "hitl_actions",
    "reasoning_level", "output_format", "output_schema", "guardrails",
    "session_state_schema", "enable_agentic_state", "deployment_interfaces",
    "model_provider", "model_id", "multimodal_inputs", "schedule_enabled",
    "schedule_cron", "observability_level", "observability_provider",
    "skills_domains", "system_prompt", "instructions", "description",
    "expected_output", "cost_preference", "latency_requirement",
    "runtime_environment", "required_env_vars", "pip_dependencies",
    "additional_setup_notes", "status", "design_system_id", "created_by",
})

_VALID_STATUSES = ["draft", "spec_complete", "code_generated", "tested", "deployed"]


def _serialize(obj: Any) -> str:
    """Serialize a row dict or list to a JSON string, handling datetime and UUID values."""
    def _default(o: Any) -> str:
        if isinstance(o, datetime):
            return o.isoformat()
        return str(o)

    return json.dumps(obj, default=_default, indent=2)


def _encode_jsonb(data: dict) -> dict:
    """JSON-encode any JSONB column values that are still Python objects."""
    result = dict(data)
    for col in _JSONB_COLUMNS:
        if col in result and not isinstance(result[col], str):
            result[col] = json.dumps(result[col])
    return result


class AgentSpecTools(Toolkit):
    """
    Agno Toolkit for creating and managing agent_spec rows in Supabase.

    Gives the agent_designer the ability to:
    - Create and list design systems
    - Create, read, update, and list agent specs
    - Advance the spec lifecycle status
    - Auto-derive pip dependencies, env vars, and setup notes
    """

    def __init__(self, db_url: str | None = None):
        super().__init__(name="agent_spec_tools")
        self.db_url = db_url or os.environ.get("SUPABASE_DB_URL", "")
        self.default_user_id = os.environ.get("AGENT_SPEC_USER_ID", "")
        self.default_design_system_id = os.environ.get("AGENT_SPEC_DESIGN_SYSTEM_ID", "")
        self.register(self.create_design_system)
        self.register(self.list_design_systems)
        self.register(self.create_agent_spec)
        self.register(self.update_agent_spec)
        self.register(self.get_agent_spec)
        self.register(self.list_agent_specs)
        self.register(self.set_spec_status)
        self.register(self.derive_spec_metadata)

    def _connect(self) -> psycopg.Connection:
        if not self.db_url:
            raise ValueError(
                "SUPABASE_DB_URL is not set. Add it to your .env file.\n"
                "Format: postgresql://postgres.[ref]:[password]@aws-1-[region].pooler.supabase.com:5432/postgres"
            )
        return psycopg.connect(self.db_url, row_factory=psycopg.rows.dict_row)

    # ─── Design System ────────────────────────────────────────────────────────

    def create_design_system(self, name: str, description: str = "", user_id: str = "") -> str:
        """
        Create a new design system and return its UUID.
        A design system groups related agent specs together (e.g. one per project or product).

        Args:
            name: Human-readable name (e.g. "Customer Support Platform")
            description: Optional description of what this design system covers
            user_id: Supabase auth user UUID. Falls back to AGENT_SPEC_USER_ID env var.

        Returns:
            The UUID of the created design system, or an error message.
        """
        uid = user_id or self.default_user_id
        if not uid:
            return "Error: user_id is required. Set AGENT_SPEC_USER_ID env var or pass user_id."
        try:
            with self._connect() as conn:
                row = conn.execute(
                    """
                    INSERT INTO public.design_system (name, description, created_by)
                    VALUES (%s, %s, %s::uuid)
                    RETURNING id
                    """,
                    (name, description or None, uid),
                ).fetchone()
                return str(row["id"])
        except Exception as e:
            logger.error(f"create_design_system failed: {e}")
            return f"Error: {e}"

    def list_design_systems(self) -> str:
        """
        List all design systems.

        Returns:
            JSON list of {id, name, description, created_at} objects.
        """
        try:
            with self._connect() as conn:
                rows = conn.execute(
                    "SELECT id, name, description, created_at "
                    "FROM public.design_system ORDER BY created_at DESC"
                ).fetchall()
                return _serialize([dict(r) for r in rows])
        except Exception as e:
            logger.error(f"list_design_systems failed: {e}")
            return f"Error: {e}"

    # ─── Agent Spec ───────────────────────────────────────────────────────────

    def create_agent_spec(
        self,
        spec_json: str,
        design_system_id: str = "",
        user_id: str = "",
    ) -> str:
        """
        Create a new agent spec row from a JSON string. Returns the created spec's UUID.

        The spec_json must include at minimum:
            agent_name, purpose, target_users, user_type, cognitive_mode

        All other fields are optional and will use their database defaults.

        Args:
            spec_json: JSON object with the spec fields (see agent_spec table schema)
            design_system_id: UUID of the parent design system. Falls back to
                              AGENT_SPEC_DESIGN_SYSTEM_ID env var. Create one first
                              with create_design_system() if needed.
            user_id: Supabase auth user UUID. Falls back to AGENT_SPEC_USER_ID env var.

        Returns:
            The UUID of the created agent spec, or an error message.
        """
        uid = user_id or self.default_user_id
        dsid = design_system_id or self.default_design_system_id
        if not uid:
            return "Error: user_id is required. Set AGENT_SPEC_USER_ID env var or pass user_id."
        if not dsid:
            return (
                "Error: design_system_id is required. "
                "Use create_design_system() to create one, then pass its UUID here "
                "or set AGENT_SPEC_DESIGN_SYSTEM_ID env var."
            )

        try:
            data: dict[str, Any] = json.loads(spec_json)
        except json.JSONDecodeError as e:
            return f"Error: Invalid JSON in spec_json: {e}"

        data["design_system_id"] = dsid
        data["created_by"] = uid

        # Filter to allowed columns only (prevents SQL injection via column names)
        data = {k: v for k, v in data.items() if k in _WRITABLE_COLUMNS}

        data = _encode_jsonb(data)

        cols = list(data.keys())
        placeholders = []
        for c in cols:
            if c in ("design_system_id", "created_by"):
                placeholders.append("%s::uuid")
            elif c in _JSONB_COLUMNS:
                placeholders.append("%s::jsonb")
            else:
                placeholders.append("%s")

        values = [data[c] for c in cols]
        sql = (
            f"INSERT INTO public.agent_spec ({', '.join(cols)}) "
            f"VALUES ({', '.join(placeholders)}) "
            f"RETURNING id"
        )

        try:
            with self._connect() as conn:
                row = conn.execute(sql, values).fetchone()
                return str(row["id"])
        except Exception as e:
            logger.error(f"create_agent_spec failed: {e}")
            return f"Error: {e}"

    def update_agent_spec(self, spec_id: str, updates_json: str) -> str:
        """
        Update fields on an existing agent spec row (partial update).

        Args:
            spec_id: UUID of the agent spec to update
            updates_json: JSON object with field:value pairs to update

        Returns:
            "Updated successfully." or an error message.
        """
        try:
            updates: dict[str, Any] = json.loads(updates_json)
        except json.JSONDecodeError as e:
            return f"Error: Invalid JSON in updates_json: {e}"

        if not updates:
            return "Error: updates_json is empty."

        # Filter to allowed columns only
        updates = {k: v for k, v in updates.items() if k in _WRITABLE_COLUMNS}
        if not updates:
            return "Error: No valid columns found in updates_json."

        updates = _encode_jsonb(updates)

        set_clauses = []
        values = []
        for col, val in updates.items():
            if col in _JSONB_COLUMNS:
                set_clauses.append(f"{col} = %s::jsonb")
            else:
                set_clauses.append(f"{col} = %s")
            values.append(val)

        values.append(spec_id)
        sql = f"UPDATE public.agent_spec SET {', '.join(set_clauses)} WHERE id = %s::uuid"

        try:
            with self._connect() as conn:
                conn.execute(sql, values)
                return "Updated successfully."
        except Exception as e:
            logger.error(f"update_agent_spec failed: {e}")
            return f"Error: {e}"

    def get_agent_spec(self, spec_id: str) -> str:
        """
        Get the full agent spec row as a JSON string.

        Args:
            spec_id: UUID of the agent spec

        Returns:
            JSON string of the full spec row, or an error message.
        """
        try:
            with self._connect() as conn:
                row = conn.execute(
                    "SELECT * FROM public.agent_spec WHERE id = %s::uuid",
                    (spec_id,),
                ).fetchone()
                if row is None:
                    return f"Error: No agent spec found with id '{spec_id}'"
                return _serialize(dict(row))
        except Exception as e:
            logger.error(f"get_agent_spec failed: {e}")
            return f"Error: {e}"

    def list_agent_specs(self, status: str = "all") -> str:
        """
        List agent specs, optionally filtered by lifecycle status.

        Args:
            status: One of draft/spec_complete/code_generated/tested/deployed/all

        Returns:
            JSON list of {id, agent_name, status, created_at} objects.
        """
        try:
            with self._connect() as conn:
                if status == "all":
                    rows = conn.execute(
                        "SELECT id, agent_name, status, created_at "
                        "FROM public.agent_spec ORDER BY created_at DESC"
                    ).fetchall()
                else:
                    rows = conn.execute(
                        "SELECT id, agent_name, status, created_at "
                        "FROM public.agent_spec WHERE status = %s "
                        "ORDER BY created_at DESC",
                        (status,),
                    ).fetchall()
                return _serialize([dict(r) for r in rows])
        except Exception as e:
            logger.error(f"list_agent_specs failed: {e}")
            return f"Error: {e}"

    def set_spec_status(self, spec_id: str, new_status: str) -> str:
        """
        Advance the lifecycle status of an agent spec.
        Valid progression: draft → spec_complete → code_generated → tested → deployed

        Args:
            spec_id: UUID of the agent spec
            new_status: One of: draft, spec_complete, code_generated, tested, deployed

        Returns:
            "Status updated to '{new_status}'." or an error message.
        """
        if new_status not in _VALID_STATUSES:
            return (
                f"Error: Invalid status '{new_status}'. "
                f"Must be one of: {', '.join(_VALID_STATUSES)}"
            )
        try:
            with self._connect() as conn:
                row = conn.execute(
                    "UPDATE public.agent_spec SET status = %s WHERE id = %s::uuid RETURNING id",
                    (new_status, spec_id),
                ).fetchone()
                if row is None:
                    return f"Error: No agent spec found with id '{spec_id}'"
                return f"Status updated to '{new_status}'."
        except Exception as e:
            logger.error(f"set_spec_status failed: {e}")
            return f"Error: {e}"

    def derive_spec_metadata(self, spec_id: str) -> str:
        """
        Auto-derive pip_dependencies, required_env_vars, and additional_setup_notes
        from the spec's tool, model, storage, vector DB, observability, and schedule settings.
        Writes the derived values directly to the spec row.

        Call this after create_agent_spec() to complete the auto-derived fields.

        Args:
            spec_id: UUID of the agent spec to process

        Returns:
            A summary of what was derived and written, or an error message.
        """
        try:
            with self._connect() as conn:
                row = conn.execute(
                    "SELECT * FROM public.agent_spec WHERE id = %s::uuid", (spec_id,)
                ).fetchone()
        except Exception as e:
            return f"Error reading spec: {e}"

        if row is None:
            return f"Error: No agent spec found with id '{spec_id}'"

        row = dict(row)
        pip_deps: list[str] = []
        env_vars: list[dict] = []
        setup_notes: list[str] = []

        # Model provider
        provider = row.get("model_provider") or "ollama"
        pip_deps.extend(_MODEL_DEPS.get(provider, []))
        env_vars.extend(_MODEL_ENV_VARS.get(provider, []))
        if provider == "ollama":
            model_id = row.get("model_id") or "glm-5.1:cloud"
            setup_notes.append(
                f"Start Ollama before running: `ollama serve`. "
                f"Pull the model: `ollama pull {model_id}`."
            )

        # Storage
        storage = row.get("storage_type") or "sqlite"
        pip_deps.extend(_STORAGE_DEPS.get(storage, []))
        if storage == "postgres":
            setup_notes.append(
                "Provision a PostgreSQL database. Set the connection URL in storage_db_url or via env var."
            )
        elif storage == "mongodb":
            setup_notes.append("Start a MongoDB instance. Provide the connection URL in storage_db_url.")
        elif storage == "redis":
            setup_notes.append("Start a Redis instance. Provide the connection URL in storage_db_url.")

        # Vector DB (NULL means none needed)
        vector_db = row.get("vector_db_type")
        if vector_db:
            pip_deps.extend(_VECTOR_DB_DEPS.get(vector_db, []))
            if vector_db == "pgvector":
                setup_notes.append(
                    "Enable pgvector in your PostgreSQL database: "
                    "`CREATE EXTENSION IF NOT EXISTS vector;`"
                )
            elif vector_db == "chroma":
                setup_notes.append(
                    "ChromaDB runs in ephemeral mode by default. "
                    "Pass a `path` argument to persist data between runs."
                )
            elif vector_db == "pinecone":
                env_vars.append({
                    "var_name": "PINECONE_API_KEY",
                    "description": "Pinecone API key",
                    "required_by": "vector_db_type=pinecone",
                })
                setup_notes.append("Create a Pinecone index. Set PINECONE_API_KEY and PINECONE_INDEX_NAME.")
            elif vector_db == "qdrant":
                setup_notes.append("Start Qdrant: `docker run -p 6333:6333 qdrant/qdrant:latest`")
            elif vector_db == "weaviate":
                setup_notes.append(
                    "Start Weaviate: `docker run -p 8080:8080 semitechnologies/weaviate:latest`"
                )

        # Tools
        tools_val = row.get("tools") or []
        if isinstance(tools_val, str):
            tools_val = json.loads(tools_val)
        for tool_entry in tools_val:
            tk_name = tool_entry.get("toolkit_name", "")
            pip_deps.extend(_TOOL_DEPS.get(tk_name, []))
            env_vars.extend(_TOOL_ENV_VARS.get(tk_name, []))

        # Observability (NULL means no provider)
        obs_provider = row.get("observability_provider")
        if obs_provider:
            pip_deps.extend(_OBS_DEPS.get(obs_provider, []))
            env_vars.extend(_OBS_ENV_VARS.get(obs_provider, []))

        # Human-in-the-loop
        if row.get("hitl_enabled"):
            actions_val = row.get("hitl_actions") or []
            if isinstance(actions_val, str):
                actions_val = json.loads(actions_val)
            setup_notes.append(
                f"Human-in-the-loop confirmation is required for: {', '.join(actions_val)}. "
                "Connect a frontend that handles the confirmation UI for these actions."
            )

        # Scheduled execution
        if row.get("schedule_enabled"):
            cron = row.get("schedule_cron") or ""
            setup_notes.append(
                f"This agent runs on a schedule ({cron}). "
                "Ensure your runtime supports cron execution or use a task scheduler."
            )

        # Deduplicate while preserving order
        seen_deps: set[str] = set()
        unique_deps = [d for d in pip_deps if not (d in seen_deps or seen_deps.add(d))]  # type: ignore[func-returns-value]

        seen_vars: set[str] = set()
        unique_vars = [
            v for v in env_vars
            if not (v["var_name"] in seen_vars or seen_vars.add(v["var_name"]))  # type: ignore[func-returns-value]
        ]

        notes_text = "\n\n".join(setup_notes) if setup_notes else None

        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    UPDATE public.agent_spec
                    SET pip_dependencies      = %s::jsonb,
                        required_env_vars     = %s::jsonb,
                        additional_setup_notes = %s
                    WHERE id = %s::uuid
                    """,
                    (
                        json.dumps(unique_deps),
                        json.dumps(unique_vars),
                        notes_text,
                        spec_id,
                    ),
                )
        except Exception as e:
            return f"Error writing derived metadata: {e}"

        return (
            f"Derived metadata written to spec {spec_id}:\n"
            f"  pip_dependencies ({len(unique_deps)}): {unique_deps}\n"
            f"  required_env_vars ({len(unique_vars)}): {[v['var_name'] for v in unique_vars]}\n"
            f"  additional_setup_notes: {len(setup_notes)} note(s)"
        )
