from datetime import date, datetime

import pandas as pd

from components.presentation import (
    LOCAL_TIMEZONE,
    PERIOD_7_DAYS,
    PERIOD_ALL,
    PERIOD_CUSTOM,
    build_period_range,
    case_priority,
    comparison_delta,
    count_previous_period,
    filter_by_period,
    format_datetime,
    mask_cedula,
    mask_phone,
    percentage,
    redact_payload,
    relative_time,
    translate_case_reason,
    translate_request_status,
    translate_result,
)


REFERENCE = datetime(2026, 7, 17, 12, 0, tzinfo=LOCAL_TIMEZONE)


def test_historical_period_does_not_filter_or_invent_comparison() -> None:
    period = build_period_range(PERIOD_ALL, reference=REFERENCE)
    frame = pd.DataFrame([{"created_at": "2025-01-01T00:00:00Z"}])
    assert period.is_historical
    assert len(filter_by_period(frame, period)) == 1
    assert count_previous_period(frame, period) is None
    assert comparison_delta(1, None) is None


def test_seven_day_period_and_previous_interval() -> None:
    period = build_period_range(PERIOD_7_DAYS, reference=REFERENCE)
    assert period.start.date() == date(2026, 7, 11)
    assert period.end.date() == date(2026, 7, 18)
    frame = pd.DataFrame(
        [
            {"created_at": "2026-07-12T12:00:00Z"},
            {"created_at": "2026-07-05T12:00:00Z"},
            {"created_at": "fecha-invalida"},
        ]
    )
    assert len(filter_by_period(frame, period)) == 1
    assert count_previous_period(frame, period) == 1
    assert comparison_delta(3, 1) == "+2 vs. periodo anterior"


def test_custom_period_includes_last_selected_day() -> None:
    period = build_period_range(
        PERIOD_CUSTOM,
        (date(2026, 7, 13), date(2026, 7, 15)),
        reference=REFERENCE,
    )
    frame = pd.DataFrame(
        [
            {"created_at": "2026-07-13T05:00:00Z"},
            {"created_at": "2026-07-16T05:00:00Z"},
        ]
    )
    assert len(filter_by_period(frame, period)) == 1


def test_translations_priority_and_percentages() -> None:
    assert translate_result("preaprobado") == "Preaprobada"
    assert translate_request_status("draft") == "En progreso"
    assert translate_case_reason("user_requested_advisor") == "Solicitó un asesor"
    assert case_priority("user_requested_advisor")[0] == "Alta"
    assert case_priority("observed_result")[0] == "Media"
    assert case_priority("nuevo_motivo")[0] == "Revisar"
    assert percentage(4, 15) == 26.7
    assert percentage(1, 0) == 0.0


def test_dates_relative_time_and_masks() -> None:
    value = "2026-07-17T15:00:00Z"
    assert format_datetime(value) == "17/07/2026 · 10:00"
    assert relative_time(value, reference=REFERENCE) == "Hace 2 h"
    assert mask_cedula("0912345675") == "09******75"
    assert mask_phone("593991234567") == "5939****567"


def test_audit_payload_redaction_is_recursive() -> None:
    payload = {
        "cedula": "0912345675",
        "nested": {"api_key": "secret", "allowed": 42},
        "items": [{"token": "abc"}],
    }
    assert redact_payload(payload) == {
        "cedula": "[OCULTO]",
        "nested": {"api_key": "[OCULTO]", "allowed": 42},
        "items": [{"token": "[OCULTO]"}],
    }
