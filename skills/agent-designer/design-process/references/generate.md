# Phase 5: GENERATE

## Goal
Produce a complete, runnable Python agent file with all imports, configuration, and setup instructions.

## What to Produce

### Agent Python File
- All imports (verified against Agno docs)
- Database/storage configuration
- Knowledge base configuration
- Tool instantiation (with `cache_results=True` where appropriate)
- System prompt (concise — details live in skill files, not the prompt)
- Agent constructor with all parameters
- `if __name__ == "__main__"` block for standalone testing

### Setup Instructions
- pip/uv install commands for all dependencies
- Required environment variables with descriptions
- Any one-time setup steps (creating directories, pulling Ollama models, etc.)

### Inline Comments
- Explain key design choices in comments
- Note why specific tools, storage, or knowledge configurations were chosen
- Flag any non-obvious tradeoffs

## Run Command
- `agno serve agent_name.py:agent_var` for AgentOS deployment
- `python agent_name.py` for standalone testing

## Tips
- Generate COMPLETE code — not fragments. The file must run as-is.
- Verify all import paths against Agno docs before writing.
- Verify all constructor parameters against Agno docs before writing.
- Use `cache_results=True` on Toolkits where results are deterministic or expensive.
- Keep system prompts focused — load skills for detailed guidance, don't inline everything.