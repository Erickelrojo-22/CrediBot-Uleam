"""Pruebas del endpoint de reply de handoff."""
from fastapi.testclient import TestClient

from app.main import app


def test_reply_handoff_requiere_password(monkeypatch):
    from app.api import deps

    monkeypatch.setattr(deps.settings, "admin_dashboard_password", "secret")

    client = TestClient(app)
    response = client.post(
        "/admin/handoff/case-1/reply",
        json={"message": "Hola"},
    )
    assert response.status_code == 401


def test_reply_handoff_ok(monkeypatch):
    from app.api import deps, routes_admin

    monkeypatch.setattr(deps.settings, "admin_dashboard_password", "secret")
    monkeypatch.setattr(
        routes_admin,
        "reply_as_advisor",
        lambda case_id, message: {
            "phone": "593999000111",
            "case": {"id": case_id, "status": "assigned"},
            "message": {"id": "msg-1", "content": message},
        },
    )

    client = TestClient(app)
    response = client.post(
        "/admin/handoff/case-1/reply",
        json={"message": "Hola asesor"},
        headers={"X-Admin-Password": "secret"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["phone"] == "593999000111"
    assert body["message"]["content"] == "Hola asesor"
