# Phase 6: VALIDATE

## Goal
Verify the generated agent code is correct, complete, and runnable before persisting.

## Validation Checklist

### Import Paths
- [ ] Every `from agno.X import Y` path exists in Agno
- [ ] No fabricated or outdated module paths
- [ ] All third-party imports have corresponding pip dependencies

### Constructor Parameters
- [ ] Every Agent constructor parameter is valid (check against Agno docs)
- [ ] Tool constructor parameters are correct (check against Agno docs)
- [ ] Knowledge base configuration is correct
- [ ] Storage/DB configuration is correct
- [ ] No deprecated parameters used

### Environment Variables
- [ ] All required env vars are documented in setup instructions
- [ ] Env var names match what the code expects
- [ ] Default values are sensible for local development

### Dependencies
- [ ] All pip dependencies are listed in setup instructions
- [ ] Version constraints are appropriate (not too loose, not too tight)
- [ ] No missing dependencies (check all imports)

### Design Principles
- [ ] System prompt is focused and not overloaded
- [ ] Tools are minimal — only what the use case requires
- [ ] Knowledge base is appropriate for the data type
- [ ] Memory configuration matches the use case
- [ ] `cache_results=True` is set on deterministic tools

### Runability
- [ ] The file can run standalone with `python agent_name.py`
- [ ] The file can serve via `agno serve`
- [ ] No syntax errors or obvious runtime errors
- [ ] Required directories are created in setup or code

## If Validation Fails
- Fix the issue in the generated code
- Re-validate
- If the fix changes the spec, update `spec_changes_since_approval` in session state
- If the change is significant, ask the user to re-approve