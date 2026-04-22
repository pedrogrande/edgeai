# Phase 7: PERSIST

## Goal
Save the completed spec to the database so it can be tracked, referenced, and evolved.

## Steps

### 1. Build the Spec JSON
Construct a JSON object from all design decisions made in Phases 1–5. Include at minimum:
- `agent_name`
- `purpose`
- `target_users`
- `user_type`
- `cognitive_mode`

Plus any non-default values for:
- Architecture (single/workflow/team)
- Tools (list with import paths)
- Knowledge (type, vector DB, embedder)
- Memory (agent/user/both)
- Model (Ollama model ID)
- Storage (DB type and URL)
- Guardrails
- Deployment target
- Cost/latency constraints

### 2. Create or Get Design System
- If no design system exists, call `create_design_system()` with a descriptive name
- Otherwise, use the existing design system UUID (from `AGENT_SPEC_DESIGN_SYSTEM_ID` env var)

### 3. Create Agent Spec
- Call `create_agent_spec()` with the JSON and the design system UUID
- This returns the spec's UUID — save this!

### 4. Derive Metadata
- Call `derive_spec_metadata()` with the spec UUID
- This auto-populates `pip_dependencies`, `required_env_vars`, and `additional_setup_notes`

### 5. Advance Lifecycle Status
- Call `set_spec_status()` with the spec UUID and `"spec_complete"`
- This advances from `draft` to `spec_complete`

### 6. Report to User
- Share the spec UUID so the user can reference it later
- Confirm the spec has been persisted
- Note the current lifecycle status

## Error Handling
- If `AGENT_SPEC_USER_ID` or `SUPABASE_DB_URL` are not set, warn the user that persistence requires these env vars
- If any step fails, report the error but don't lose the generated code — the user can retry persistence