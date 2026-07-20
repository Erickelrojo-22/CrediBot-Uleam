"""CLI para indexar documentos Markdown de políticas en pgvector.

Ejecuta desde creditbot: `python -m app.rag.ingest`.
"""
from pathlib import Path

from app.core.config import settings
from app.repositories.supabase_client import get_supabase_client

POLICY_DIR = Path(__file__).resolve().parents[2] / "docs" / "policies"


def _chunks(path: Path) -> list[tuple[str, str]]:
    title = path.stem.replace("_", " ").title()
    chunks: list[tuple[str, str]] = []
    current: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            if current:
                chunks.append((title, "\n".join(current).strip()))
            title, current = line[3:].strip(), []
        elif line.strip() and not line.startswith("# "):
            current.append(line.strip())
    if current:
        chunks.append((title, "\n".join(current).strip()))
    return [(heading, content) for heading, content in chunks if content]


def ingest_policies() -> int:
    """Genera embeddings y reemplaza los chunks de las políticas locales."""
    if not settings.openai_api_key:
        raise RuntimeError("Configura OPENAI_API_KEY antes de indexar políticas.")
    from openai import OpenAI

    client, database = OpenAI(api_key=settings.openai_api_key), get_supabase_client()
    total = 0
    for path in sorted(POLICY_DIR.glob("*.md")):
        document = database.table("rag_documents").upsert(
            {"title": path.stem.replace("_", " ").title(), "source_path": path.name},
            on_conflict="source_path",
        ).execute().data[0]
        database.table("rag_chunks").delete().eq("document_id", document["id"]).execute()
        for title, content in _chunks(path):
            embedding = client.embeddings.create(
                model=settings.openai_embedding_model, input=content
            ).data[0].embedding
            database.table("rag_chunks").insert(
                {"document_id": document["id"], "content": content, "embedding": embedding,
                 "metadata": {"title": title, "source": path.name}}
            ).execute()
            total += 1
    return total


if __name__ == "__main__":
    print(f"Chunks indexados: {ingest_policies()}")
