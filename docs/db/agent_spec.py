"""
SQLAlchemy Core Table definition for the `agent_spec` table.

Captures a completed agent design template as a single, structured record.
Every column maps directly to an Agno API parameter or a code-generation decision.
A code generator reads one row and produces a complete, runnable Python agent
file + setup instructions.

This object is used for query composition only. The authoritative DDL is in
agentia/db/migrations/XXX_create_agent_spec.sql — CHECK constraints and indexes
are expressed there, not here.
"""

import sqlalchemy as sa
from db import metadata

agent_spec_table = sa.Table(
    "agent_spec",
    metadata,
    # ── Identity ────────────────────────────────────────────────────────────
    sa.Column(
        "id",
        sa.UUID(as_uuid=True),
        nullable=False,
        server_default=sa.text("gen_random_uuid()"),
    ),
    sa.Column("design_system_id", sa.UUID(as_uuid=True), nullable=False),
    sa.Column("agent_name", sa.Text(), nullable=False),
    sa.Column("purpose", sa.Text(), nullable=False),
    sa.Column("target_users", sa.Text(), nullable=False),
    # Normalized: non_technical | semi_technical | developer | agent | internal
    sa.Column("user_type", sa.Text(), nullable=False),
    # extractor | measurer | assessor | generator | aggregator
    sa.Column("cognitive_mode", sa.Text(), nullable=False),

    # ── Architecture ────────────────────────────────────────────────────────
    # agent | team | workflow
    sa.Column("architecture_type", sa.Text(), nullable=False, server_default=sa.text("'agent'")),
    # Array of {role, responsibility} — only for team/workflow
    sa.Column("sub_roles", sa.JSON(), nullable=True),

    # ── Knowledge ───────────────────────────────────────────────────────────
    # Array of {type, details}
    sa.Column("knowledge_sources", sa.JSON(), nullable=True),
    # none | user_memory | org_memory | both
    sa.Column("memory_type", sa.Text(), nullable=False, server_default=sa.text("'none'")),
    sa.Column(
        "enable_agentic_memory",
        sa.Boolean(),
        nullable=False,
        server_default=sa.text("FALSE"),
    ),
    sa.Column(
        "update_memory_on_run",
        sa.Boolean(),
        nullable=False,
        server_default=sa.text("FALSE"),
    ),

    # ── Storage ─────────────────────────────────────────────────────────────
    # sqlite | postgres | mongodb | redis | in_memory
    sa.Column("storage_type", sa.Text(), nullable=False, server_default=sa.text("'sqlite'")),
    sa.Column("storage_db_url", sa.Text(), nullable=True),
    # lancedb | pgvector | chroma | pinecone | qdrant | milvus | weaviate | redis | none
    sa.Column("vector_db_type", sa.Text(), nullable=True),

    # ── Tools ───────────────────────────────────────────────────────────────
    # Array of {toolkit_name, config} — matches Agno toolkit import names
    sa.Column("tools", sa.JSON(), nullable=True),
    # Array of {name, description, code_stub} for custom Python tools
    sa.Column("custom_tools", sa.JSON(), nullable=True),

    # ── Human-in-the-Loop ──────────────────────────────────────────────────
    sa.Column(
        "hitl_enabled",
        sa.Boolean(),
        nullable=False,
        server_default=sa.text("FALSE"),
    ),
    # Array of action names requiring human approval
    sa.Column("hitl_actions", sa.JSON(), nullable=True),

    # ── Intelligence & Behavior ─────────────────────────────────────────────
    # none | moderate | deep
    sa.Column("reasoning_level", sa.Text(), nullable=False, server_default=sa.text("'none'")),
    # text | markdown | structured | mixed
    sa.Column("output_format", sa.Text(), nullable=False, server_default=sa.text("'markdown'")),
    # JSON Schema for Pydantic output model (if output_format = structured)
    sa.Column("output_schema", sa.JSON(), nullable=True),
    # Array of {type, config} — pii_detection | prompt_injection | content_moderation | input_validation | output_validation | custom
    sa.Column("guardrails", sa.JSON(), nullable=True),
    # Description of state that persists across turns
    sa.Column("session_state_schema", sa.JSON(), nullable=True),
    sa.Column(
        "enable_agentic_state",
        sa.Boolean(),
        nullable=False,
        server_default=sa.text("FALSE"),
    ),

    # ── Deployment ──────────────────────────────────────────────────────────
    # Array: web_chat | slack | discord | telegram | whatsapp | rest_api | mcp_server | cli
    sa.Column("deployment_interfaces", sa.JSON(), nullable=False, server_default=sa.text("'[\"web_chat\"]'")),
    # ollama | openai | anthropic | google | other
    sa.Column("model_provider", sa.Text(), nullable=False, server_default=sa.text("'ollama'")),
    sa.Column("model_id", sa.Text(), nullable=False, server_default=sa.text("'glm-5.1:cloud'")),
    # Array: image | audio | video | file
    sa.Column("multimodal_inputs", sa.JSON(), nullable=True),
    sa.Column(
        "schedule_enabled",
        sa.Boolean(),
        nullable=False,
        server_default=sa.text("FALSE"),
    ),
    sa.Column("schedule_cron", sa.Text(), nullable=True),
    # none | basic | advanced
    sa.Column("observability_level", sa.Text(), nullable=False, server_default=sa.text("'basic'")),
    # langfuse | langsmith | arize | langwatch | none
    sa.Column("observability_provider", sa.Text(), nullable=True),

    # ── Skills & Persona ───────────────────────────────────────────────────
    # Array of domain name strings
    sa.Column("skills_domains", sa.JSON(), nullable=True),
    sa.Column("system_prompt", sa.Text(), nullable=True),
    # Array of instruction strings (Agno `instructions` param)
    sa.Column("instructions", sa.JSON(), nullable=True),
    sa.Column("description", sa.Text(), nullable=True),
    sa.Column("expected_output", sa.Text(), nullable=True),

    # ── Constraints ─────────────────────────────────────────────────────────
    # minimize | balanced | performance_first
    sa.Column("cost_preference", sa.Text(), nullable=False, server_default=sa.text("'balanced'")),
    # realtime | conversational | batch
    sa.Column("latency_requirement", sa.Text(), nullable=False, server_default=sa.text("'conversational'")),
    # local | docker | cloud | agent_os
    sa.Column("runtime_environment", sa.Text(), nullable=False, server_default=sa.text("'local'")),

    # ── Auto-Derived (filled by spec processor, not user) ──────────────────
    # Array of {var_name, description, required_by}
    sa.Column("required_env_vars", sa.JSON(), nullable=True),
    # Array of pip package strings
    sa.Column("pip_dependencies", sa.JSON(), nullable=True),
    # Free-text notes about external tasks
    sa.Column("additional_setup_notes", sa.Text(), nullable=True),

    # ── Lifecycle ───────────────────────────────────────────────────────────
    # draft | spec_complete | code_generated | tested | deployed
    sa.Column(
        "status",
        sa.Text(),
        nullable=False,
        server_default=sa.text("'draft'"),
    ),
    sa.Column(
        "created_at",
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.text("now()"),
    ),
    sa.Column(
        "updated_at",
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.text("now()"),
    ),
    sa.Column("created_by", sa.UUID(as_uuid=True), nullable=False),

    schema="public",
)