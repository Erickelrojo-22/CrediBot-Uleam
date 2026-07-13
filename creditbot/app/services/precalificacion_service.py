"""Servicio de precalificación crediticia v2.

Orquesta las tres piezas del flujo v2 sin acoplarse al canal (WhatsApp) ni al LLM:
1. Valida la cédula ecuatoriana (app.domain.cedula_validator).
2. Consulta el perfil crediticio en el buró simulado (credit_profile_repository).
3. Aplica las reglas de negocio deterministas (app.domain.credit_rules).

Devuelve siempre un dict con la clave ``ok``. Si ``ok`` es False, ``error`` indica
el motivo (cedula_invalida). Si es True, incluye el resultado de la precalificación
y datos de presentación (cédula enmascarada, nombre, si tiene historial, etc.).
"""
from typing import Any

from app.domain import credit_rules
from app.domain.cedula_validator import mask_cedula, validate_cedula
from app.repositories import credit_profile_repository


def _profile_flags(profile: dict[str, Any] | None) -> dict[str, Any]:
    """Extrae, con valores por defecto seguros, los campos del perfil que usan las reglas."""
    if not profile:
        return {
            "score": 0,
            "cuotas_actuales": 0.0,
            "has_delinquency": False,
            "delinquency_days": 0,
            "lista_negra": False,
            "sin_historial": True,
            "full_name": None,
        }
    return {
        "score": int(profile.get("credit_score") or 0),
        "cuotas_actuales": float(profile.get("monthly_installments") or 0.0),
        "has_delinquency": bool(profile.get("has_delinquency")),
        "delinquency_days": int(profile.get("delinquency_days") or 0),
        "lista_negra": bool(profile.get("blacklisted")),
        "sin_historial": bool(profile.get("thin_file")),
        "full_name": profile.get("full_name"),
    }


def precalificar_por_cedula(
    cedula: str,
    ingreso_neto: float,
    plazo_meses: int,
    monto_solicitado: float | None = None,
) -> dict[str, Any]:
    """Ejecuta la precalificación completa a partir de una cédula.

    No lanza excepciones por datos del usuario: retorna siempre un dict con ``ok``.
    """
    es_valida, motivo = validate_cedula(cedula)
    if not es_valida:
        return {
            "ok": False,
            "error": "cedula_invalida",
            "motivo": motivo,
            "cedula_masked": mask_cedula(cedula),
        }

    profile = credit_profile_repository.get_profile_by_cedula(cedula)
    flags = _profile_flags(profile)

    resultado = credit_rules.precalificar(
        flags["score"],
        ingreso_neto,
        plazo_meses,
        cuotas_actuales=flags["cuotas_actuales"],
        has_delinquency=flags["has_delinquency"],
        delinquency_days=flags["delinquency_days"],
        lista_negra=flags["lista_negra"],
        sin_historial=flags["sin_historial"],
        monto_solicitado=monto_solicitado,
    )

    return {
        "ok": True,
        "cedula_masked": mask_cedula(cedula),
        "full_name": flags["full_name"],
        "tiene_perfil": profile is not None,
        "sin_historial": flags["sin_historial"],
        "credit_score": flags["score"] if profile is not None else None,
        **resultado,
    }
