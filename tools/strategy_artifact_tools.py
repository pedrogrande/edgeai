"""
Strategy Artifact Tools — Agno Toolkit for saving, listing, and reading
strategy artifacts as markdown files with YAML front matter.

Artifacts are saved to the `artifacts/strategy/` directory as markdown files.
The Document Manager Agent is responsible for ingesting these files into its
knowledge base — this toolkit only handles file I/O.

Usage in strategy_advisor.py:
    from tools.strategy_artifact_tools import StrategyArtifactTools
    tools=[..., StrategyArtifactTools(), ...]
"""

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import yaml
from agno.tools import Toolkit
from agno.utils.log import logger


# Default base directory for strategy artifacts
DEFAULT_BASE_DIR = Path("artifacts/strategy")


class StrategyArtifactTools(Toolkit):
    """
    Agno Toolkit for managing strategy artifact files.

    Provides three tools:
    - save_artifact: Save a markdown file with YAML front matter (HITL-gated)
    - list_artifacts: List all .md files in the artifacts directory
    - read_artifact: Read a specific artifact file
    """

    def __init__(self, base_dir: Optional[Path] = None):
        super().__init__(name="strategy_artifact_tools")
        self.base_dir = base_dir or DEFAULT_BASE_DIR
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.register(self.save_artifact)
        self.register(self.list_artifacts)
        self.register(self.read_artifact)

    def _slugify(self, text: str) -> str:
        """Convert a title to a filesystem-safe slug."""
        slug = text.lower().strip()
        # Replace spaces and common separators with hyphens
        for ch in (" ", "_", "/", "\\"):
            slug = slug.replace(ch, "-")
        # Remove non-alphanumeric characters (except hyphens)
        slug = "".join(c for c in slug if c.isalnum() or c == "-")
        # Collapse multiple hyphens and strip edges
        while "--" in slug:
            slug = slug.replace("--", "-")
        return slug.strip("-")

    def _front_matter(self, title: str, artifact_type: str) -> str:
        """Generate YAML front matter for a strategy artifact."""
        now = datetime.now(timezone.utc)
        metadata = {
            # ── Identity ──
            "title": title,
            "slug": self._slugify(title),
            "created": now.isoformat(),
            "updated": now.isoformat(),
            "version": "0.1",
            # ── Work Product Status ──
            "status": "draft",
            # ── AI Usage Transparency ──
            "authorship": "collaborative",
            "authorship_detail": "Human–agent collaborative session",
            # ── Classification ──
            "category": "strategy",
            "tags": [artifact_type],
            "description": f"{artifact_type.capitalize()}: {title}",
            # ── Relationships ──
            "related": [],
            # ── Retrieval Hints ──
            "audience": ["strategist", "founder", "product-manager"],
            "domain": "business-strategy",
        }
        return yaml.dump(metadata, default_flow_style=False, sort_keys=False)

    def save_artifact(self, title: str, artifact_type: str, content: str) -> str:
        """
        Save a strategy artifact as a markdown file with YAML front matter.

        IMPORTANT: Only call this after the user has explicitly confirmed they want
        to save the artifact. Propose the artifact first, wait for confirmation,
        then call this tool.

        Args:
            title: Short descriptive title (e.g., "SWOT Analysis: Acme Corp Q4 2025")
            artifact_type: One of: strategy, framework, analysis, template, insight
            content: The full markdown content to save — be specific, structured, and actionable

        Returns:
            Confirmation message with the saved file path, or an error message.
        """
        if not title or not title.strip():
            return "Error: title is required"
        if not content or not content.strip():
            return "Error: content is required"

        valid_types = ["strategy", "framework", "analysis", "template", "insight"]
        if artifact_type not in valid_types:
            return f"Error: artifact_type must be one of {valid_types}, got '{artifact_type}'"

        slug = self._slugify(title)
        filename = f"{slug}.md"
        filepath = self.base_dir / filename

        # Build the file: front matter + content
        front_matter = self._front_matter(title, artifact_type)
        file_content = f"---\n{front_matter}---\n\n{content.strip()}\n"

        try:
            filepath.write_text(file_content, encoding="utf-8")
            logger.info(f"Saved strategy artifact: {filepath}")
            return (
                f"✅ Saved artifact: '{title}' (type: {artifact_type})\n"
                f"   File: {filepath}\n"
                f"   The Document Manager Agent will ingest this into its knowledge base."
            )
        except Exception as e:
            logger.error(f"Failed to save artifact: {e}")
            return f"Error: Failed to save artifact — {e}"

    def list_artifacts(self) -> str:
        """
        List all strategy artifact files in the artifacts directory.

        Returns:
            A formatted list of all .md files with their titles and types,
            or a message if no artifacts exist yet.
        """
        md_files = sorted(self.base_dir.glob("*.md"))
        if not md_files:
            return "No strategy artifacts found. Start a conversation to create your first one."

        lines = [f"📋 Strategy Artifacts ({len(md_files)} files):\n"]
        for f in md_files:
            # Read just the front matter to extract title
            try:
                text = f.read_text(encoding="utf-8")
                title = f.stem.replace("-", " ").title()
                if text.startswith("---"):
                    end = text.find("---", 3)
                    if end > 0:
                        import yaml as _yaml
                        fm = _yaml.safe_load(text[3:end])
                        title = fm.get("title", title)
                lines.append(f"  • {f.name}  —  {title}")
            except Exception:
                lines.append(f"  • {f.name}")

        return "\n".join(lines)

    def read_artifact(self, filename: str) -> str:
        """
        Read a specific strategy artifact file.

        Args:
            filename: The filename to read (e.g., "swot-analysis-acme-corp.md")

        Returns:
            The full file content, or an error message if the file doesn't exist.
        """
        # Sanitize filename — no path traversal
        safe_name = Path(filename).name
        filepath = self.base_dir / safe_name

        if not filepath.exists():
            available = [f.name for f in sorted(self.base_dir.glob("*.md"))]
            avail_str = ", ".join(available) if available else "none"
            return f"Error: File '{safe_name}' not found. Available: {avail_str}"

        try:
            return filepath.read_text(encoding="utf-8")
        except Exception as e:
            return f"Error: Failed to read '{safe_name}' — {e}"