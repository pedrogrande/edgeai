# Phase 3: SPECIFY

## Goal
Define every concrete specification for the agent — model, prompt, tools, knowledge, memory, output format, and all template fields.

## Specifications to Define

### Model
- Default: `Ollama(id="glm-5.1:cloud")` — free, private, no API keys needed
- Only change if user explicitly requests a different model
- Embeddings: always `OpenAIEmbedder`, never Ollama

### System Prompt
- Clear, specific instructions
- Role definition + behavioral rules + guardrails
- Keep focused — don't over-prompt
- Structure like linter configs: critical rules top, boundaries bottom, nothing important in middle

### Tools
- Verified import paths from Agno docs
- Constructor parameters verified against docs
- Add `cache_results=True` on Toolkits where results are deterministic or expensive to recompute

### Knowledge
- Appropriate vector DB type for the use case
- Correct embedder (OpenAIEmbedder for embeddings)
- Table name conventions

### Memory
- AgentMemory, UserMemory, or both
- LearningMachine configuration if agentic memory needed

### Storage
- If persistence needed, configure PostgresDb or SqliteDb

### Output Format
- Markdown (default for conversational agents)
- Structured data (JSON/Pydantic) for pipeline agents
- Mixed (depends on context)

### All Other Template Fields
- Guardrails (PII detection, prompt injection defense, content moderation)
- Deployment target (local, Docker, cloud, AgentOS)
- Cost constraints
- Latency requirements
- Human-in-the-loop requirements
- Observability level

## Tips
- For each specification, briefly explain *why* you chose it.
- If there's a tradeoff the user should be aware of, surface it.
- By the end of Phase 3, every template field should have an answer.