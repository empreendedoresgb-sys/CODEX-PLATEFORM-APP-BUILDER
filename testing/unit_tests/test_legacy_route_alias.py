import pytest


def _client():
    pytest.importorskip("fastapi")
    try:
        from fastapi.testclient import TestClient
    except RuntimeError as exc:
        pytest.skip(f"TestClient unavailable: {exc}")

    from api.rest_endpoints import app

    return TestClient(app)


def test_legacy_typo_route_alias_matches_generate_text() -> None:
    client = _client()
    payload = {"input": "Kriol KA na tira boka na binhu", "mode": "kriol", "ntopy4": True, "validation": True}

    canonical = client.post("/v1/generate/text", json=payload)
    legacy = client.post("/v1/generhate/text", json=payload)

    assert canonical.status_code == 200
    assert legacy.status_code == 200
    assert canonical.json()["status"] == legacy.json()["status"] == "ok"
