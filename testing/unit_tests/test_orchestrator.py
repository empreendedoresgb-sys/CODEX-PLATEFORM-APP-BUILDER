from orchestrator.contracts import BuildType, KpiFocus, OrchestratorRunRequest, RunStage, TaskEnvelope
from orchestrator.master import get_orchestrator_run, run_orchestrator


def test_orchestrator_run_reaches_deploy_ready() -> None:
    result = run_orchestrator(
        OrchestratorRunRequest(prompt="Build a CRM with dashboard", target="web", mode="prototype", build_type=BuildType.MOBILE_APP)
    )
    assert result.stage == RunStage.DEPLOY_READY
    assert result.preview_url is not None
    assert len(result.artifacts) >= 5
    assert result.selected_plane.value == "BUILD"
    assert result.build_type == BuildType.MOBILE_APP
    assert any("mobile" in item.summary.lower() for item in result.artifacts)


def test_orchestrator_run_fetch_by_id() -> None:
    result = run_orchestrator(OrchestratorRunRequest(prompt="Build analytics app with BI reports"))
    fetched = get_orchestrator_run(result.run_id)
    assert fetched.run_id == result.run_id


def test_orchestrator_policy_gates_unsigned_plugins() -> None:
    result = run_orchestrator(
        OrchestratorRunRequest(
            prompt="Build commerce app with payment workflows",
            task=TaskEnvelope(
                intent="Deploy external plugin task",
                rollback_plan="Disable plugin and roll back deployment.",
                required_permissions=["scope:repo.write"],
                tool_class="plugin",
                plugin_signature="",
            ),
        )
    )
    assert result.stage == RunStage.FAILED
    assert result.policy_decision is not None
    assert result.policy_decision.allowed is False


def test_orchestrator_short_prompt_validation() -> None:
    import pytest

    with pytest.raises(Exception):
        run_orchestrator(OrchestratorRunRequest(prompt="Hi"))


def test_orchestrator_endpoint_if_fastapi_available() -> None:
    import pytest

    pytest.importorskip("httpx")
    from fastapi.testclient import TestClient

    from api.rest_endpoints import app

    client = TestClient(app)
    response = client.post(
        "/v1/orchestrator/run",
        json={
            "prompt": "Build invoice app with approval workflows",
            "target": "web",
            "mode": "prototype",
            "language_id": "en",
            "kpi_focus": KpiFocus.PR_THROUGHPUT_MTTR,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    run_id = body["run"]["run_id"]

    fetched = client.get(f"/v1/orchestrator/runs/{run_id}")
    assert fetched.status_code == 200
    assert fetched.json()["status"] == "ok"

    deployed = client.post(f"/v1/orchestrator/runs/{run_id}/deploy")
    assert deployed.status_code == 200
    assert deployed.json()["status"] == "ok"
    assert deployed.json()["run"]["stage"] == RunStage.RELEASED


def test_control_plane_and_policy_endpoints() -> None:
    import pytest

    pytest.importorskip("httpx")
    from fastapi.testclient import TestClient

    from api.rest_endpoints import app

    client = TestClient(app)

    route = client.post("/v1/control-plane/route", json={"kpi_focus": "CROSS_SYSTEM_AUTONOMY"})
    assert route.status_code == 200
    assert route.json()["selected_plane"] == "OPS"

    decision = client.post(
        "/v1/policy/evaluate",
        json={
            "intent": "Push plugin release",
            "risk_level": "HIGH",
            "required_permissions": ["repo.write"],
            "rollback_plan": "Revert release and disable plugin",
            "tool_class": "plugin",
            "plugin_signature": "",
            "agent_id": "release_agent",
        },
    )
    assert decision.status_code == 200
    assert decision.json()["decision"]["allowed"] is False


def test_orchestrator_deploy_not_ready() -> None:
    import pytest

    pytest.importorskip("httpx")
    from fastapi.testclient import TestClient

    from api.rest_endpoints import app

    client = TestClient(app)
    response = client.post(
        "/v1/orchestrator/run",
        json={"prompt": "bad", "target": "web", "mode": "prototype", "language_id": "en"},
    )
    run_id = response.json()["run"]["run_id"]

    deployed = client.post(f"/v1/orchestrator/runs/{run_id}/deploy")
    assert deployed.status_code == 200
    assert deployed.json()["status"] == "failed"
