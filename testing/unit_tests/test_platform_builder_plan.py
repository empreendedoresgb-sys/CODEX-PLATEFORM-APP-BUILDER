import pytest

from ai_assistant.platform_orchestrator import build_plan


def test_build_plan_hybrid_contains_sync_module() -> None:
    response = build_plan(
        prompt="Build a fintech SaaS with dashboard and analytics",
        mode="hybrid",
        deployment_target="cloud",
    )

    assert response["status"] == "ok"
    assert response["product"] == "APBUILDER.APP"
    assert "sync_inspector" in response["plan"]["modules"]
    assert response["plan"]["deployment_steps"][0] == "container_plan"
    assert len(response["plan"]["agents"]) == 7


def test_build_plan_rejects_invalid_mode() -> None:
    try:
        build_plan(prompt="Build", mode="invalid", deployment_target="cloud")
    except ValueError as exc:
        assert "Unsupported mode" in str(exc)
    else:
        raise AssertionError("Expected ValueError for unsupported mode")


def test_platform_build_plan_endpoint() -> None:
    pytest.importorskip("httpx")
    from fastapi.testclient import TestClient

    from api.rest_endpoints import app

    client = TestClient(app)
    response = client.post(
        "/v1/platform/build-plan",
        json={
            "prompt": "Create marketplace builder",
            "mode": "developer",
            "deployment_target": "hybrid",
        },
    )
    body = response.json()

    assert response.status_code == 200
    assert body["status"] == "ok"
    assert body["product"] == "APBUILDER.APP"
    assert body["plan"]["mode"] == "developer"
    assert "private_node_connector" in body["plan"]["deployment_steps"]
