from orchestrator.contracts import OrchestratorRunRequest, RunStage
from orchestrator.master import get_orchestrator_run, run_orchestrator


def test_orchestrator_run_reaches_released() -> None:
    result = run_orchestrator(
        OrchestratorRunRequest(prompt="Build a CRM with dashboard", target="web", mode="prototype")
    )
    assert result.stage == RunStage.RELEASED
    assert result.preview_url is not None
    assert len(result.artifacts) >= 4


def test_orchestrator_run_fetch_by_id() -> None:
    result = run_orchestrator(OrchestratorRunRequest(prompt="Build analytics app"))
    fetched = get_orchestrator_run(result.run_id)
    assert fetched.run_id == result.run_id


def test_orchestrator_endpoint_if_fastapi_available() -> None:
    import pytest

    pytest.importorskip("httpx")
    from fastapi.testclient import TestClient

    from api.rest_endpoints import app

    client = TestClient(app)
    response = client.post(
        "/v1/orchestrator/run",
        json={"prompt": "Build invoice app", "target": "web", "mode": "prototype", "language_id": "en"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    run_id = body["run"]["run_id"]

    fetched = client.get(f"/v1/orchestrator/runs/{run_id}")
    assert fetched.status_code == 200
    assert fetched.json()["status"] == "ok"
