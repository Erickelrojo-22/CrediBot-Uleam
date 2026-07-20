"""Fachada de WhatsApp mediante Kapso."""
from app.providers.whatsapp.base import WhatsAppProviderError as WhatsAppServiceError
from app.providers.whatsapp.factory import send_text_message

__all__ = [
    "WhatsAppServiceError",
    "send_text_message",
]
