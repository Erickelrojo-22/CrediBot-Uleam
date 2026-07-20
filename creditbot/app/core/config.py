"""Configuración central de la aplicación usando variables de entorno."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Lee y expone las variables de entorno definidas en el archivo .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Configuración general de la aplicación ---
    app_name: str = "CrediBot"
    app_env: str = "development"
    app_debug: bool = True
    app_public_url: str = ""

    # --- Credenciales de Supabase (base de datos) ---
    supabase_url: str = ""
    supabase_service_role_key: str = ""

    # --- Redis (sesión activa; Upstash o Memorystore) ---
    redis_url: str = ""
    redis_session_ttl_seconds: int = 3600

    # --- Configuración de OpenAI (IA conversacional) ---
    openai_api_key: str = ""
    openai_model: str = "gpt-5.5"
    openai_embedding_model: str = "text-embedding-3-small"
    openai_enable_ai: bool = True

    # --- WhatsApp con Kapso ---
    whatsapp_provider: str = "kapso"
    kapso_api_key: str = ""
    kapso_phone_number_id: str = ""
    kapso_webhook_secret: str = ""
    kapso_validate_webhook_signature: bool = True
    kapso_graph_api_version: str = "v24.0"

    # --- Configuración regional ---
    default_country_code: str = "593"

    # --- Auth del panel admin / API de handoff ---
    admin_dashboard_password: str = ""


settings = Settings()
