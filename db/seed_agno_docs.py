"""
Seed script: populates the Agno docs database from docs/agent-design/Agno-features.md.

Run once after applying db/schema.sql:
    python db/seed_agno_docs.py

The markdown table structure:
- Bold feature name  → category (top-level section)
- Plain feature name → feature (child of most recent category)
- Multiple URLs in a cell → one doc_page row each, all linked as 'colocated'
"""

import json
import re
import sys
from pathlib import Path

import psycopg

DB_URL = "postgresql://edgeai:edgeai@localhost:5533/edgeai"
FEATURES_MD = (
    Path(__file__).parent.parent / "docs" / "agent-design" / "Agno-features.md"
)

# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------


def strip_md(text: str) -> str:
    """Remove markdown bold, inline code, and link syntax."""
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)  # **bold**
    text = re.sub(r"`([^`]+)`", r"\1", text)  # `code`
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)  # [label](url)
    return text.strip()


def extract_urls(cell: str) -> list[str]:
    """Extract all https URLs from a markdown table cell."""
    urls = re.findall(r"https://[^\s)\]]+", cell)
    # Markdown sometimes escapes # as \# in link display text — normalise.
    return [u.replace("\\#", "#") for u in urls]


def slugify(text: str) -> str:
    """Convert display name to a slug."""
    text = strip_md(text).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def infer_page_type(url: str) -> str:
    """Guess page_type from URL path segments."""
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


def parse_features_md(path: Path) -> list[dict]:
    """
    Parse the markdown table into a list of row dicts:
        {"raw_name": str, "is_category": bool, "description": str, "urls": [str]}
    """
    rows = []
    in_table = False

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        # Detect table start (header row)
        if line.startswith("| Feature") and "Usage" in line:
            in_table = True
            continue
        # Skip separator row
        if in_table and re.match(r"^\|[\s:\-|]+\|$", line):
            continue
        # End of table
        if in_table and not line.startswith("|"):
            in_table = False
            continue

        if not in_table or not line.startswith("|"):
            continue

        # Split cells — strip outer pipes, split on |
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue

        name_cell, usage_cell = cells[0], cells[1]
        link_cell = cells[2] if len(cells) > 2 else ""

        # Empty name cell means continuation of previous feature's link cell
        if not name_cell and not usage_cell and link_cell:
            if rows:
                rows[-1]["urls"].extend(extract_urls(link_cell))
            continue

        is_category = bool(re.match(r"\*\*", name_cell))
        raw_name = strip_md(name_cell)
        description = strip_md(usage_cell)
        urls = extract_urls(link_cell) + extract_urls(usage_cell)

        if raw_name:
            rows.append(
                {
                    "raw_name": raw_name,
                    "is_category": is_category,
                    "description": description,
                    "urls": urls,
                }
            )

    return rows


def unique_slug(base: str, seen: set[str]) -> str:
    """Return base slug, appending -2/-3/... if already used."""
    slug = base
    counter = 2
    while slug in seen:
        slug = f"{base}-{counter}"
        counter += 1
    seen.add(slug)
    return slug


# ---------------------------------------------------------------------------
# Database seeding
# ---------------------------------------------------------------------------


def seed(conn: psycopg.Connection) -> None:
    rows = parse_features_md(FEATURES_MD)

    current_category_id: int | None = None
    current_category_slug: str | None = None
    category_sort = 0
    feature_sort = 0
    seen_slugs: set[str] = set()

    with conn.cursor() as cur:
        for row in rows:
            name = row["raw_name"]
            slug = unique_slug(slugify(name), seen_slugs)
            description = row["description"] or name
            urls = row["urls"]

            if row["is_category"]:
                # ── Insert category ────────────────────────────────────────
                cur.execute(
                    """
                    INSERT INTO categories (slug, name, description, sort_order)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (slug) DO UPDATE SET updated_at = NOW()
                    RETURNING id
                    """,
                    (slug, name, description, category_sort),
                )
                current_category_id = cur.fetchone()[0]
                current_category_slug = slug
                category_sort += 10
                feature_sort = 0

                cur.execute(
                    """
                    INSERT INTO changelog (entity_type, entity_id, action, new_value, change_note, changed_by)
                    VALUES ('category', %s, 'created',
                            %s::jsonb, 'Initial seed from Agno-features.md', 'seed_script')
                    """,
                    (current_category_id, json.dumps({"slug": slug, "name": name})),
                )

                # Categories may also have doc pages (e.g. overview links)
                if urls and current_category_id:
                    # Insert a stub feature to hold the category overview page
                    cur.execute(
                        """
                        INSERT INTO features (slug, name, description, category_id, feature_type, sort_order)
                        VALUES (%s, %s, %s, %s, 'core', %s)
                        ON CONFLICT (slug) DO UPDATE SET updated_at = NOW()
                        RETURNING id
                        """,
                        (
                            slug + "-overview",
                            name,
                            description,
                            current_category_id,
                            feature_sort,
                        ),
                    )
                    feature_id = cur.fetchone()[0]
                    feature_sort += 10

                    cur.execute(
                        """
                        INSERT INTO changelog (entity_type, entity_id, action, new_value, change_note, changed_by)
                        VALUES ('feature', %s, 'created',
                                %s::jsonb, 'Category overview feature', 'seed_script')
                        """,
                        (
                            feature_id,
                            json.dumps({"slug": slug + "-overview", "name": name}),
                        ),
                    )

                    _insert_doc_pages(cur, feature_id, urls, description)

            else:
                # ── Insert feature ─────────────────────────────────────────
                if current_category_id is None:
                    print(f"  [warn] No category yet for feature '{name}' — skipping")
                    continue

                is_experimental = "experimental" in description.lower()

                cur.execute(
                    """
                    INSERT INTO features (slug, name, description, category_id, feature_type, is_experimental, sort_order)
                    VALUES (%s, %s, %s, %s, 'subfeature', %s, %s)
                    ON CONFLICT (slug) DO UPDATE SET updated_at = NOW()
                    RETURNING id
                    """,
                    (
                        slug,
                        name,
                        description,
                        current_category_id,
                        is_experimental,
                        feature_sort,
                    ),
                )
                feature_id = cur.fetchone()[0]
                feature_sort += 10

                cur.execute(
                    """
                    INSERT INTO changelog (entity_type, entity_id, action, new_value, change_note, changed_by)
                    VALUES ('feature', %s, 'created',
                            %s::jsonb, 'Initial seed from Agno-features.md', 'seed_script')
                    """,
                    (feature_id, json.dumps({"slug": slug, "name": name})),
                )

                if urls:
                    _insert_doc_pages(cur, feature_id, urls, description)

    conn.commit()
    print("Seed complete.")


def _insert_doc_pages(cur, feature_id: int, urls: list[str], description: str) -> None:
    """Insert doc pages for a feature. Add colocated relations when there are multiple URLs."""
    page_ids = []

    for url in urls:
        page_type = infer_page_type(url)
        cur.execute(
            """
            INSERT INTO doc_pages (feature_id, page_type, url, summary, is_current)
            VALUES (%s, %s, %s, %s, TRUE)
            ON CONFLICT (url, feature_id) DO NOTHING
            RETURNING id
            """,
            (feature_id, page_type, url, description),
        )
        result = cur.fetchone()
        if result:
            page_ids.append(result[0])

            cur.execute(
                """
                INSERT INTO changelog (entity_type, entity_id, action, new_value, change_note, changed_by)
                VALUES ('doc_page', %s, 'created',
                        %s::jsonb, 'Initial seed from Agno-features.md', 'seed_script')
                """,
                (result[0], json.dumps({"url": url, "page_type": page_type})),
            )

    # Create colocated relations between all page pairs
    if len(page_ids) > 1:
        for i, from_id in enumerate(page_ids):
            for to_id in page_ids[i + 1 :]:
                for a, b in [(from_id, to_id), (to_id, from_id)]:
                    cur.execute(
                        """
                        INSERT INTO doc_page_relations (from_page_id, to_page_id, relation_type)
                        VALUES (%s, %s, 'colocated')
                        ON CONFLICT DO NOTHING
                        RETURNING id
                        """,
                        (a, b),
                    )
                    result = cur.fetchone()
                    if result:
                        cur.execute(
                            """
                            INSERT INTO changelog (entity_type, entity_id, action, new_value, change_note, changed_by)
                            VALUES ('relation', %s, 'created',
                                    %s::jsonb, 'Colocated pages (same feature, multiple URLs)', 'seed_script')
                            """,
                            (
                                result[0],
                                json.dumps({"from": a, "to": b, "type": "colocated"}),
                            ),
                        )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if not FEATURES_MD.exists():
        print(f"ERROR: Cannot find {FEATURES_MD}", file=sys.stderr)
        sys.exit(1)

    print(f"Connecting to {DB_URL} ...")
    with psycopg.connect(DB_URL) as conn:
        print("Seeding Agno docs database ...")
        seed(conn)
