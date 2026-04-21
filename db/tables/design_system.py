"""
SQLAlchemy Core Table definition for the `design_system` table.

A design system groups related agent specs together (e.g. one per product,
project, or team). The authoritative DDL is in
db/migrations/001_create_design_system.sql.
"""

import sqlalchemy as sa
from db import metadata

design_system_table = sa.Table(
    "design_system",
    metadata,
    sa.Column(
        "id",
        sa.UUID(as_uuid=True),
        nullable=False,
        server_default=sa.text("gen_random_uuid()"),
    ),
    sa.Column("name", sa.Text(), nullable=False),
    sa.Column("description", sa.Text(), nullable=True),
    sa.Column("created_by", sa.UUID(as_uuid=True), nullable=False),
    sa.Column(
        "created_at",
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.text("now()"),
    ),
    sa.Column(
        "updated_at",
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.text("now()"),
    ),
    schema="public",
)
