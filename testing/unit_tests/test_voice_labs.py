import pytest

from monetization import get_tier
from voice.labs.template_manager import list_templates


def test_templates_list_non_empty() -> None:
    templates = list_templates()
    assert len(templates) >= 3


def test_get_tier_enterprise() -> None:
    tier = get_tier("enterprise")
    assert tier["voice_library_size"] == 400


def test_get_tier_unknown_fails() -> None:
    with pytest.raises(ValueError):
        get_tier("invalid")


def test_api_templates_endpoint_if_fastapi_available() -> None:
    fastapi = pytest.importorskip("fastapi")
    pytest.importorskip("httpx")
    from fastapi.testclient import TestClient
    from api.rest_endpoints import app

    assert fastapi is not None
    client = TestClient(app)
    response = client.get("/v1/voice/templates")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
