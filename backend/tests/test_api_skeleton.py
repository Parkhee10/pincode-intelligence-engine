"""
Smoke tests for the API skeleton. These verify wiring (routes respond,
schemas validate) — not business logic correctness, since the underlying
logic is still placeholder. Real model-behavior tests get added in Stage 1.
"""
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "pincode-intelligence-engine"


def test_confidence_score_shape():
    response = client.get("/api/v1/confidence-score", params={"pincode": "560034"})
    assert response.status_code == 200
    body = response.json()
    assert "score" in body
    assert 0 <= body["score"] <= 100
    assert body["root_cause"] in ["first_mile", "last_mile", "unknown"]


def test_delivery_promise_shape():
    response = client.get("/api/v1/delivery-promise", params={"pincode": "560034"})
    assert response.status_code == 200
    body = response.json()
    assert body["estimated_min_days"] <= body["estimated_max_days"]


def test_nudge_triggers_on_risky_pincode():
    response = client.get(
        "/api/v1/nudge", params={"pincode": "560030", "order_value": 1500}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["nudge_triggered"] is True


def test_nudge_does_not_trigger_on_safe_pincode():
    response = client.get(
        "/api/v1/nudge", params={"pincode": "560034", "order_value": 1500}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["nudge_triggered"] is False
