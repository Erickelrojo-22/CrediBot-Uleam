"""Dependencias compartidas de autenticación admin."""
from fastapi import Header, HTTPException

from app.core.config import settings


def require_admin_password(
    x_admin_password: str | None = Header(default=None, alias="X-Admin-Password"),
) -> None:
    """Valida la contraseña compartida del panel / API admin."""
    expected = (settings.admin_dashboard_password or "").strip()
    if not expected:
        raise HTTPException(
            status_code=500,
            detail="ADMIN_DASHBOARD_PASSWORD no está configurado en el backend.",
        )
    if not x_admin_password or x_admin_password.strip() != expected:
        raise HTTPException(status_code=401, detail="No autorizado.")
