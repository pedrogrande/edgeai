# Agno features

| Feature | Usage | Link |
| :---- | :---- | :---- |
| **Agents** | Agents are AI programs that use tools to accomplish tasks. | [https://docs.agno.com/agents/overview](https://docs.agno.com/agents/overview)  |
| Follow up suggestions | Generate actionable followup prompts after every agent response. | [https://docs.agno.com/agents/usage/agent-with-followup-suggestions](https://docs.agno.com/agents/usage/agent-with-followup-suggestions)  [https://docs.agno.com/teams/usage/team-with-followup-suggestions](https://docs.agno.com/teams/usage/team-with-followup-suggestions)  |
| **Teams** | Groups of agents that collaborate to solve complex tasks. | [https://docs.agno.com/teams/overview](https://docs.agno.com/teams/overview)  |
| **Workflows** | Workflows orchestrate agents, teams, and functions through defined steps for repeatable tasks. | [https://docs.agno.com/workflows/overview](https://docs.agno.com/workflows/overview)  |
| Conversational workflows | Build multi-turn conversational workflows in Agno. | [https://docs.agno.com/workflows/conversational-workflows](https://docs.agno.com/workflows/conversational-workflows)  |
| **Models** | Language Models are machine-learning programs that are trained to understand natural language and code. | [https://docs.agno.com/models/overview](https://docs.agno.com/models/overview)  [https://docs.agno.com/models/fallback-models](https://docs.agno.com/models/fallback-models)  |
| **Input / Output** | Learn how to pass data to agents and handle their responses. |  |
| Typed Input & Output | Defined inputs and outputs using [Pydantic](https://pydantic.dev/) | [https://docs.agno.com/input-output/overview](https://docs.agno.com/input-output/overview)  |
| Multi-modal I/O | Upload and download files, images, audio, video | [https://docs.agno.com/input-output/multimodal](https://docs.agno.com/input-output/multimodal)  |
| Custom Output | Style output documents or use multiple models to create designed output | [https://docs.agno.com/input-output/output-model](https://docs.agno.com/input-output/output-model)  |
| **Database** | Give your agents persistent storage for sessions, context, memory and knowledge. | [https://docs.agno.com/database/overview](https://docs.agno.com/database/overview)  |
| Chat history | Enables multi-turn conversations. If previous messages should be included in every request. | [https://docs.agno.com/database/chat-history](https://docs.agno.com/database/chat-history)  `add_history_to_context=True, num_history_runs=3,  # Include last 3 turns num_history_messages=20,  # Cap at 20 messages total` [https://docs.agno.com/history/overview](https://docs.agno.com/history/overview)  |
| Sessions storage | Store and retrieve agent sessions from your database. | [https://docs.agno.com/database/session-storage](https://docs.agno.com/database/session-storage)  `session_table="my_agent_sessions"`  |
| Memory | Give your agents the ability to remember user preferences, context, and past interactions for truly personalized experiences. [Memory manager](https://docs.agno.com/memory/working-with-memories/overview) add\_memories\_to\_context  | [https://docs.agno.com/memory/overview](https://docs.agno.com/memory/overview)  `update_memory_on_run=True memory_table="my_memory_table"`  |
| Memory tools | Instead of automatic memory management, you can give your agent explicit tools to create, retrieve, update, and delete memories. This approach gives the agent more control and reasoning ability, so it can decide when to store something versus when to search for existing memories. | [https://docs.agno.com/memory/working-with-memories/overview\#using-memory-tools](https://docs.agno.com/memory/working-with-memories/overview#using-memory-tools)  |
| Memory optimisation | As users accumulate memories over time, and these memories are added to your context on each request, token costs can grow significantly. Memory optimization helps reduce these costs by combining multiple memories into fewer, more efficient memories while preserving all the key information. | [https://docs.agno.com/memory/working-with-memories/memory-optimization](https://docs.agno.com/memory/working-with-memories/memory-optimization)  |
| Memory best practices | Avoid common pitfalls, optimize costs, and ensure reliable memory behavior in production.  | [https://docs.agno.com/memory/best-practices](https://docs.agno.com/memory/best-practices)  |
| Knowledge | Give agents access to documents, databases, and domain expertise. | [https://docs.agno.com/knowledge/overview](https://docs.agno.com/knowledge/overview)  |
| Chunking | Split documents into smaller pieces for effective vector search. | [https://docs.agno.com/knowledge/concepts/chunking/overview](https://docs.agno.com/knowledge/concepts/chunking/overview)  |
| Knowledge search | How agents search knowledge bases to find relevant information. | [https://docs.agno.com/knowledge/concepts/search-and-retrieval/overview](https://docs.agno.com/knowledge/concepts/search-and-retrieval/overview)  |
| Agentic RAG with Reranking | Combine agentic search, hybrid retrieval, and reranking for high-quality responses | [https://docs.agno.com/knowledge/concepts/search-and-retrieval/agentic-rag](https://docs.agno.com/knowledge/concepts/search-and-retrieval/agentic-rag)  |
| Filtering | Filter knowledge searches by metadata for precise retrieval. | [https://docs.agno.com/knowledge/concepts/filters/overview](https://docs.agno.com/knowledge/concepts/filters/overview)  |
| Learning | Agents that learn and improve with every interaction. | [https://docs.agno.com/learning/overview](https://docs.agno.com/learning/overview)  |
| Learning stores | Each store captures a different type of knowledge. | [https://docs.agno.com/learning/stores/intro](https://docs.agno.com/learning/stores/intro)  |
| **Tools** | Tools are functions Agents call to interact with external systems. | [https://docs.agno.com/tools/overview](https://docs.agno.com/tools/overview)  |
| MCP | MCPTools | [https://docs.agno.com/tools/mcp/overview](https://docs.agno.com/tools/mcp/overview)  |
| Custom tools | Write custom tool functions and use the @tool decorator to modify tool behavior. | [https://docs.agno.com/tools/creating-tools/overview](https://docs.agno.com/tools/creating-tools/overview)  |
| MCP Toolbox for databases | Google tool: [https://github.com/googleapis/mcp-toolbox](https://github.com/googleapis/mcp-toolbox)  | [https://docs.agno.com/tools/mcp/mcp-toolbox](https://docs.agno.com/tools/mcp/mcp-toolbox)  |
| Multiple MCP servers | Understanding how to connect to multiple MCP servers with Agno | [https://docs.agno.com/tools/mcp/multiple-servers](https://docs.agno.com/tools/mcp/multiple-servers)  |
| Dynamic headers | Setting dynamic headers with Agno MCP tools | [https://docs.agno.com/tools/mcp/dynamic-headers](https://docs.agno.com/tools/mcp/dynamic-headers)  |
| Github MCP agent | [https://github.com/github/github-mcp-server](https://github.com/github/github-mcp-server)  | [https://docs.agno.com/tools/mcp/usage/github](https://docs.agno.com/tools/mcp/usage/github)  |
| Reasoning | The ReasoningTools toolkit allows an Agent to use reasoning like any other tool, at any point during execution. | [https://docs.agno.com/tools/reasoning\_tools/reasoning-tools](https://docs.agno.com/tools/reasoning_tools/reasoning-tools)  |
| Tool call limit | Limit the number of tool calls an agent can make. | [https://docs.agno.com/tools/tool-call-limit](https://docs.agno.com/tools/tool-call-limit)  |
| Tool result caching | Cache tool results to reduce repeated API calls and improve performance. | [https://docs.agno.com/tools/caching](https://docs.agno.com/tools/caching)  |
| Toolkits | Index of all toolkits supported by Agno. | [https://docs.agno.com/tools/toolkits/overview](https://docs.agno.com/tools/toolkits/overview)  |
| Web search | Search results | [https://docs.agno.com/tools/toolkits/search/websearch](https://docs.agno.com/tools/toolkits/search/websearch)  |
| Telegram | Chat tools | [https://docs.agno.com/tools/toolkits/social/telegram](https://docs.agno.com/tools/toolkits/social/telegram)  [https://docs.agno.com/agent-os/interfaces/telegram/introduction](https://docs.agno.com/agent-os/interfaces/telegram/introduction)  |
| Email | Read and Send emails and manage inbox | [https://docs.agno.com/tools/toolkits/social/email](https://docs.agno.com/tools/toolkits/social/email)  |
| Webscrape | Needed for agents to read web pages | [https://docs.agno.com/tools/toolkits/web-scrape/website](https://docs.agno.com/tools/toolkits/web-scrape/website)  |
| Data tools | CSV | [https://docs.agno.com/tools/toolkits/database/csv](https://docs.agno.com/tools/toolkits/database/csv)  |
|  | SQL | [https://docs.agno.com/tools/toolkits/database/duckdb](https://docs.agno.com/tools/toolkits/database/duckdb)  |
|  | Postgresql | [https://docs.agno.com/tools/toolkits/database/postgres](https://docs.agno.com/tools/toolkits/database/postgres)  |
| Local tools | Docker | [https://docs.agno.com/tools/toolkits/local/docker](https://docs.agno.com/tools/toolkits/local/docker)  |
|  | File read & write | [https://docs.agno.com/tools/toolkits/local/file](https://docs.agno.com/tools/toolkits/local/file)  |
|  | Local file system | [https://docs.agno.com/tools/toolkits/local/local-file-system](https://docs.agno.com/tools/toolkits/local/local-file-system)  |
|  | Python | [https://docs.agno.com/tools/toolkits/local/python](https://docs.agno.com/tools/toolkits/local/python)  |
|  | Shell | [https://docs.agno.com/tools/toolkits/local/shell](https://docs.agno.com/tools/toolkits/local/shell)  |
|  | Sleep | [https://docs.agno.com/tools/toolkits/local/sleep](https://docs.agno.com/tools/toolkits/local/sleep)  |
| File generation | Create files | [https://docs.agno.com/tools/toolkits/file-generation/file-generation](https://docs.agno.com/tools/toolkits/file-generation/file-generation)  |
| Text to image  | Nebius integration | [https://docs.agno.com/tools/toolkits/models/nebius](https://docs.agno.com/tools/toolkits/models/nebius)  |
| Workflow | Airflow by Apache [https://airflow.apache.org/](https://airflow.apache.org/)  | [https://docs.agno.com/tools/toolkits/others/airflow](https://docs.agno.com/tools/toolkits/others/airflow)  |
|  | APIfy [https://apify.com/actors](https://apify.com/actors)  | [https://docs.agno.com/tools/toolkits/others/apify](https://docs.agno.com/tools/toolkits/others/apify)  |
| Custom API | Add any API tools  | [https://docs.agno.com/tools/toolkits/others/custom-api](https://docs.agno.com/tools/toolkits/others/custom-api)  |
| File conversion | Docling [https://www.docling.ai/](https://www.docling.ai/)  | [https://docs.agno.com/tools/toolkits/others/docling](https://docs.agno.com/tools/toolkits/others/docling)  |
| Ethereum EVM | EvmTools enables agents to interact with Ethereum and EVM-compatible blockchains for transactions and smart contract operations. | [https://docs.agno.com/tools/toolkits/others/evm](https://docs.agno.com/tools/toolkits/others/evm)  [https://docs.agno.com/examples/tools/evm-tools](https://docs.agno.com/examples/tools/evm-tools)  |
| Knowledge tools | provide intelligent search and analysis capabilities over knowledge bases with reasoning integration | [https://docs.agno.com/tools/toolkits/others/knowledge](https://docs.agno.com/tools/toolkits/others/knowledge)  |
| Linear | Needs API key | [https://docs.agno.com/tools/toolkits/others/linear](https://docs.agno.com/tools/toolkits/others/linear)  |
| Reasoning | Reasoning gives Agents the ability to “think” before responding and “analyze” the results of their actions (i.e. tool calls), greatly improving the Agents’ ability to solve problems that require sequential tool calls. | [https://docs.agno.com/tools/toolkits/others/reasoning](https://docs.agno.com/tools/toolkits/others/reasoning)  [https://docs.agno.com/reasoning/overview](https://docs.agno.com/reasoning/overview)  |
| Resend | Email sending | [https://docs.agno.com/tools/toolkits/others/resend](https://docs.agno.com/tools/toolkits/others/resend)  |
| Scheduler | Let agents create and manage recurring schedules through natural language. | [https://docs.agno.com/tools/toolkits/others/scheduler](https://docs.agno.com/tools/toolkits/others/scheduler)  [https://docs.agno.com/scheduler/overview](https://docs.agno.com/scheduler/overview)  |
| User control flow | enable agents to pause execution and request input from users during conversations | [https://docs.agno.com/tools/toolkits/others/user-control-flow](https://docs.agno.com/tools/toolkits/others/user-control-flow)  |
| Visualization | enables agents to create various types of charts and plots using matplotlib | [https://docs.agno.com/tools/toolkits/others/visualization](https://docs.agno.com/tools/toolkits/others/visualization)  |
| Web browser tools | Enables agent to open URL in a browser | [https://docs.agno.com/tools/toolkits/others/web-browser](https://docs.agno.com/tools/toolkits/others/web-browser)  |
| Session management | Multi-turn conversation threads with persistent history and state. | [https://docs.agno.com/sessions/overview](https://docs.agno.com/sessions/overview)  |
| Metrics | Token usage, cost, timing, and per-model breakdowns for agents, teams, and workflows. | [https://docs.agno.com/sessions/metrics/overview](https://docs.agno.com/sessions/metrics/overview)  |
| Context management | Design and control the information sent to language models to guide their behavior. | [https://docs.agno.com/context/overview](https://docs.agno.com/context/overview)  [https://docs.agno.com/compression/overview](https://docs.agno.com/compression/overview)  |
| State management | Persist and share data across agent runs, team coordination, and workflow execution | [https://docs.agno.com/state/overview](https://docs.agno.com/state/overview)  |
| Token counting | Token estimation for context planning and compression. | [https://docs.agno.com/compression/token-counting](https://docs.agno.com/compression/token-counting)  |
| Dependency injection | Inject variables into agent and team context with dependencies | [https://docs.agno.com/dependencies/overview](https://docs.agno.com/dependencies/overview)  |
| Hooks | Execute custom logic before and after agent runs with hooks | [https://docs.agno.com/hooks/overview](https://docs.agno.com/hooks/overview)  |
| Run cancellation | Cancel running agent, team, or workflow executions. | [https://docs.agno.com/run-cancellation/overview](https://docs.agno.com/run-cancellation/overview)  |
| Skills | Skills provide agents with structured domain expertise through instructions, scripts, and reference documentation. | [https://docs.agno.com/skills/overview](https://docs.agno.com/skills/overview)  |
| Guardrails | Built-in safeguards for input validation, PII detection, and prompt injection defense. | [https://docs.agno.com/guardrails/overview](https://docs.agno.com/guardrails/overview)  |
| Human-in-the-loop | Control agent execution flow with human oversight and input. | [https://docs.agno.com/hitl/overview](https://docs.agno.com/hitl/overview)  |
| Evals | Evals is a way to measure the quality of your Agents and Teams. | [https://docs.agno.com/evals/overview](https://docs.agno.com/evals/overview)  |
| Tracing | Gain deep visibility into your Agno agents with OpenTelemetry-based observability  | [https://docs.agno.com/tracing/overview](https://docs.agno.com/tracing/overview)  |
| Supported databases | Index of all databases supported by Agno | [https://docs.agno.com/database/providers/overview](https://docs.agno.com/database/providers/overview)  |
| Vector stores | Index of all vector stores supported by Agno | [https://docs.agno.com/knowledge/vector-stores/index](https://docs.agno.com/knowledge/vector-stores/index)  |
| Embedders | Convert text into vector representations for semantic search. | [https://docs.agno.com/knowledge/concepts/embedder/overview](https://docs.agno.com/knowledge/concepts/embedder/overview)  |
| Culture | Experimental feature: Enable your agents to share universal knowledge, principles, and best practices that compound across all interactions. | [https://docs.agno.com/culture/overview](https://docs.agno.com/culture/overview)  |
| Custom logging | Configure custom loggers and formatters for your Agno setup. | [https://docs.agno.com/custom-logging](https://docs.agno.com/custom-logging)  |
| Observability | Agno supports observability through OpenTelemetry, integrating seamlessly with popular tracing and monitoring platforms | [https://docs.agno.com/observability/overview](https://docs.agno.com/observability/overview)  |
| Governance | Cryptographically verifiable audit trails | [https://docs.agno.com/integrations/governance/agentsystems-notary](https://docs.agno.com/integrations/governance/agentsystems-notary)  |
| Custom FastAPI app | Integrate your own FastAPI app with AgentOS. AgentOS is built on FastAPI, which means you can easily integrate your existing FastAPI applications or add custom routes and routers to extend your agent’s capabilities. | [https://docs.agno.com/agent-os/custom-fastapi/overview](https://docs.agno.com/agent-os/custom-fastapi/overview)  |
| AgentOS as MCP server | Learn how and why to expose your AgentOS as an MCP server | [https://docs.agno.com/agent-os/mcp/mcp](https://docs.agno.com/agent-os/mcp/mcp)  |
| AgentOS Middleware | Add authentication, logging, monitoring, and security features to your AgentOS application using middleware | [https://docs.agno.com/agent-os/middleware/overview](https://docs.agno.com/agent-os/middleware/overview)  |
| Approvals | Manage approval workflows for agents and teams via the AgentOS Control Panel | [https://docs.agno.com/agent-os/approvals/overview](https://docs.agno.com/agent-os/approvals/overview)  |
| A2A client | Connect to any A2A-compatible agent server | [https://docs.agno.com/agent-os/client/a2a-client](https://docs.agno.com/agent-os/client/a2a-client)  |
| AgentOS security | Secure your AgentOS with authentication and authorization. | [https://docs.agno.com/agent-os/security/overview](https://docs.agno.com/agent-os/security/overview)  |

