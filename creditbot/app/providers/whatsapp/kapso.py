"""Proveedor y normalizador del webhook nativo de Kapso WhatsApp."""
from typing import Any

import httpx

from app.core.config import settings
from app.providers.whatsapp.base import WhatsAppProvider, WhatsAppProviderError


def normalize_kapso_phone(phone: str) -> str:
    """Normaliza un teléfono WhatsApp a dígitos internacionales."""
    return "".join(character for character in (phone or "") if character.isdigit())


class KapsoWhatsAppProvider(WhatsAppProvider):
    """Envía mensajes por la API proxy de WhatsApp Cloud API de Kapso."""

    name = "kapso"

    def send_text_message(self, to_phone: str, message: str) -> dict[str, Any]:
        if not settings.kapso_api_key:
            raise WhatsAppProviderError("KAPSO_API_KEY no está configurado.")
        if not settings.kapso_phone_number_id:
            raise WhatsAppProviderError(
                "KAPSO_PHONE_NUMBER_ID no está configurado."
            )

        version = settings.kapso_graph_api_version.strip("/") or "v24.0"
        url = (
            "https://api.kapso.ai/meta/whatsapp/"
            f"{version}/{settings.kapso_phone_number_id}/messages"
        )
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": normalize_kapso_phone(to_phone),
            "type": "text",
            "text": {"preview_url": False, "body": message},
        }
        headers = {
            "X-API-Key": settings.kapso_api_key,
            "Content-Type": "application/json",
        }

        try:
            response = httpx.post(url, json=payload, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            raise WhatsAppProviderError(
                f"Error de Kapso API ({exc.response.status_code}): {exc.response.text}"
            ) from exc
        except httpx.RequestError as exc:
            raise WhatsAppProviderError(f"Error de conexión con Kapso API: {exc}") from exc


def extract_kapso_messages(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Extrae mensajes de texto del formato v2 de Kapso, incluso en lotes."""
    event_payloads = payload.get("data") if payload.get("batch") else [payload]
    if not isinstance(event_payloads, list):
        return []

    messages: list[dict[str, Any]] = []
    for event_payload in event_payloads:
        if not isinstance(event_payload, dict):
            continue
        message = event_payload.get("message") or {}
        phone = normalize_kapso_phone(
            message.get("from")
            or (event_payload.get("conversation") or {}).get("phone_number")
            or (message.get("kapso") or {}).get("phone_number")
            or ""
        )
        if not phone:
            continue

        message_type = str(message.get("type") or "unknown")
        body = ((message.get("text") or {}).get("body") or "").strip()
        raw_payload = {
            "provider": "kapso",
            "id": message.get("id"),
            "timestamp": message.get("timestamp"),
            "type": message_type,
            "kapso": message.get("kapso") or {},
            "conversation_id": (event_payload.get("conversation") or {}).get("id"),
        }
        if message_type != "text":
            messages.append(
                {
                    "phone": phone,
                    "reply": "Por favor, envíame tu mensaje como texto. Puedo entenderte mejor cuando escribes.",
                    "raw_payload": raw_payload,
                }
            )
            continue
        if not body:
            continue

        messages.append(
            {
                "phone": phone,
                "message": body,
                "raw_payload": raw_payload,
            }
        )
    return messages
