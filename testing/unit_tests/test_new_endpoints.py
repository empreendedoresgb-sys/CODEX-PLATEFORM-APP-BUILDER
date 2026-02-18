import hashlib
import hmac
import json
import os

import pytest


def _client():
    pytest.importorskip("fastapi")
    try:
        from fastapi.testclient import TestClient
    except RuntimeError as exc:
        pytest.skip(f"TestClient unavailable: {exc}")

    from api.rest_endpoints import app

    return TestClient(app)


def test_files_import_accepts_supported_extension() -> None:
    client = _client()
    response = client.post("/v1/files/import", json={"filename": "story.mp3"})
    assert response.status_code == 200
    assert response.json()["data"]["extension"] == "mp3"


def test_files_import_rejects_unsupported_extension() -> None:
    client = _client()
    response = client.post("/v1/files/import", json={"filename": "archive.zip"})
    assert response.status_code == 400


def test_qr_create_and_stats_roundtrip() -> None:
    client = _client()
    created = client.post(
        "/v1/qr/create",
        json={"target_type": "voice", "target_id": "voice-1", "expires_in_seconds": 3600},
    )
    assert created.status_code == 200
    token = created.json()["data"]["token"]

    stats = client.get(f"/v1/qr/{token}/stats")
    assert stats.status_code == 200
    assert stats.json()["data"]["target_type"] == "voice"


def test_transcription_analyze_response_shape() -> None:
    client = _client()
    response = client.post(
        "/v1/transcription/analyze",
        json={"content": "Kriol KA na tabanka", "language_hint": "kriol"},
    )
    assert response.status_code == 200
    body = response.json()["data"]
    assert "language_detected" in body
    assert "ntopy4_compliance" in body


def test_billing_invoice_create_and_list() -> None:
    client = _client()
    created = client.post(
        "/v1/billing/invoices",
        json={"org_id": "org-1", "amount_cents": 1299, "currency": "USD"},
    )
    assert created.status_code == 200

    listed = client.get("/v1/billing/invoices", params={"org_id": "org-1"})
    assert listed.status_code == 200
    assert len(listed.json()["data"]) >= 1


def test_billing_webhook_signature_validation() -> None:
    client = _client()
    payload = {"event": "invoice.paid", "invoice_id": "inv-1"}
    secret = os.getenv("PAYMENT_WEBHOOK_SECRET", "dev-secret")
    signature = hmac.new(secret.encode(), json.dumps(payload, sort_keys=True).encode(), hashlib.sha256).hexdigest()

    ok = client.post("/v1/billing/webhook/payment", json=payload, headers={"X-Signature": signature})
    assert ok.status_code == 200

    bad = client.post("/v1/billing/webhook/payment", json=payload, headers={"X-Signature": "wrong"})
    assert bad.status_code == 403
