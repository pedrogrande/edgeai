"""
Seed script: inserts rows from docs/agent-design/agno-base-docs.csv into doc_pages.

Feature assignment uses Option B — infer feature_id from URL path segments by
matching against existing features.slug / categories.slug in the DB.
Requires seed_agno_docs.py to have been run first.

Run:
    python db/seed_base_docs_csv.py
"""

import csv
import json
import re
from pathlib import Path
from urllib.parse import urlparse

import psycopg

DB_URL = "postgresql://edgeai:edgeai@localhost:5533/edgeai"
CSV_PATH = Path(__file__).parent.parent / "docs" / "agent-design" / "agno-base-docs.csv"


# ---------------------------------------------------------------------------
# Helpers (consistent with seed_agno_docs.py)
# ---------------------------------------------------------------------------


def infer_page_type(url: str) -> str:
    path = url.rstrip("/").lower()
    if "/overview" in path:
        return "overview"
    if "/usage/" in path:
        return "usage"
    if "/examples/" in path or "/example" in path:
        return "example"
    if "/concept" in path:
        return "concept"
    if "/guide" in path:
        return "guide"
    if "/faq" in path:
        return "faq"
    return "reference"


def url_segments(url: str) -> list[str]:
    """Return non-empty path segments from a docs.agno.com URL, stripping .md extension."""
    path = urlparse(url).path.strip("/")
    # Strip .md from the last segment so slug matching works for both URL forms
    if path.endswith(".md"):
        path = path[:-3]
    return [s for s in path.split("/") if s]


def find_feature_id(cur, url: str) -> int | None:
    """
    Infer the best-matching feature_id from the URL path.

    Priority order:
      1. features.slug == '{seg0}-{seg1}'
      2. features.slug == '{seg0}'
      3. categories.slug == '{seg0}' → first feature in that category (sort_order ASC)

    Returns None if no match found.
    """
    segs = url_segments(url)
    if not segs:
        return None

    seg0 = segs[0]
    seg1 = segs[1] if len(segs) > 1 else None

    # 1. Two-segment slug match (e.g. 'agent-os', 'database-providers')
    if seg1:
        candidate = f"{seg0}-{seg1}"
        cur.execute("SELECT id FROM features WHERE slug = %s", (candidate,))
        row = cur.fetchone()
        if row:
            return row[0]

    # 2. Single-segment slug match against features
    cur.execute("SELECT id FROM features WHERE slug = %s", (seg0,))
    row = cur.fetchone()
    if row:
        return row[0]

    # 3. Single-segment slug match against categories → first feature in that category
    cur.execute(
        """
        SELECT f.id FROM features f
        JOIN categories c ON f.category_id = c.id
        WHERE c.slug = %s
        ORDER BY f.sort_order ASC
        LIMIT 1
        """,
        (seg0,),
    )
    row = cur.fetchone()
    if row:
        return row[0]

    return None


# ---------------------------------------------------------------------------
# Seeding
# ---------------------------------------------------------------------------


def seed(conn: psycopg.Connection) -> None:
    processed = 0
    inserted = 0
    skipped = 0

    with conn.cursor() as cur, open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            title = row["title"].strip()
            url = row["url"].strip()
            description = row["description"].strip()
            processed += 1

            feature_id = find_feature_id(cur, url)
            if feature_id is None:
                print(f"  [skip] No feature match for: {url}")
                skipped += 1
                continue

            page_type = infer_page_type(url)

            cur.execute(
                """
                INSERT INTO doc_pages (feature_id, page_type, url, title, summary, is_current)
                VALUES (%s, %s, %s, %s, %s, TRUE)
                ON CONFLICT (url, feature_id) DO NOTHING
                RETURNING id
                """,
                (feature_id, page_type, url, title, description),
            )
            result = cur.fetchone()

            if result:
                page_id = result[0]
                cur.execute(
                    """
                    INSERT INTO changelog (entity_type, entity_id, action, new_value, change_note, changed_by)
                    VALUES ('doc_page', %s, 'created',
                            %s::jsonb, 'Seeded from agno-base-docs.csv', 'seed_base_docs_csv')
                    """,
                    (
                        page_id,
                        json.dumps(
                            {"url": url, "page_type": page_type, "title": title}
                        ),
                    ),
                )
                inserted += 1
            else:
                # Row already existed — not an error
                skipped += 1

    conn.commit()
    print(f"\nDone — processed: {processed}, inserted: {inserted}, skipped: {skipped}")


if __name__ == "__main__":
    with psycopg.connect(DB_URL) as conn:
        seed(conn)
