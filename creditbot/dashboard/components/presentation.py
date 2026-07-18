"""Reglas de presentación compartidas por el dashboard de CrediBot."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

import pandas as pd


LOCAL_TIMEZONE = ZoneInfo("America/Guayaquil")

PERIOD_ALL = "Todo el histórico"
PERIOD_7_DAYS = "Últimos 7 días"
PERIOD_30_DAYS = "Últimos 30 días"
PERIOD_CUSTOM = "Rango personalizado"
PERIOD_OPTIONS = [PERIOD_ALL, PERIOD_7_DAYS, PERIOD_30_DAYS, PERIOD_CUSTOM]

RESULT_LABELS = {
    "preaprobado": "Preaprobada",
    "observado": "Observada",
    "no_cumple": "No cumple",
}
REQUEST_STATUS_LABELS = {
    "draft": "En progreso",
    "completed": "Completada",
}
CASE_STATUS_LABELS = {
    "pending": "Pendiente",
    "assigned": "En atención",
    "closed": "Cerrado",
}
CASE_REASON_LABELS = {
    "observed_result": "Resultado observado",
    "repeated_invalid_input": "Datos inválidos repetidos",
    "user_requested_advisor": "Solicitó un asesor",
    "menu_option_3": "Eligió hablar con un asesor",
}


@dataclass(frozen=True)
class PeriodRange:
    """Intervalo local con límite final exclusivo y periodo anterior equivalente."""

    label: str
    start: datetime | None = None
    end: datetime | None = None
    previous_start: datetime | None = None
    previous_end: datetime | None = None

    @property
    def is_historical(self) -> bool:
        return self.start is None or self.end is None


def now_local() -> datetime:
    """Retorna la hora actual del panel en Ecuador continental."""
    return datetime.now(LOCAL_TIMEZONE)


def _local_midnight(value: date) -> datetime:
    return datetime.combine(value, time.min, tzinfo=LOCAL_TIMEZONE)


def build_period_range(
    option: str,
    custom_dates: tuple[date, date] | list[date] | date | None = None,
    *,
    reference: datetime | None = None,
) -> PeriodRange:
    """Construye el periodo elegido y su intervalo anterior comparable."""
    if option == PERIOD_ALL:
        return PeriodRange(label=PERIOD_ALL)

    current = (reference or now_local()).astimezone(LOCAL_TIMEZONE)
    if option == PERIOD_7_DAYS:
        first_day = current.date() - timedelta(days=6)
        last_day = current.date()
    elif option == PERIOD_30_DAYS:
        first_day = current.date() - timedelta(days=29)
        last_day = current.date()
    else:
        if isinstance(custom_dates, date):
            first_day = last_day = custom_dates
        elif custom_dates:
            values = list(custom_dates)
            first_day = min(values)
            last_day = max(values)
        else:
            first_day = current.date() - timedelta(days=29)
            last_day = current.date()

    start = _local_midnight(first_day)
    end = _local_midnight(last_day + timedelta(days=1))
    duration = end - start
    return PeriodRange(
        label=option,
        start=start,
        end=end,
        previous_start=start - duration,
        previous_end=start,
    )


def filter_by_period(
    frame: pd.DataFrame,
    period: PeriodRange,
    column: str = "created_at",
) -> pd.DataFrame:
    """Filtra un DataFrame por un periodo local sin fallar ante fechas inválidas."""
    if frame.empty or period.is_historical or column not in frame:
        return frame.copy()
    timestamps = pd.to_datetime(frame[column], errors="coerce", utc=True)
    start = pd.Timestamp(period.start).tz_convert("UTC")
    end = pd.Timestamp(period.end).tz_convert("UTC")
    return frame[(timestamps >= start) & (timestamps < end)].copy()


def count_previous_period(
    frame: pd.DataFrame,
    period: PeriodRange,
    column: str = "created_at",
) -> int | None:
    """Cuenta registros del periodo anterior o retorna None para histórico."""
    if frame.empty or period.is_historical or column not in frame:
        return None if period.is_historical else 0
    timestamps = pd.to_datetime(frame[column], errors="coerce", utc=True)
    start = pd.Timestamp(period.previous_start).tz_convert("UTC")
    end = pd.Timestamp(period.previous_end).tz_convert("UTC")
    return int(((timestamps >= start) & (timestamps < end)).sum())


def comparison_delta(current: int, previous: int | None) -> str | None:
    """Texto honesto de variación para st.metric."""
    if previous is None:
        return None
    difference = current - previous
    sign = "+" if difference > 0 else ""
    return f"{sign}{difference} vs. periodo anterior"


def percentage(part: int | float, total: int | float) -> float:
    return round((float(part) / float(total)) * 100, 1) if total else 0.0


def safe_value(value: object, default: str = "No registrado") -> str:
    if value is None or (not isinstance(value, (dict, list)) and pd.isna(value)):
        return default
    text = str(value).strip()
    return text if text else default


def translate_result(value: object) -> str:
    raw = safe_value(value, "")
    return RESULT_LABELS.get(raw, raw or "Sin resultado")


def translate_request_status(value: object) -> str:
    raw = safe_value(value, "")
    return REQUEST_STATUS_LABELS.get(raw, raw or "Sin estado")


def translate_case_status(value: object) -> str:
    raw = safe_value(value, "")
    return CASE_STATUS_LABELS.get(raw, raw or "Sin estado")


def translate_case_reason(value: object) -> str:
    raw = safe_value(value, "")
    return CASE_REASON_LABELS.get(raw, raw or "Sin motivo registrado")


def case_priority(value: object) -> tuple[str, str]:
    """Retorna etiqueta y clase visual; no altera el estado persistido."""
    reason = safe_value(value, "")
    if reason in {"user_requested_advisor", "menu_option_3"}:
        return "Alta", "cb-pill-red"
    if reason in {"observed_result", "repeated_invalid_input"}:
        return "Media", "cb-pill-yellow"
    return "Revisar", "cb-pill"


def _parse_datetime(value: object) -> datetime | None:
    if value is None or pd.isna(value):
        return None
    parsed = pd.to_datetime(value, errors="coerce", utc=True)
    if pd.isna(parsed):
        return None
    return parsed.to_pydatetime().astimezone(LOCAL_TIMEZONE)


def format_datetime(value: object, *, include_year: bool = True) -> str:
    parsed = _parse_datetime(value)
    if not parsed:
        return "—"
    return parsed.strftime("%d/%m/%Y · %H:%M" if include_year else "%d/%m · %H:%M")


def relative_time(value: object, *, reference: datetime | None = None) -> str:
    parsed = _parse_datetime(value)
    if not parsed:
        return "Sin fecha"
    current = (reference or now_local()).astimezone(LOCAL_TIMEZONE)
    seconds = max(0, int((current - parsed).total_seconds()))
    if seconds < 60:
        return "Hace menos de un minuto"
    minutes = seconds // 60
    if minutes < 60:
        return f"Hace {minutes} min"
    hours = minutes // 60
    if hours < 24:
        return f"Hace {hours} h"
    days = hours // 24
    return f"Hace {days} día" if days == 1 else f"Hace {days} días"


def format_money(value: object, default: str = "—") -> str:
    if value is None or pd.isna(value):
        return default
    try:
        return f"${float(value):,.2f}"
    except (TypeError, ValueError):
        return default


def format_term(value: object, default: str = "—") -> str:
    if value is None or pd.isna(value):
        return default
    try:
        return f"{int(float(value))} meses"
    except (TypeError, ValueError):
        return default


def mask_cedula(value: object) -> str:
    text = safe_value(value, "")
    if len(text) < 5:
        return text or "—"
    return f"{text[:2]}******{text[-2:]}"


def mask_phone(value: object) -> str:
    text = safe_value(value, "")
    if len(text) < 6:
        return text or "—"
    return f"{text[:4]}****{text[-3:]}"


def redact_payload(value: object) -> object:
    """Oculta credenciales y datos personales dentro de payloads de auditoría."""
    sensitive_fragments = ("cedula", "password", "token", "secret", "api_key", "authorization")
    if isinstance(value, dict):
        return {
            str(key): (
                "[OCULTO]"
                if any(fragment in str(key).lower() for fragment in sensitive_fragments)
                else redact_payload(item)
            )
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact_payload(item) for item in value]
    return value
