"""Pruebas del proveedor y del formato de webhook de Kapso."""
import pytest

from app.providers.whatsapp.factory import get_whatsapp_provider
from app.providers.whatsapp.kapso import (
    KapsoWhatsAppProvider,
    extract_kapso_messages,
    normalize_kapso_phone,
)


def test_normalize_kapso_phone():
    assert normalize_kapso_phone("+593 99 999 9999") == "593999999999"


def test_extract_kapso_message_v2():
    payload = {
        "message": {
            "id": "wamid.1",
            "timestamp": "123",
            "type": "text",
            "from": "593999999999",
            "text": {"body": "Hola"},
            "kapso": {"direction": "inbound"},
        },
        "conversation": {"id": "conv-1", "phone_number": "593999999999"},
    }

    messages = extract_kapso_messages(payload)

    assert len(messages) == 1
    assert messages[0]["phone"] == "593999999999"
    assert messages[0]["message"] == "Hola"
    assert messages[0]["raw_payload"]["provider"] == "kapso"


def test_extract_kapso_batch_uses_conversation_phone():
    payload = {
        "type": "whatsapp.message.received",
        "batch": True,
        "data": [
            {
                "message": {"type": "text", "text": {"body": "Primero"}},
                "conversation": {"phone_number": "+593999000111"},
            }
        ],
    }

    messages = extract_kapso_messages(payload)

    assert messages[0]["phone"] == "593999000111"
    assert messages[0]["message"] == "Primero"


def test_factory_uses_kapso(monkeypatch):
    get_whatsapp_provider.cache_clear()
    monkeypatch.setattr(
        "app.providers.whatsapp.factory.settings.whatsapp_provider",
        "kapso",
    )

    provider = get_whatsapp_provider()

    assert isinstance(provider, KapsoWhatsAppProvider)
    assert provider.name == "kapso"
    get_whatsapp_provider.cache_clear()


def test_factory_rejects_unknown(monkeypatch):
    get_whatsapp_provider.cache_clear()
    monkeypatch.setattr(
        "app.providers.whatsapp.factory.settings.whatsapp_provider",
        "telegram",
    )
    with pytest.raises(Exception, match="desconocido"):
        get_whatsapp_provider()
    get_whatsapp_provider.cache_clear()
