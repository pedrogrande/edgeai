-- Migration: 001_create_design_system
-- Creates the design_system table — a top-level container for grouping related
-- agent specs (e.g. one per product, project, or team).
-- Run this BEFORE 002_create_agent_spec.sql.

CREATE TABLE IF NOT EXISTS public.design_system (
    id              UUID            NOT NULL DEFAULT gen_random_uuid(),
    name            TEXT            NOT NULL,
    description     TEXT,
    created_by      UUID            NOT NULL REFERENCES auth.users(id) ON DELETE RESTRICT,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT now(),

    CONSTRAINT pk_design_system PRIMARY KEY (id)
);

CREATE INDEX ix_design_system_created_by ON public.design_system (created_by);

CREATE OR REPLACE FUNCTION update_design_system_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_design_system_updated_at
    BEFORE UPDATE ON public.design_system
    FOR EACH ROW
    EXECUTE FUNCTION update_design_system_updated_at();
