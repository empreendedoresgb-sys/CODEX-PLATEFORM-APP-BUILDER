import pytest


def _client():
    pytest.importorskip("fastapi")
    try:
        from fastapi.testclient import TestClient
    except RuntimeError as exc:
        pytest.skip(f"TestClient unavailable: {exc}")

    from api.rest_endpoints import app

    return TestClient(app)


def test_demo_route_serves_html() -> None:
    client = _client()
    response = client.get("/demo")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")


def test_root_redirects_to_demo() -> None:
    client = _client()
    response = client.get("/", follow_redirects=False)
    assert response.status_code in {307, 302}
    assert response.headers.get("location") == "/demo"
