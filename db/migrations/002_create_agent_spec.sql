-- Migration: 002_create_agent_spec
-- Creates the agent_spec table for capturing completed agent design templates
-- as structured, code-generation-ready records.
-- Depends on: 001_create_design_system.sql

CREATE TABLE IF NOT EXISTS public.agent_spec (
    -- Identity
    id              UUID            NOT NULL DEFAULT gen_random_uuid(),
    design_system_id UUID           NOT NULL,
    agent_name      TEXT            NOT NULL,
    purpose         TEXT            NOT NULL,
    target_users    TEXT            NOT NULL,
    user_type       TEXT            NOT NULL,
    cognitive_mode  TEXT            NOT NULL,

    -- Architecture
    architecture_type TEXT          NOT NULL DEFAULT 'agent',
    sub_roles       JSONB,

    -- Knowledge
    knowledge_sources JSONB,
    memory_type     TEXT            NOT NULL DEFAULT 'none',
    enable_agentic_memory BOOLEAN   NOT NULL DEFAULT FALSE,
    update_memory_on_run  BOOLEAN   NOT NULL DEFAULT FALSE,

    -- Storage
    storage_type    TEXT            NOT NULL DEFAULT 'sqlite',
    storage_db_url  TEXT,
    vector_db_type  TEXT,

    -- Tools
    tools           JSONB,
    custom_tools    JSONB,

    -- Human-in-the-Loop
    hitl_enabled    BOOLEAN         NOT NULL DEFAULT FALSE,
    hitl_actions    JSONB,

    -- Intelligence & Behavior
    reasoning_level TEXT            NOT NULL DEFAULT 'none',
    output_format   TEXT            NOT NULL DEFAULT 'markdown',
    output_schema   JSONB,
    guardrails      JSONB,
    session_state_schema JSONB,
    enable_agentic_state BOOLEAN   NOT NULL DEFAULT FALSE,

    -- Deployment
    deployment_interfaces JSONB     NOT NULL DEFAULT '["web_chat"]'::jsonb,
    model_provider   TEXT           NOT NULL DEFAULT 'ollama',
    model_id         TEXT           NOT NULL DEFAULT 'glm-5.1:cloud',
    multimodal_inputs JSONB,
    schedule_enabled BOOLEAN        NOT NULL DEFAULT FALSE,
    schedule_cron    TEXT,
    observability_level TEXT        NOT NULL DEFAULT 'basic',
    observability_provider TEXT,

    -- Skills & Persona
    skills_domains  JSONB,
    system_prompt   TEXT,
    instructions    JSONB,
    description     TEXT,
    expected_output TEXT,

    -- Constraints
    cost_preference  TEXT           NOT NULL DEFAULT 'balanced',
    latency_requirement TEXT        NOT NULL DEFAULT 'conversational',
    runtime_environment TEXT        NOT NULL DEFAULT 'local',

    -- Auto-Derived (populated by derive_spec_metadata, not the user)
    required_env_vars JSONB,
    pip_dependencies  JSONB,
    additional_setup_notes TEXT,

    -- Lifecycle
    status          TEXT            NOT NULL DEFAULT 'draft',
    created_at      TIMESTAMPTZ    NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ    NOT NULL DEFAULT now(),
    created_by      UUID            NOT NULL,

    -- Primary Key
    CONSTRAINT pk_agent_spec PRIMARY KEY (id),

    -- Foreign Keys
    CONSTRAINT fk_agent_spec_design_system FOREIGN KEY (design_system_id)
        REFERENCES public.design_system(id) ON DELETE CASCADE,
    CONSTRAINT fk_agent_spec_created_by FOREIGN KEY (created_by)
        REFERENCES auth.users(id) ON DELETE RESTRICT,

    -- CHECK constraints
    CONSTRAINT chk_user_type CHECK (user_type IN ('non_technical','semi_technical','developer','agent','internal')),
    CONSTRAINT chk_cognitive_mode CHECK (cognitive_mode IN ('extractor','measurer','assessor','generator','aggregator')),
    CONSTRAINT chk_architecture_type CHECK (architecture_type IN ('agent','team','workflow')),
    CONSTRAINT chk_memory_type CHECK (memory_type IN ('none','user_memory','org_memory','both')),
    CONSTRAINT chk_reasoning_level CHECK (reasoning_level IN ('none','moderate','deep')),
    CONSTRAINT chk_output_format CHECK (output_format IN ('text','markdown','structured','mixed')),
    CONSTRAINT chk_cost_preference CHECK (cost_preference IN ('minimize','balanced','performance_first')),
    CONSTRAINT chk_latency_requirement CHECK (latency_requirement IN ('realtime','conversational','batch')),
    CONSTRAINT chk_runtime_environment CHECK (runtime_environment IN ('local','docker','cloud','agent_os')),
    CONSTRAINT chk_status CHECK (status IN ('draft','spec_complete','code_generated','tested','deployed')),
    CONSTRAINT chk_storage_type CHECK (storage_type IN ('sqlite','postgres','mongodb','redis','in_memory')),
    CONSTRAINT chk_model_provider CHECK (model_provider IN ('ollama','openai','anthropic','google','other')),
    CONSTRAINT chk_observability_level CHECK (observability_level IN ('none','basic','advanced')),
    -- 'none' removed: use NULL to indicate no provider is set
    CONSTRAINT chk_observability_provider CHECK (
        observability_provider IS NULL
        OR observability_provider IN ('langfuse','langsmith','arize','langwatch')
    ),
    -- 'none' removed: use NULL to indicate no vector DB is needed
    CONSTRAINT chk_vector_db_type CHECK (
        vector_db_type IS NULL
        OR vector_db_type IN ('lancedb','pgvector','chroma','pinecone','qdrant','milvus','weaviate','redis')
    ),

    -- Cross-column constraints
    CONSTRAINT chk_sub_roles_for_team CHECK (architecture_type = 'agent' OR sub_roles IS NOT NULL),
    CONSTRAINT chk_vector_db_for_knowledge CHECK (knowledge_sources IS NULL OR vector_db_type IS NOT NULL),
    CONSTRAINT chk_schedule_cron CHECK (NOT schedule_enabled OR schedule_cron IS NOT NULL),
    CONSTRAINT chk_advanced_observability CHECK (
        observability_level != 'advanced' OR observability_provider IS NOT NULL
    ),
    CONSTRAINT chk_structured_output_schema CHECK (output_format != 'structured' OR output_schema IS NOT NULL),
    CONSTRAINT chk_hitl_actions CHECK (NOT hitl_enabled OR hitl_actions IS NOT NULL)
);

-- Indexes
CREATE INDEX ix_agent_spec_design_system ON public.agent_spec (design_system_id);
CREATE INDEX ix_agent_spec_status ON public.agent_spec (status);
CREATE INDEX ix_agent_spec_cognitive_mode ON public.agent_spec (cognitive_mode);
CREATE INDEX ix_agent_spec_architecture ON public.agent_spec (architecture_type);
CREATE INDEX ix_agent_spec_created_by ON public.agent_spec (created_by);

-- Trigger to auto-update updated_at
CREATE OR REPLACE FUNCTION update_agent_spec_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_agent_spec_updated_at
    BEFORE UPDATE ON public.agent_spec
    FOR EACH ROW
    EXECUTE FUNCTION update_agent_spec_updated_at();
