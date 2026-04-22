"""
Seed the Zilliz Cloud 'agno_docs' Milvus collection from the local Agno docs repo.

Drops the existing collection first (schema mismatch), then re-seeds using Agno's
Knowledge pipeline so the schema matches what agent_designer expects.

Usage:
    python db/seed_milvus.py

Requirements:
    ZILLIZ_CLOUD_HOST   — Zilliz Cloud cluster endpoint URL
    ZILLIZ_CLOUD_TOKEN  — Zilliz Cloud API token
    OPENAI_API_KEY      — OpenAI key for text-embedding-3-small
"""

import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from pymilvus import MilvusClient

from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.milvus import Milvus

DOCS_PATH = Path("/Users/peteargent/ai/agno-docs")
COLLECTION = "agno_docs"
URI = os.environ["ZILLIZ_CLOUD_HOST"]
TOKEN = os.environ["ZILLIZ_CLOUD_TOKEN"]

# How many files to process concurrently (tune to avoid OpenAI rate limits)
BATCH_SIZE = 10


def drop_collection() -> None:
    client = MilvusClient(uri=URI, token=TOKEN)
    collections = client.list_collections()
    if COLLECTION in collections:
        client.drop_collection(COLLECTION)
        print(f"Dropped collection '{COLLECTION}'")
    else:
        print(f"Collection '{COLLECTION}' does not exist, skipping drop")


async def seed() -> None:
    drop_collection()

    vector_db = Milvus(
        collection=COLLECTION,
        uri=URI,
        token=TOKEN,
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    )

    knowledge = Knowledge(vector_db=vector_db)

    # Recursively collect all .md / .mdx files
    all_files = sorted(
        p for p in DOCS_PATH.rglob("*") if p.suffix in {".md", ".mdx"} and p.is_file()
    )
    total = len(all_files)
    print(f"Seeding {total} files from {DOCS_PATH} ...")

    for i in range(0, total, BATCH_SIZE):
        batch = all_files[i : i + BATCH_SIZE]
        tasks = [
            knowledge.ainsert(path=str(f), upsert=False, skip_if_exists=True)
            for f in batch
        ]
        await asyncio.gather(*tasks)
        print(f"  [{i + len(batch)}/{total}] inserted")

    print("Seeding complete.")


if __name__ == "__main__":
    asyncio.run(seed())
