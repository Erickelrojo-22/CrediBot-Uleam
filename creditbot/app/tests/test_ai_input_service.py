"""Pruebas de normalización de entradas con IA."""
from app.services import ai_input_service


def test_local_normalize_un_ano_to_12_months():
    assert ai_input_service._local_normalize("term_months", "un año") == "12"


def test_local_normalize_si_to_confirmation_1():
    assert ai_input_service._local_normalize("confirmation", "sí") == "1"


def test_local_normalize_precalificar_to_menu_1():
    assert ai_input_service._local_normalize("menu_option", "quiero precalificar") == "1"


def test_normalize_user_input_uses_local_rules_without_api_key(monkeypatch):
    monkeypatch.setattr(ai_input_service.settings, "openai_api_key", "")
    assert ai_input_service.normalize_user_input("dos años", "term_months") == "24"
