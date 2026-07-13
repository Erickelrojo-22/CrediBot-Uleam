"""Pruebas del servicio RAG local."""
from app.services import rag_service


def test_split_policy_produces_chunks():
    text = "## A\n\n" + ("párrafo " * 80) + "\n\n## B\n\nSegundo bloque."
    chunks = rag_service._split_policy(text)
    assert len(chunks) >= 2
    assert any("Segundo bloque" in chunk for chunk in chunks)


def test_is_rag_available_without_api_key(monkeypatch):
    monkeypatch.setattr(rag_service.settings, "openai_api_key", "")
    assert rag_service.is_rag_available() is False
