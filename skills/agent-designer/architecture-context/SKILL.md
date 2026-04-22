---
name: architecture-context
description: Current EdgeAI infrastructure reference — databases, agents, tools, services, and environment variables. Load when referring to existing infrastructure or making compatibility decisions.
metadata:
  version: "1.0.0"
  author: edgeai
  tags: ["infrastructure", "edgeai", "architecture"]
---

# Architecture Context

Load the full current architecture reference when you need to refer to existing EdgeAI infrastructure:

`get_skill_reference("architecture-context", "current-arch.md")`

## When to Use This Skill
- You need to know which databases are available (PostgreSQL, SQLite, LanceDB, Milvus)
- You need to reference existing agents and their configurations
- You need to check environment variable names
- You need to know what MCP tools are available
- You need to determine if a new agent should share infrastructure or be standalone
- You need to check what tools other agents use

## Key Facts (Always Visible)

| Component | Detail |
|-----------|--------|
| Framework | Agno (`agno[all]`) |
| App server | AgentOS (FastAPI + auto-discovered agents) |
| Primary DB | PostgreSQL with pgvector on port 5533 |
| MCP Toolbox | edgeai-toolbox on port 5001 |
| Default model | `Ollama(id="glm-5.1:cloud")` |
| Default embedder | `OpenAIEmbedder(id="text-embedding-3-small")` |