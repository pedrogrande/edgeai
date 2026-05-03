# Agno Local Docs Database — Schema Design & MCP Server

## Analysis

Your requirements break down into three core problems:

1. **Organization** — The Agno docs are scattered across many URLs with overlapping content. You need a structured database that colocates related pages.
2. **Change tracking** — URLs and content change over time. You need version/audit capability.
3. **Agent access** — Agents need to query this database via an MCP server, not raw markdown.

Given your DAO's emphasis on immutable records and transparency, I'm recommending **PostgreSQL** with the **MCP Toolbox for Databases** as the MCP server layer. This gives you:

- ACID transactions (immutability-friendly)
- Full-text search via `tsvector`
- Direct MCP exposure via Google's MCP Toolbox (no custom server code)
- Schema migrations via Agno's built-in `SqliteDb`/`PostgresDb` for agent sessions

---

## Recommended Database Schema

Here's a normalized schema with 5 tables that handles your feature table, colocated links, change tracking, and hierarchical organization:

```sql
-- ============================================================
-- TABLE 1: categories
-- Groups features into top-level sections (Agents, Teams, Tools, etc.)
-- ============================================================
CREATE TABLE categories (
    id              SERIAL PRIMARY KEY,
    slug            VARCHAR(100) UNIQUE NOT NULL,   -- e.g. "agents", "tools", "memory"
    name            VARCHAR(200) NOT NULL,           -- e.g. "Agents", "Tools"
    description     TEXT,                             -- e.g. "AI programs that use tools to accomplish tasks"
    parent_id       INTEGER REFERENCES categories(id), -- for nested subcategories
    sort_order      INTEGER DEFAULT 0,               -- display order within parent
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- TABLE 2: features
-- The core features table — one row per Agno feature/concept
-- ============================================================
CREATE TABLE features (
    id              SERIAL PRIMARY KEY,
    slug            VARCHAR(200) UNIQUE NOT NULL,    -- e.g. "memory-tools", "mcp-toolbox"
    name            VARCHAR(200) NOT NULL,           -- e.g. "Memory tools"
    description     TEXT NOT NULL,                    -- brief description
    category_id     INTEGER NOT NULL REFERENCES categories(id),
    feature_type    VARCHAR(50) NOT NULL              -- 'core', 'subfeature', 'tool', 'integration', 'concept'
                        CHECK (feature_type IN ('core', 'subfeature', 'tool', 'integration', 'concept')),
    is_experimental BOOLEAN DEFAULT FALSE,            -- e.g. Culture is experimental
    sort_order      INTEGER DEFAULT 0,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- TABLE 3: doc_pages
-- One row per documentation URL/page
-- ============================================================
CREATE TABLE doc_pages (
    id              SERIAL PRIMARY KEY,
    feature_id      INTEGER NOT NULL REFERENCES features(id) ON DELETE CASCADE,
    page_type       VARCHAR(50) NOT NULL              -- 'overview', 'usage', 'concept', 'reference', 'example', 'guide', 'faq'
                        CHECK (page_type IN ('overview', 'usage', 'concept', 'reference', 'example', 'guide', 'faq')),
    url             TEXT NOT NULL,                     -- e.g. "https://docs.agno.com/memory/working-with-memories/overview"
    title           VARCHAR(500),                     -- page title extracted from docs
    summary         TEXT,                              -- brief summary of what's on this page
    code_snippet    TEXT,                              -- key code example from the page
    is_current      BOOLEAN DEFAULT TRUE,             -- FALSE if URL has been replaced
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(url, feature_id)
);

-- ============================================================
-- TABLE 4: doc_page_relations
-- Cross-references between pages (related, duplicate, supersedes, etc.)
-- ============================================================
CREATE TABLE doc_page_relations (
    id              SERIAL PRIMARY KEY,
    from_page_id    INTEGER NOT NULL REFERENCES doc_pages(id) ON DELETE CASCADE,
    to_page_id      INTEGER NOT NULL REFERENCES doc_pages(id) ON DELETE CASCADE,
    relation_type   VARCHAR(50) NOT NULL               -- 'related', 'duplicate', 'supersedes', 'colocated', 'prerequisite'
                        CHECK (relation_type IN ('related', 'duplicate', 'supersedes', 'colocated', 'prerequisite')),
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(from_page_id, to_page_id, relation_type)
);

-- ============================================================
-- TABLE 5: changelog
-- Immutable audit log of changes to docs and features
-- ============================================================
CREATE TABLE changelog (
    id              SERIAL PRIMARY KEY,
    entity_type     VARCHAR(50) NOT NULL              -- 'feature', 'category', 'doc_page', 'relation'
                        CHECK (entity_type IN ('feature', 'category', 'doc_page', 'relation')),
    entity_id       INTEGER NOT NULL,                 -- FK to the relevant table
    action          VARCHAR(20) NOT NULL               -- 'created', 'updated', 'deleted', 'url_changed'
                        CHECK (action IN ('created', 'updated', 'deleted', 'url_changed')),
    old_value       JSONB,                             -- previous state (for updates/deletes)
    new_value       JSONB,                             -- new state (for creates/updates)
    change_note     TEXT,                               -- human-readable description of the change
    changed_by      VARCHAR(200),                      -- who/what made the change
    created_at      TIMESTAMPTZ DEFAULT NOW()          -- immutable timestamp
);

-- ============================================================
-- INDEXES for fast agent queries
-- ============================================================
CREATE INDEX idx_features_category ON features(category_id);
CREATE INDEX idx_features_type ON features(feature_type);
CREATE INDEX idx_features_slug ON features(slug);
CREATE INDEX idx_doc_pages_feature ON doc_pages(feature_id);
CREATE INDEX idx_doc_pages_type ON doc_pages(page_type);
CREATE INDEX idx_doc_pages_url ON doc_pages(url);
CREATE INDEX idx_doc_pages_current ON doc_pages(is_current);
CREATE INDEX idx_doc_page_relations_from ON doc_page_relations(from_page_id);
CREATE INDEX idx_doc_page_relations_to ON doc_page_relations(to_page_id);
CREATE INDEX idx_changelog_entity ON changelog(entity_type, entity_id);
CREATE INDEX idx_changelog_created ON changelog(created_at);
```

---

## How This Schema Solves Each Problem

### 1. Organization & Colocation
- **Categories** provide hierarchy (`Agents > Memory > Memory Tools`)
- **Features** are the atomic unit — each row is one Agno capability
- **Doc Pages** are linked to features with a `page_type` tag (`overview`, `usage`, `concept`, etc.)
- **Relations** connect pages that cover similar ground (e.g. `followup-suggestions` appears in both `agents/usage` and `teams/usage` — both pages get a `colocated` relation)

### 2. Change Tracking
- **`is_current`** on `doc_pages` marks whether a URL is still valid
- **`changelog`** table is an immutable append-only log (fits your DAO's transparency ethos)
- When a URL changes, you mark the old page `is_current = FALSE`, create a new page, and log it in the changelog with `action = 'url_changed'`

### 3. Agent Access via MCP
- The MCP Toolbox reads your `tools.yaml` and exposes SQL queries as tools
- Agents can query by category, feature type, keyword, page type, etc.
- The `relation_type = 'colocated'` lets agents suggest "see also" links

---

## Example Data Population

Here's how your table data maps from the markdown you provided:

| Table | Example rows |
|-------|-------------|
| **categories** | `{slug: "agents", name: "Agents"}`, `{slug: "teams", name: "Teams"}`, `{slug: "tools", name: "Tools"}`, `{slug: "memory", name: "Memory", parent_id: 1}`, `{slug: "knowledge", name: "Knowledge"}` |
| **features** | `{slug: "followup-suggestions", name: "Follow up suggestions", category_id: 1, feature_type: "subfeature"}`, `{slug: "mcp", name: "MCP", category_id: 3, feature_type: "tool"}`, `{slug: "memory-tools", name: "Memory tools", category_id: 4, feature_type: "subfeature"}` |
| **doc_pages** | `{feature_id: followup, page_type: "usage", url: "https://docs.agno.com/agents/usage/agent-with-followup-suggestions"}`, `{feature_id: followup, page_type: "usage", url: "https://docs.agno.com/teams/usage/team-with-followup-suggestions"}` |
| **doc_page_relations** | `{from: agents/followup, to: teams/followup, relation_type: "colocated"}` |
| **changelog** | `{entity: "doc_page", action: "created", change_note: "Initial seed of Agno docs database"}` |

---

## MCP Toolbox Configuration

Create a `tools.yaml` file that defines the tools agents can use:

```yaml
# tools.yaml — MCP Toolbox for Databases configuration
sources:
  agno-docs-db:
    kind: postgres
    host: ${DB_HOST}
    port: ${DB_PORT}
    database: ${DB_NAME}
    user: ${DB_USER}
    password: ${DB_PASSWORD}

tools:
  # ---- Feature queries ----
  search-features:
    kind: postgres-sql
    source: agno-docs-db
    description: >
      Search Agno documentation features by name or description.
      Returns matching features with their categories and doc page URLs.
    parameters:
      - name: query
        type: string
        description: "Search term for feature name or description"
    statement: |
      SELECT f.slug, f.name, f.description, f.feature_type,
             c.name AS category, c.slug AS category_slug
      FROM features f
      JOIN categories c ON f.category_id = c.id
      WHERE f.name ILIKE '%' || $1 || '%'
         OR f.description ILIKE '%' || $1 || '%'
      ORDER BY c.sort_order, f.sort_order

  get-feature-by-category:
    kind: postgres-sql
    source: agno-docs-db
    description: >
      Get all features in a given category (e.g. 'agents', 'tools', 'memory').
      Returns feature name, description, type, and all associated doc page URLs.
    parameters:
      - name: category_slug
        type: string
        description: "The category slug, e.g. 'agents', 'tools', 'memory'"
    statement: |
      SELECT f.slug, f.name, f.description, f.feature_type,
             f.is_experimental,
             json_agg(
               json_build_object(
                 'url', dp.url,
                 'type', dp.page_type,
                 'title', dp.title,
                 'is_current', dp.is_current
               )
             ) FILTER (WHERE dp.id IS NOT NULL) AS doc_pages
      FROM features f
      JOIN categories c ON f.category_id = c.id
      LEFT JOIN doc_pages dp ON dp.feature_id = f.id AND dp.is_current = TRUE
      WHERE c.slug = $1
      GROUP BY f.id, f.slug, f.name, f.description, f.feature_type, f.is_experimental
      ORDER BY f.sort_order

  get-feature-details:
    kind: postgres-sql
    source: agno-docs-db
    description: >
      Get full details for a specific feature including all doc pages,
      code snippets, and related pages (colocated, related, prerequisite).
    parameters:
      - name: feature_slug
        type: string
        description: "The feature slug, e.g. 'memory-tools', 'mcp'"
    statement: |
      SELECT f.name, f.description, f.feature_type, f.is_experimental,
             c.name AS category,
             json_agg(DISTINCT
               json_build_object(
                 'url', dp.url,
                 'type', dp.page_type,
                 'title', dp.title,
                 'summary', dp.summary,
                 'code_snippet', dp.code_snippet,
                 'is_current', dp.is_current
               )
             ) FILTER (WHERE dp.id IS NOT NULL) AS doc_pages,
             json_agg(DISTINCT
               json_build_object(
                 'url', rp.url,
                 'title', rp.title,
                 'relation', r.relation_type
               )
             ) FILTER (WHERE r.id IS NOT NULL) AS related_pages
      FROM features f
      JOIN categories c ON f.category_id = c.id
      LEFT JOIN doc_pages dp ON dp.feature_id = f.id
      LEFT JOIN doc_page_relations r ON r.from_page_id = dp.id
      LEFT JOIN doc_pages rp ON r.to_page_id = rp.id
      WHERE f.slug = $1
      GROUP BY f.id, f.name, f.description, f.feature_type, f.is_experimental, c.name

  list-categories:
    kind: postgres-sql
    source: agno-docs-db
    description: >
      List all documentation categories with their feature counts.
      Use this to discover the top-level organization of Agno docs.
    parameters: []
    statement: |
      SELECT c.slug, c.name, c.description,
             COUNT(f.id) AS feature_count,
             SUM(CASE WHEN f.feature_type = 'subfeature' THEN 1 ELSE 0 END) AS subfeature_count
      FROM categories c
      LEFT JOIN features f ON f.category_id = c.id
      GROUP BY c.id, c.slug, c.name, c.description
      ORDER BY c.sort_order

  get-colocated-pages:
    kind: postgres-sql
    source: agno-docs-db
    description: >
      Find pages that are colocated with a given doc page URL.
      Returns related pages that cover similar topics.
    parameters:
      - name: url
        type: string
        description: "A doc page URL to find colocated pages for"
    statement: |
      SELECT rp.url, rp.title, rp.page_type, r.relation_type
      FROM doc_page_relations r
      JOIN doc_pages dp ON r.from_page_id = dp.id
      JOIN doc_pages rp ON r.to_page_id = rp.id
      WHERE dp.url = $1
      ORDER BY r.relation_type

  get-recent-changes:
    kind: postgres-sql
    source: agno-docs-db
    description: >
      Get recent changes to the documentation database.
      Shows new features, updated pages, and URL changes.
    parameters:
      - name: limit
        type: integer
        description: "Number of recent changes to return (default 20)"
    statement: |
      SELECT cl.entity_type, cl.entity_id, cl.action, cl.change_note,
             cl.old_value, cl.new_value, cl.changed_by, cl.created_at
      FROM changelog cl
      ORDER BY cl.created_at DESC
      LIMIT $1

  search-doc-pages:
    kind: postgres-sql
    source: agno-docs-db
    description: >
      Search doc pages by keyword in title, summary, or URL.
      Returns matching pages with their feature and category.
    parameters:
      - name: query
        type: string
        description: "Search term for doc page title, summary, or URL"
    statement: |
      SELECT dp.url, dp.title, dp.summary, dp.page_type, dp.is_current,
             f.name AS feature_name, f.slug AS feature_slug,
             c.name AS category_name, c.slug AS category_slug
      FROM doc_pages dp
      JOIN features f ON dp.feature_id = f.id
      JOIN categories c ON f.category_id = c.id
      WHERE dp.is_current = TRUE
        AND (dp.title ILIKE '%' || $1 || '%'
          OR dp.summary ILIKE '%' || $1 || '%'
          OR dp.url ILIKE '%' || $1 || '%')
      ORDER BY dp.page_type, c.sort_order, f.sort_order

toolsets:
  agno-docs-search:
    - search-features
    - search-doc-pages
    - get-feature-details
    - get-colocated-pages

  agno-docs-browse:
    - list-categories
    - get-feature-by-category
    - get-feature-details

  agno-docs-changes:
    - get-recent-changes
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                   Agno Agents                        │
│  (use MCPTools or MCPToolbox to connect)            │
└─────────────────────┬───────────────────────────────┘
                      │ MCP Protocol (streamable-http)
                      ▼
┌─────────────────────────────────────────────────────┐
│           MCP Toolbox for Databases                  │
│  (reads tools.yaml, exposes SQL as MCP tools)        │
│  Runs as Docker container on port 5001               │
└─────────────────────┬───────────────────────────────┘
                      │ PostgreSQL wire protocol
                      ▼
┌─────────────────────────────────────────────────────┐
│              PostgreSQL Database                     │
│  Tables: categories, features, doc_pages,            │
│          doc_page_relations, changelog               │
│                                                      │
│  • categories: hierarchical grouping                  │
│  • features: one row per Agno capability              │
│  • doc_pages: URLs + metadata per feature            │
│  • doc_page_relations: colocated/related links        │
│  • changelog: immutable audit trail                  │
└─────────────────────────────────────────────────────┘
```

---

## Agent Code — Using the MCP Toolbox

Here's a complete Agno agent that connects to your docs database via MCP Toolbox:

```python
"""
Agno Docs Query Agent — connects to the Agno docs database via MCP Toolbox.
"""

import asyncio
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.mcp_toolbox import MCPToolbox

MCP_TOOLBOX_URL = "http://127.0.0.1:5001"  # MCP Toolbox server


async def main():
    async with MCPToolbox(
        url=MCP_TOOLBOX_URL,
        toolsets=["agno-docs-search", "agno-docs-browse", "agno-docs-changes"],
    ) as db_tools:
        agent = Agent(
            name="Agno Docs Assistant",
            model=Ollama(id="glm-5.1:cloud"),
            tools=[db_tools],
            instructions=[
                "You are an expert assistant for Agno documentation.",
                "Use the available database tools to find features, doc pages,",
                "related pages, and recent changes.",
                "When a user asks about a feature, always check for colocated",
                "pages that cover the same topic from different perspectives.",
                "When reporting URLs, clearly indicate which are current.",
                "If a feature is marked experimental, say so.",
            ],
            markdown=True,
            show_tool_calls=True,
        )

        await agent.acli_app(stream=True)


if __name__ == "__main__":
    asyncio.run(main())
```

---

## Setup Instructions

### 1. Create the PostgreSQL database and schema

```bash
# Create the database
createdb agno_docs

# Run the schema
psql -d agno_docs -f schema.sql
```

### 2. Seed the database

I can generate a Python seed script that parses your markdown table and populates all 5 tables. Want me to create that?

### 3. Set up MCP Toolbox for Databases

```bash
# Clone the MCP Toolbox demo and adapt
git clone https://github.com/googleapis/mcp-toolbox.git
# Or use the Agno cookbook demo structure:
# https://github.com/agno-agi/agno/tree/main/cookbook/14_tools/mcp/mcp_toolbox_demo

# Create a docker-compose.yml that points to your agno_docs database
# with your tools.yaml configuration
docker-compose up -d
```

### 4. Install dependencies

```bash
uv pip install agno toolbox-core
```

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **PostgreSQL** over SQLite | Full-text search, JSONB for changelog, concurrent access, production-grade. SQLite works for single-user local dev but not for MCP Toolbox. |
| **MCP Toolbox** over custom MCP server | Zero server code needed — just `tools.yaml`. You define SQL queries, it exposes them as MCP tools. |
| **Separate `doc_pages` table** | One feature can have multiple doc URLs (overview, usage, concept). Normalizing this avoids duplicate feature rows. |
| **`doc_page_relations` table** | Solves the colocation problem cleanly. Instead of a comma-separated list of URLs, you get structured relations that agents can traverse. |
| **`page_type` enum** | Lets agents filter by "just give me the overview" or "show me usage examples" — much more useful than raw URL searches. |
| **`is_current` flag** | When Agno moves a page (which they do), you don't delete the old record — you mark it `is_current = FALSE` and create a new one, with a changelog entry. This preserves history. |
| **Immutable `changelog` table** | Fits your DAO's emphasis on transparency. Every change is recorded with old/new values. No deletes, only appends. |
| **3 toolsets** in `tools.yaml` | Prevents tool overload. A general-purpose agent loads all 3. A focused agent can load just `agno-docs-search` or `agno-docs-changes`. |

---

## What's Next?

1. **Seed script** — Want me to generate a Python script that populates all tables from your markdown table?
2. **Docker Compose** — Want the full `docker-compose.yml` for PostgreSQL + MCP Toolbox?
3. **Migration strategy** — Want me to design an automated scraper that checks for new/changed pages on `docs.agno.com` and updates the database with changelog entries?
4. **Additional tools** — Want me to add full-text search tools (using PostgreSQL `tsvector`) to the `tools.yaml`?