# Analogies for Technical Choices

## Memory

> "Memory means the agent remembers things between conversations. Think of it like 
> a notepad the agent keeps. 'No memory' means every conversation starts fresh — 
> like calling a helpline that doesn't keep notes. 'Remember user preferences' 
> means it recalls *your* likes and habits across sessions — like a barista who 
> remembers your usual order. 'Remember organizational knowledge' means the agent 
> builds up a shared knowledge base that *all* users benefit from — like a company 
> wiki that grows over time. 'Both' gives you personal recall plus shared knowledge."

## Storage

> "This is where the agent keeps its conversation history and working data. 'Local 
> file (SQLite)' is like a notebook on your desk — simple, free, works on one 
> machine. 'PostgreSQL' is like a shared filing cabinet — more setup, but anyone 
> on your team can access it and it handles much bigger workloads. 'MongoDB' is 
> like a document box — good for unstructured data like JSON documents. 'Redis' 
> is like short-term memory — blazing fast but primarily for temporary/cached data."

## Model Selection

> "The model is the AI 'brain' the agent uses. 'Ollama' (default) runs on your own 
> machine — free, private, no API keys needed, but needs decent hardware. Cloud 
> models (OpenAI, Claude, Gemini) are faster and often smarter, but cost money per 
> conversation and send data over the internet. For most use cases, Ollama is a 
> great starting point — you can always upgrade to a cloud model later."

## Observability

> "Observability means tracking what the agent does behind the scenes — like a 
> flight data recorder. 'Basic' just prints to your screen — fine for getting 
> started. 'Advanced' gives you a dashboard to debug problems, track costs, and 
> see exactly what the agent did step-by-step — useful in production but requires 
> extra setup and a third-party service (like Langfuse or LangSmith)."

## Vector DB / Knowledge Storage

> "When the agent needs to search through large documents, it uses a 'vector 
> database' — think of it as a smart index that finds information by meaning, 
> not just by exact keyword match. 'LanceDB' runs locally on your machine, free 
> and simple. 'PgVector' uses your existing PostgreSQL database — one less thing 
> to manage. 'Pinecone' and 'Milvus' are cloud services — more powerful for large 
> collections but need API keys and cost money at scale."

## Architecture: Single vs Team vs Workflow

> "A 'Single Agent' is one AI assistant that handles everything — like a general 
> practitioner. A 'Workflow' chains multiple steps in a fixed order — like an 
> assembly line where each station does one thing. A 'Team' has multiple 
> specialists that coordinate dynamically — like a project team where members 
> jump in as needed. Start simple (Single Agent) and only add complexity when 
> the task genuinely needs it."

## Guardrails

> "Guardrails are safety rules for the agent. 'PII detection' means the agent 
> watches for personal info (names, emails, phone numbers) and handles them 
> carefully. 'Prompt injection defense' protects against someone trying to trick 
> the agent with cleverly worded inputs. 'Content moderation' keeps the agent 
> from generating harmful or inappropriate content. Think of guardrails like 
> training wheels — they add safety at the cost of some flexibility."

## Human-in-the-Loop

> "This means the agent pauses and asks for human permission before taking certain 
> actions — like a debit card that requires confirmation for large purchases. 
> 'Yes' means the agent checks with you before *any* action. 'Only for risky 
> actions' means it acts freely for safe things (like searching the web) but asks 
> before potentially consequential things (like sending an email or modifying a 
> database). 'No' means the agent acts fully autonomously — faster but less 
> oversight."

## Tool Result Caching

> "Caching tool results is like keeping a sticky note with the answer to a question 
> you've already looked up. Instead of searching the web or querying a database 
> every time for the same information, the agent checks its sticky notes first. 
> This makes the agent faster and cheaper — especially for tools that call external 
> APIs or do expensive calculations. The tradeoff is that cached results might be 
> slightly stale, so we only cache things that don't change often."