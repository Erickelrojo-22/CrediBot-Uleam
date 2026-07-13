"""Recuperación de contexto (RAG) sobre la política de crédito.

Usa embeddings de OpenAI sobre un documento local. Las tablas `rag_*` en Supabase
quedan preparadas para una migración futura; este servicio funciona sin pgvector.
"""
from __future__ import annotations

import logging
import math
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

from app.core.config import settings

logger = logging.getLogger(__name__)

POLICY_PATH = Path(__file__).resolve().parents[2] / "data" / "politica_credito.md"
EMBEDDING_MODEL = "text-embedding-3-small"
CHUNK_SIZE = 500


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b, strict=False))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if not norm_a or not norm_b:
        return 0.0
    return dot / (norm_a * norm_b)


def _split_policy(text: str) -> list[str]:
    """Divide la política en fragmentos por secciones y párrafos."""
    sections = re.split(r"\n(?=## )", text.strip())
    chunks: list[str] = []
    for section in sections:
        section = section.strip()
        if not section:
            continue
        if len(section) <= CHUNK_SIZE:
            chunks.append(section)
            continue
        paragraphs = [p.strip() for p in section.split("\n\n") if p.strip()]
        buffer = ""
        for paragraph in paragraphs:
            candidate = f"{buffer}\n\n{paragraph}".strip() if buffer else paragraph
            if len(candidate) <= CHUNK_SIZE:
                buffer = candidate
            else:
                if buffer:
                    chunks.append(buffer)
                buffer = paragraph
        if buffer:
            chunks.append(buffer)
    return chunks


def _load_policy_text() -> str:
    if not POLICY_PATH.is_file():
        logger.warning("No se encontró el documento RAG en %s", POLICY_PATH)
        return ""
    return POLICY_PATH.read_text(encoding="utf-8")


def _embed_texts(texts: list[str]) -> list[list[float]]:
    from openai import OpenAI

    client = OpenAI(api_key=settings.openai_api_key)
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]


@lru_cache(maxsize=1)
def _indexed_chunks() -> tuple[tuple[str, ...], tuple[tuple[float, ...], ...]]:
    """Carga chunks y embeddings (cacheados en memoria)."""
    policy = _load_policy_text()
    chunks = tuple(_split_policy(policy))
    if not chunks or not settings.openai_api_key:
        return (), ()
    vectors = _embed_texts(list(chunks))
    return chunks, tuple(tuple(vector) for vector in vectors)


def is_rag_available() -> bool:
    """Indica si hay documento de política y API key para embeddings."""
    return bool(_load_policy_text().strip() and settings.openai_api_key)


def retrieve_context(query: str, *, top_k: int = 3) -> list[str]:
    """Devuelve los fragmentos más relevantes para la pregunta del usuario."""
    chunks, vectors = _indexed_chunks()
    if not chunks or not vectors:
        return []

    query_vector = _embed_texts([query])[0]
    scored: list[tuple[float, str]] = []
    for chunk, vector in zip(chunks, vectors, strict=False):
        scored.append((_cosine_similarity(query_vector, list(vector)), chunk))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [chunk for score, chunk in scored[:top_k] if score > 0.15]


def build_context_block(chunks: list[str]) -> str:
    """Formatea los fragmentos recuperados para el prompt del LLM."""
    if not chunks:
        return ""
    return "\n\n---\n\n".join(chunks)
