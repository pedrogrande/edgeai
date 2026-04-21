# Agno Knowledge Base Strategy
## For: DAO Documentation Database (Non-Technical User File Ingestion)

---

## Executive Summary

Agno's Knowledge system has **8 major feature dimensions** that need decisions. This document maps each dimension to your use case (non-technical users adding markdown + PDF files to a documentation knowledge base), explains the trade-offs, and recommends a phased implementation strategy.

---

## The 8 Decision Dimensions

| # | Dimension | What It Controls | Your Key Question |
|---|-----------|-----------------|-------------------|
| 1 | **Knowledge Store Architecture** | Single vs. multiple Knowledge instances | Do we need separate stores per domain or one unified store? |
| 2 | **Vector Database** | Where embeddings are stored & searched | Local dev vs. production, scale requirements? |
| 3 | **Embedder** | How text becomes vectors | Local/free (Ollama) vs. hosted ($) vs. quality trade-off? |
| 4 | **Chunking Strategy** | How documents are split | By heading? By semantic meaning? Fixed size? Per content type? |
| 5 | **Readers** | How files are parsed | Auto-detect vs. explicit? PDF options (OCR, page splitting)? |
| 6 | **Search & Retrieval** | How agents find information | Vector, keyword, hybrid? Reranking? Agentic vs. traditional RAG? |
| 7 | **Metadata & Filtering** | How results are scoped | What metadata schema? Manual vs. agentic filtering? |
| 8 | **Contents Database** | Content tracking & management | Do we need visibility, management, and the AgentOS Knowledge UI? |

---

## Dimension 1: Knowledge Store Architecture

### What Agno Offers

Agno's `Knowledge` class is the central object. You can create:
- **One Knowledge instance** — all content in one searchable pool
- **Multiple Knowledge instances** — separate pools, can share or isolate their vector DB

**Isolation feature**: `isolate_vector_search=True` on a Knowledge instance automatically tags inserted documents with a `linked_to` field matching the instance name, and filters by it during search. This lets multiple Knowledge instances share the same vector DB table while keeping searches scoped.

### When to Use Separate Stores

| Pattern | When | How |
|---------|------|-----|
| **Single store, no isolation** | One domain, one agent, simple case | `Knowledge(vector_db=...)` |
| **Single vector DB, isolated instances** | Multiple domains, shared infrastructure, scoped retrieval | `Knowledge(name="hr-docs", vector_db=shared_db, isolate_vector_search=True)` |
| **Separate vector DBs** | Completely different data, different embedders, different access patterns | Each Knowledge gets its own vector_db |

### 🎯 Recommendation for Your Use Case

**Start with a single Knowledge instance with `isolate_vector_search=True`**, named by domain. This gives you:

- **Shared infrastructure** — one PostgreSQL + PgVector deployment
- **Scoped retrieval** — an "agno-docs" agent only searches agno docs, not DAO governance docs
- **Future flexibility** — easy to split to separate DBs later if scale demands it

Example:
```python
agno_knowledge = Knowledge(
    name="agno-docs",              # Used as linked_to filter key
    vector_db=PgVector(table_name="shared_vectors", db_url=db_url),
    isolate_vector_search=True,    # Searches only return this instance's docs
)
```

**Key constraint**: Each Knowledge instance needs a unique `name` if sharing the same contents_db + table. Two instances with the same name on the same table will throw a `ValueError`.

---

## Dimension 2: Vector Database

### What Agno Supports (20+)

| Category | Options | Best For |
|----------|---------|----------|
| **Local/Dev** | LanceDB, ChromaDB | Zero-setup development, file-based |
| **Production SQL** | PgVector | Up to ~1M docs, leverages PostgreSQL |
| **Managed** | Pinecone, Weaviate Cloud | No-ops, auto-scaling |
| **High Performance** | Qdrant, Milvus | Large-scale, high-throughput |
| **Hybrid/Multi-model** | Weaviate, SurrealDB, ClickHouse | Complex query needs |

### Hybrid Search Support

Hybrid search (vector + keyword) is critical for documentation where users search by concept AND by exact term (e.g., "how does `isolate_vector_search` work?"). Supported on:

- PgVector ✅
- ChromaDB ✅
- LanceDB ✅
- Weaviate ✅
- Milvus ✅
- Pinecone ✅

### 🎯 Recommendation for Your Use Case

| Environment | Database | Why |
|-------------|----------|-----|
| **Development** | LanceDB | Zero setup, file-based, supports hybrid search |
| **Production** | PgVector | You likely already need PostgreSQL for the Contents DB; reuse it for vectors. Hybrid search support. Proven at ~1M doc scale. |

```python
# Development
vector_db = LanceDb(uri="./local_db", table_name="docs")

# Production
vector_db = PgVector(
    table_name="dao_docs",
    db_url="postgresql+psycopg://user:pass@localhost:5532/db",
    search_type=SearchType.hybrid,  # Combine vector + keyword
)
```

---

## Dimension 3: Embedder

### What Agno Supports

| Embedder | Type | Cost | Notes |
|----------|------|------|-------|
| **OpenAI** | Hosted | $$ | Default, excellent quality, `text-embedding-3-small` (1536d) or `text-embedding-3-large` (3072d) |
| **Gemini** | Hosted | $$ | Multilingual, Google ecosystem |
| **Cohere** | Hosted | $$ | Strong retrieval, `embed-v4.0` |
| **Voyage AI** | Hosted | $$$ | Best retrieval quality |
| **Mistral** | Hosted | $$ | European provider |
| **Ollama** | Local | Free | Privacy, offline, uses local models |
| **FastEmbed** | Local | Free | Fast local embeddings via ONNX |
| **HuggingFace** | Local/Hosted | Free/$ | Open source models |
| **AWS Bedrock** | Hosted | $$ | AWS ecosystem |
| **Azure OpenAI** | Hosted | $$ | Azure ecosystem |

### Key Considerations

1. **Embedders are NOT interchangeable** — vectors from different embedders aren't compatible. Switching embedders means re-embedding everything.
2. **Dimensions must match** — your embedder's output dimensions must match what your vector DB expects.
3. **Batch embedding** — supported on OpenAI, Gemini, Cohere, Voyage, Mistral, and others. Significantly faster for bulk ingestion.
4. **Ollama embedder** — uses `OllamaEmbedder()` from `agno.knowledge.embedder.ollama`. No API key needed, but you need Ollama running locally with a model pulled.

### 🎯 Recommendation for Your Use Case

| Scenario | Embedder | Why |
|----------|----------|-----|
| **Cost-sensitive / Privacy-first** | `OllamaEmbedder()` | Free, local, no API keys. Good enough for documentation retrieval. |
| **Best retrieval quality** | `OpenAIEmbedder(id="text-embedding-3-small")` | Proven quality for docs, reasonable cost |
| **Maximum quality** | `VoyageAI` or `CohereEmbedder` | Specialized for retrieval tasks |

```python
# Local/Free option (recommended if you're already using Ollama for agents)
from agno.knowledge.embedder.ollama import OllamaEmbedder
embedder = OllamaEmbedder()

# Hosted quality option
from agno.knowledge.embedder.openai import OpenAIEmbedder
embedder = OpenAIEmbedder(id="text-embedding-3-small", dimensions=1536)
```

**⚠️ Critical**: Pick ONE embedder and stick with it. Changing means re-indexing everything.

---

## Dimension 4: Chunking Strategy

### What Agno Offers

| Strategy | Import | How It Works | Best For |
|----------|--------|-------------|----------|
| **Fixed Size** | `FixedSizeChunking` | Splits by character count with optional overlap | Uniform content, predictability |
| **Semantic** | `SemanticChunking` | Splits at natural topic boundaries (uses embeddings) | Complex documents, preserving meaning |
| **Recursive** | `RecursiveChunking` | Multiple separators hierarchically | Mixed content, structured docs |
| **Document** | `DocumentChunking` | Preserves document structure (paragraphs, sections) | Structured PDFs, reports |
| **Markdown** | `MarkdownChunking` | Splits by heading structure | **Markdown files** ← your primary content |
| **CSV Row** | `CSVRowChunking` | Each row = one chunk | Tabular data |
| **Code** | `CodeChunking` | Splits at function/class boundaries (AST) | Source code |
| **Agentic** | `AgenticChunking` | AI determines optimal boundaries | Experimental, when other strategies fail |
| **Custom** | Build your own | Implement custom logic | Domain-specific needs |

### Chunk Size Trade-offs

| Size | Precision | Context | Best For |
|------|-----------|---------|----------|
| Small (1000-3000 chars) | 🔺 High | 🔻 Low | Specific factual questions |
| Default (5000 chars) | 🟡 Balanced | 🟡 Balanced | General use |
| Large (8000+ chars) | 🔻 Low | 🔺 High | When surrounding context matters |

### Per-Content-Type Strategy

This is where it gets interesting for your use case. **Different file types should use different chunking strategies:**

| Content Type | Recommended Strategy | Why |
|-------------|---------------------|-----|
| **Markdown** | `MarkdownChunking` | Respects heading structure — keeps sections together |
| **PDF** | `DocumentChunking` or `SemanticChunking` | PDFs lack explicit structure; semantic chunking preserves meaning |
| **Mixed** | `RecursiveChunking` | Handles multiple separator types gracefully |

### How to Apply Per-Type Chunking

Pass a custom reader with its chunking strategy to `knowledge.insert()`:

```python
from agno.knowledge.chunking.markdown import MarkdownChunking
from agno.knowledge.chunking.semantic import SemanticChunking
from agno.knowledge.chunking.document import DocumentChunking
from agno.knowledge.reader.markdown_reader import MarkdownReader
from agno.knowledge.reader.pdf_reader import PDFReader

# Markdown files — respect heading structure
knowledge.insert(
    path="docs/agno/",
    reader=MarkdownReader(chunking_strategy=MarkdownChunking()),
)

# PDF files — preserve document structure
knowledge.insert(
    path="docs/pdfs/",
    reader=PDFReader(chunking_strategy=DocumentChunking()),
)
```

### 🎯 Recommendation for Your Use Case

**Use different chunking strategies per content type:**
- **Markdown → MarkdownChunking** (your primary content is markdown, this keeps heading-based sections intact)
- **PDF → DocumentChunking** (preserves paragraph/section structure)
- **If PDF quality is poor → SemanticChunking** (uses embeddings to find topic boundaries, but slower and requires an embedder)

**Default chunk size**: Start at 5000 (default). If search results feel too broad, try 3000 with 200 overlap.

---

## Dimension 5: Readers

### What Agno Offers

| Reader | Import | Handles |
|--------|--------|---------|
| **PDFReader** | `agno.knowledge.reader.pdf_reader.PDFReader` | `.pdf` files, OCR, encrypted PDFs, page splitting |
| **MarkdownReader** | `agno.knowledge.reader.markdown_reader.MarkdownReader` | `.md` files |
| **CSVReader** | `agno.knowledge.reader.csv_reader.CSVReader` | `.csv` files |
| **JSONReader** | `agno.knowledge.reader.json_reader.JSONReader` | `.json` files |
| **TextReader** | `agno.knowledge.reader.text_reader.TextReader` | `.txt` files |
| **DoclingReader** | `agno.knowledge.reader.docling_reader.DoclingReader` | Multi-format via Docling |
| **WebsiteReader** | `agno.knowledge.reader.website_reader.WebsiteReader` | Web crawling |
| **YouTubeReader** | `agno.knowledge.reader.youtube_reader.YouTubeReader` | YouTube transcripts |

### Auto-Detection

Agno auto-selects the right reader based on file extension via `ReaderFactory`. When you call `knowledge.insert(path="file.pdf")`, it uses PDFReader automatically. **You only need to specify a reader when you want custom options.**

### Key Reader Options

```python
# PDF with advanced options
PDFReader(
    password="secret",          # Encrypted PDFs
    read_images=True,           # OCR for image-based PDFs
    split_on_pages=True,        # Each page = one document
    chunk_size=3000,            # Override chunk size
    chunking_strategy=SemanticChunking(),  # Override chunking strategy
)

# Markdown with custom chunking
MarkdownReader(
    chunking_strategy=MarkdownChunking(),
)
```

### 🎯 Recommendation for Your Use Case

**Rely on auto-detection for the happy path** (it works for `.md`, `.pdf`, `.csv`, `.json`, etc.). Override with explicit readers only when:

1. **PDFs need OCR** — `PDFReader(read_images=True)`
2. **PDFs are encrypted** — `PDFReader(password="...")`
3. **You want per-type chunking** — pass the reader with its chunking strategy

For your non-technical users, the UX should be: **"Drop a file, we handle the rest."** Auto-detection + sensible defaults makes this possible.

---

## Dimension 6: Search & Retrieval

### Three Search Types

| Type | `SearchType` | How It Works | Best For |
|------|-------------|-------------|----------|
| **Vector** | `SearchType.vector` | Matches by semantic meaning | Conceptual questions, paraphrased queries |
| **Keyword** | `SearchType.keyword` | Matches exact words/phrases | Product names, error codes, identifiers |
| **Hybrid** | `SearchType.hybrid` | Combines both via Reciprocal Rank Fusion | **Most real-world use cases** |

### RAG Modes

| Mode | How It Works | When to Use |
|------|-------------|-------------|
| **Agentic RAG** (default) | Agent decides when to search, can reformulate queries, run multiple searches | Most cases — agent is smarter about when/how to search |
| **Traditional RAG** | Always searches, always injects context into prompt | When you need guaranteed grounding in docs |

### Reranking

After hybrid search returns results, a reranker (like Cohere Reranker) re-scores them for relevance. This significantly improves result quality.

```python
from agno.knowledge.reranker.cohere import CohereReranker

vector_db = PgVector(
    table_name="docs",
    db_url=db_url,
    search_type=SearchType.hybrid,
    reranker=CohereReranker(model="rerank-v3.5", top_n=10),
)
```

### Custom Retrievers

For advanced use cases, you can implement your own retrieval logic:

```python
def knowledge_retriever(query: str, num_documents: int = 5, **kwargs) -> list[dict]:
    # Multi-source search
    agno_results = agno_knowledge.search(query, max_results=3)
    dao_results = dao_knowledge.search(query, max_results=3)
    # Combine and deduplicate
    ...
```

### 🎯 Recommendation for Your Use Case

| Feature | Recommendation | Why |
|---------|---------------|-----|
| **Search type** | `SearchType.hybrid` | Documentation has both conceptual content AND specific API names/identifiers |
| **RAG mode** | Agentic RAG (`search_knowledge=True`) | Let the agent decide when to search — it's smarter |
| **Reranking** | Start without, add Cohere Reranker if quality is insufficient | Reranking adds cost and latency; see if you need it first |
| **max_results** | Start at 5, increase to 10 if context is too narrow | Balance between relevance and prompt size |

---

## Dimension 7: Metadata & Filtering

### Why Metadata Matters (This Is HUGE for Your Use Case)

You said: *"thorough metadata, tags and descriptions can really help agents find the right information more quickly."* — This is exactly right. Metadata enables:

1. **Precision** — filter to only "agno-docs" type documents when asking about Agno
2. **Access control** — filter by `access_level: "public"` vs `"internal"`
3. **Temporal queries** — filter by `year: 2025` for latest versions
4. **Agentic filtering** — the agent automatically infers filters from natural language queries

### Metadata Schema Design

```python
# When inserting content, attach rich metadata
knowledge.insert(
    name="Agno Agent Building Guide",
    path="docs/agno/building-agents.md",
    metadata={
        "domain": "agno",              # Knowledge domain
        "category": "agents",          # Sub-category
        "content_type": "guide",        # guide, reference, tutorial, api-doc
        "version": "2.0",              # Agno version
        "tags": ["agent", "rag", "knowledge"],  # Tags for filtering
        "last_updated": "2025-01-15",  # Temporal filtering
        "access_level": "public",      # Access control
        "source_url": "https://docs.agno.com/agents/building-agents",
    }
)
```

### Two Filtering Approaches

| Approach | How | When |
|----------|-----|------|
| **Manual** | `knowledge_filters={"domain": "agno"}` on agent or per-query | Automation, predictable filters, full control |
| **Agentic** | `enable_agentic_knowledge_filters=True` on agent | User-facing apps, natural language queries |

**Agentic filtering requires a Contents DB** — the agent needs to know what filter keys/values exist to infer the right filters.

### 🎯 Recommendation for Your Use Case

1. **Define a metadata schema** (see above) and enforce it during ingestion
2. **Start with manual filtering** — your agents know their domain, they can hardcode `knowledge_filters={"domain": "agno"}`
3. **Add agentic filtering** when you expose to non-technical users who ask natural language questions
4. **The metadata schema is your most important design decision** — it determines how useful filtering will be

---

## Dimension 8: Contents Database

### What It Does

The Contents DB is an **optional** component that stores metadata about what you've added. Without it, you can search but can't see or manage what's in the knowledge base.

| Feature | Without Contents DB | With Contents DB |
|---------|--------------------|--------------------|
| Search | ✅ Yes | ✅ Yes |
| See what's in KB | ❌ No | ✅ Content browser |
| Delete specific content | ❌ No (must rebuild) | ✅ Auto-cleanup of vectors |
| Edit metadata | ❌ No | ✅ Update without re-indexing |
| Track processing status | ❌ No | ✅ Real-time status |
| Agentic filtering | ❌ No | ✅ Required |
| AgentOS Knowledge UI | ❌ No | ✅ Required |

### Supported Backends

| Backend | Import | Best For |
|---------|--------|----------|
| **PostgreSQL** | `PostgresDb` | Production (recommended) |
| **SQLite** | `SqliteDb` | Development |
| **MongoDB** | `MongoDb` | If you already use MongoDB |
| **In-Memory** | `InMemoryDb` | Testing only |

### 🎯 Recommendation for Your Use Case

**Use PostgreSQL as both Contents DB and Vector DB (PgVector).** This gives you:

- Single database deployment (PostgreSQL handles both roles)
- Full content management (list, delete, update metadata)
- Agentic filtering support
- AgentOS Knowledge UI support (if you use AgentOS)
- Content status tracking (know if ingestion succeeded or failed)

```python
from agno.db.postgres import PostgresDb
from agno.vectordb.pgvector import PgVector

contents_db = PostgresDb(db_url=db_url, knowledge_table="knowledge_contents")
vector_db = PgVector(table_name="vectors", db_url=db_url)

knowledge = Knowledge(
    name="agno-docs",
    contents_db=contents_db,
    vector_db=vector_db,
    isolate_vector_search=True,
)
```

---

## Phased Implementation Strategy

### Phase 1: Minimum Viable Knowledge Base (Week 1)

**Goal**: Get files into a knowledge base and make them searchable by an agent.

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Vector DB | LanceDB (local file-based) | Zero setup, supports hybrid search |
| Embedder | OllamaEmbedder() | Free, local, no API keys |
| Chunking | Default (auto-detect by reader) | Simplicity — get working first |
| Contents DB | None (skip for now) | Can add later without breaking anything |
| Search | Hybrid + Agentic RAG | Best default for documentation |
| Metadata | Basic: `{"domain": "agno", "filename": "..."}` | Start simple |

```python
from agno.agent import Agent
from agno.knowledge.embedder.ollama import OllamaEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.ollama import Ollama
from agno.vectordb.lancedb import LanceDb, SearchType

knowledge = Knowledge(
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="docs",
        search_type=SearchType.hybrid,
        embedder=OllamaEmbedder(),
    ),
)

# Load content — auto-detects reader by file extension
knowledge.insert(path="docs/markdown/")
knowledge.insert(path="docs/pdfs/")

agent = Agent(
    model=Ollama(id="glm-5.1:cloud"),
    knowledge=knowledge,
    search_knowledge=True,
    markdown=True,
)

agent.print_response("How do I add knowledge to an Agno agent?")
```

### Phase 2: Structured Metadata + Per-Type Chunking (Week 2-3)

**Goal**: Improve retrieval quality through metadata filtering and content-aware chunking.

| Addition | What Changes |
|---------|-------------|
| Metadata schema | Define and enforce domain, category, tags, content_type |
| Markdown chunking | `MarkdownReader(chunking_strategy=MarkdownChunking())` for `.md` files |
| Document chunking | `PDFReader(chunking_strategy=DocumentChunking())` for `.pdf` files |
| Manual filtering | `knowledge_filters={"domain": "agno"}` on agents |
| `skip_if_exists=True` | Don't reprocess files on re-ingestion |

### Phase 3: Production Infrastructure (Week 4+)

**Goal**: Scale to production with proper database, management, and observability.

| Addition | What Changes |
|---------|-------------|
| Vector DB → PgVector | PostgreSQL-based, scales to ~1M docs |
| Contents DB → PostgresDb | Full content management, status tracking |
| `isolate_vector_search=True` | Multiple knowledge domains, shared infrastructure |
| Agentic filtering | `enable_agentic_knowledge_filters=True` for natural language queries |
| Reranker (optional) | Add `CohereReranker()` if search quality needs improvement |
| AgentOS Knowledge UI | Upload interface, content browser, metadata editor |

### Phase 4: Advanced Features (Future)

| Feature | When |
|---------|------|
| Custom retriever (multi-source) | When you need to combine multiple knowledge bases in one search |
| Cloud storage sources (S3, GitHub) | When files live in cloud storage, not local filesystem |
| Semantic chunking | When document structure is poor and default chunking produces bad results |
| Async ingestion | When bulk loading large document sets |
| Learning (agent writes to knowledge) | When agents should save insights they discover |

---

## Decision Summary Checklist

| Decision | Status | Notes |
|----------|--------|-------|
| **Single vs. multiple knowledge stores** | ☐ Decide | Start single, add isolation when needed |
| **Vector DB: dev vs. production** | ☐ Decide | LanceDB (dev) → PgVector (prod) |
| **Embedder: local vs. hosted** | ☐ Decide | Ollama (free) vs OpenAI (quality) — pick ONE and stick with it |
| **Embedder model + dimensions** | ☐ Decide | If Ollama: which model? If OpenAI: `text-embedding-3-small` (1536d)? |
| **Chunking: per content type?** | ☐ Decide | Recommend: Markdown → MarkdownChunking, PDF → DocumentChunking |
| **Chunk size + overlap** | ☐ Decide | Start at 5000 chars default, adjust based on retrieval quality |
| **Search type** | ☐ Decide | Recommend: `SearchType.hybrid` |
| **RAG mode** | ☐ Decide | Recommend: Agentic RAG (default) |
| **Reranker: yes/no?** | ☐ Decide | Start without, add CohereReranker if quality insufficient |
| **Contents DB: yes/no?** | ☐ Decide | Recommend: yes (PostgreSQL) for management + agentic filtering |
| **Metadata schema** | ☐ Design | Most important design decision — determines filtering usefulness |
| **Filtering: manual vs. agentic** | ☐ Decide | Start manual, add agentic for user-facing scenarios |
| **AgentOS Knowledge UI** | ☐ Decide | Requires Contents DB — good for non-technical user file management |
| **Cloud storage sources** | ☐ Decide | S3, GitHub, etc. — only if files aren't local |
| **max_results** | ☐ Decide | Start at 5, increase if needed |

---

## Key Pitfalls to Avoid

| Pitfall | How to Avoid |
|---------|-------------|
| **Switching embedders** | Pick one and commit. Changing means re-embedding everything. |
| **Skipping metadata** | Rich metadata = better filtering = better retrieval. Invest in the schema early. |
| **Ignoring chunk size** | Too large = noisy results. Too small = lost context. Test with real queries. |
| **No Contents DB in production** | Without it, you can't manage content, track status, or use agentic filtering. |
| **Enabling `isolate_vector_search=True` on existing data** | Existing docs won't have `linked_to` metadata and become invisible. Re-index first. |
| **Over-engineering from day one** | Start with Phase 1 defaults, iterate based on retrieval quality feedback. |