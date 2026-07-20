"""Pruebas del webhook firmado de Kapso."""
import hashlib
import hmac
import json

from fastapi.testclient import TestClient

from app.main import app


def _signature(secret: str, body: bytes) -> str:
    return hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()


def test_webhook_kapso_procesa_mensaje_firmado(monkeypatch):
    from app.api import routes_webhook

    secret = "kapso-webhook-test"
    monkeypatch.setattr(routes_webhook.settings, "kapso_webhook_secret", secret)
    monkeypatch.setattr(
        routes_webhook.settings, "kapso_validate_webhook_signature", True
    )
    monkeypatch.setattr(
        routes_webhook,
        "process_message",
        lambda phone, message, raw_payload: f"Respuesta para {message}",
    )
    sent = []
    monkeypatch.setattr(
        routes_webhook,
        "send_text_message",
        lambda phone, message: sent.append((phone, message)),
    )
    payload = {
        "message": {
            "id": "wamid.1",
            "from": "593999000111",
            "type": "text",
            "text": {"body": "Hola"},
        },
        "conversation": {"id": "conv-1"},
    }
    raw_body = json.dumps(payload).encode("utf-8")

    response = TestClient(app).post(
        "/webhook/whatsapp",
        content=raw_body,
        headers={
            "Content-Type": "application/json",
            "X-Webhook-Event": "whatsapp.message.received",
            "X-Webhook-Signature": _signature(secret, raw_body),
        },
    )

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert sent == [("593999000111", "Respuesta para Hola")]


def test_webhook_kapso_rechaza_firma_invalida(monkeypatch):
    from app.api import routes_webhook

    monkeypatch.setattr(routes_webhook.settings, "kapso_webhook_secret", "secret")
    monkeypatch.setattr(
        routes_webhook.settings, "kapso_validate_webhook_signature", True
    )

    response = TestClient(app).post(
        "/webhook/whatsapp",
        json={"message": {"type": "text"}},
        headers={
            "X-Webhook-Event": "whatsapp.message.received",
            "X-Webhook-Signature": "invalid",
        },
    )

    assert response.status_code == 403
