"""Recuperación semántica en Supabase pgvector con fallback seguro."""
from typing import Any

from app.core.config import settings
from app.repositories.supabase_client import get_supabase_client


def semantic_search(query: str, limit: int = 3) -> list[dict[str, Any]]:
    """Busca chunks similares. Lanza excepción para activar el fallback local."""
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY no está configurada para embeddings.")
    from openai import OpenAI

    embedding = OpenAI(api_key=settings.openai_api_key).embeddings.create(
        model=settings.openai_embedding_model,
        input=query,
    ).data[0].embedding
    response = get_supabase_client().rpc(
        "match_rag_chunks",
        {"query_embedding": embedding, "match_count": limit},
    ).execute()
    return response.data or []
