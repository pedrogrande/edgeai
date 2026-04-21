-- ============================================================
-- Agno Docs Database Schema
-- Database: edgeai (reuses existing PostgreSQL container)
-- ============================================================

-- ============================================================
-- TABLE 1: categories
-- ============================================================
CREATE TABLE IF NOT EXISTS categories (
    id          SERIAL PRIMARY KEY,
    slug        VARCHAR(100) UNIQUE NOT NULL,
    name        VARCHAR(200) NOT NULL,
    description TEXT,
    parent_id   INTEGER REFERENCES categories(id),
    sort_order  INTEGER DEFAULT 0,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- TABLE 2: features
-- ============================================================
CREATE TABLE IF NOT EXISTS features (
    id              SERIAL PRIMARY KEY,
    slug            VARCHAR(200) UNIQUE NOT NULL,
    name            VARCHAR(200) NOT NULL,
    description     TEXT NOT NULL,
    category_id     INTEGER NOT NULL REFERENCES categories(id),
    feature_type    VARCHAR(50) NOT NULL
                        CHECK (feature_type IN ('core', 'subfeature', 'tool', 'integration', 'concept')),
    is_experimental BOOLEAN DEFAULT FALSE,
    sort_order      INTEGER DEFAULT 0,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- TABLE 3: doc_pages
-- ============================================================
CREATE TABLE IF NOT EXISTS doc_pages (
    id          SERIAL PRIMARY KEY,
    feature_id  INTEGER NOT NULL REFERENCES features(id) ON DELETE CASCADE,
    page_type   VARCHAR(50) NOT NULL
                    CHECK (page_type IN ('overview', 'usage', 'concept', 'reference', 'example', 'guide', 'faq')),
    url         TEXT NOT NULL,
    title       VARCHAR(500),
    summary     TEXT,
    code_snippet TEXT,
    is_current  BOOLEAN DEFAULT TRUE,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(url, feature_id)
);

-- ============================================================
-- TABLE 4: doc_page_relations
-- ============================================================
CREATE TABLE IF NOT EXISTS doc_page_relations (
    id            SERIAL PRIMARY KEY,
    from_page_id  INTEGER NOT NULL REFERENCES doc_pages(id) ON DELETE CASCADE,
    to_page_id    INTEGER NOT NULL REFERENCES doc_pages(id) ON DELETE CASCADE,
    relation_type VARCHAR(50) NOT NULL
                      CHECK (relation_type IN ('related', 'duplicate', 'supersedes', 'colocated', 'prerequisite')),
    created_at    TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(from_page_id, to_page_id, relation_type)
);

-- ============================================================
-- TABLE 5: changelog (immutable append-only audit log)
-- ============================================================
CREATE TABLE IF NOT EXISTS changelog (
    id          SERIAL PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL
                    CHECK (entity_type IN ('feature', 'category', 'doc_page', 'relation')),
    entity_id   INTEGER NOT NULL,
    action      VARCHAR(20) NOT NULL
                    CHECK (action IN ('created', 'updated', 'deleted', 'url_changed')),
    old_value   JSONB,
    new_value   JSONB,
    change_note TEXT,
    changed_by  VARCHAR(200),
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- INDEXES
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_features_category    ON features(category_id);
CREATE INDEX IF NOT EXISTS idx_features_type        ON features(feature_type);
CREATE INDEX IF NOT EXISTS idx_features_slug        ON features(slug);
CREATE INDEX IF NOT EXISTS idx_doc_pages_feature    ON doc_pages(feature_id);
CREATE INDEX IF NOT EXISTS idx_doc_pages_type       ON doc_pages(page_type);
CREATE INDEX IF NOT EXISTS idx_doc_pages_url        ON doc_pages(url);
CREATE INDEX IF NOT EXISTS idx_doc_pages_current    ON doc_pages(is_current);
CREATE INDEX IF NOT EXISTS idx_doc_page_rels_from   ON doc_page_relations(from_page_id);
CREATE INDEX IF NOT EXISTS idx_doc_page_rels_to     ON doc_page_relations(to_page_id);
CREATE INDEX IF NOT EXISTS idx_changelog_entity     ON changelog(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_changelog_created    ON changelog(created_at);
