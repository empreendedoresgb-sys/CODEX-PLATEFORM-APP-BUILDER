import pytest


def _client():
    pytest.importorskip("httpx")
    from fastapi.testclient import TestClient

    from api.rest_endpoints import app

    return TestClient(app)


def test_workspace_document_and_media_capabilities() -> None:
    client = _client()

    doc = client.post(
        "/v1/capabilities/workspace-document",
        json={
            "source_folder": "factures",
            "output_type": "SPREADSHEET",
            "title": "Invoice Analysis",
            "summary_goal": "Analyze invoices and produce charts",
        },
    )
    assert doc.status_code == 200
    assert doc.json()["artifact"]["output_path"].endswith(".xlsx")

    media = client.post(
        "/v1/capabilities/media-plan",
        json={
            "prompt": "Create Instagram post for a sports wearable launch",
            "media_type": "VIDEO",
            "brand_reference": "whoop-style-posts",
            "aspect_ratio": "4:5",
        },
    )
    assert media.status_code == 200
    assert "animate sequence" in media.json()["plan"]["generation_steps"]


def test_skills_mcp_plugin_and_automation_capabilities() -> None:
    client = _client()

    skill = client.post(
        "/v1/capabilities/skills",
        json={
            "name": "trend intelligence",
            "description": "Analyze competitors and market trends",
            "required_connectors": ["perplexity"],
            "instructions": ["prioritize recommendations", "cite evidence"],
        },
    )
    assert skill.status_code == 200
    assert skill.json()["invocation"] == "/trend-intelligence"

    connector = client.post(
        "/v1/capabilities/mcp-connectors",
        json={"name": "perplexity", "provider": "mcp", "scopes": ["scope:research.read"]},
    )
    assert connector.status_code == 200
    assert "scoped authorization" in connector.json()["security_note"]

    plugin = client.post(
        "/v1/capabilities/plugin-chains",
        json={
            "name": "creator intelligence",
            "skills": ["trend intelligence", "ppt branding"],
            "connectors": ["perplexity"],
            "output_goal": "branded presentation",
        },
    )
    assert plugin.status_code == 200
    assert plugin.json()["execution_plan"][-1] == "Produce: branded presentation"

    automation = client.post(
        "/v1/capabilities/automations",
        json={
            "title": "weekly reporting",
            "schedule": "MON 09:00",
            "trigger_condition": "calendar contains presentation des chiffres",
            "steps": ["read sales data", "create deck", "draft email"],
            "connectors": ["google-calendar", "gmail"],
        },
    )
    assert automation.status_code == 200
    assert automation.json()["runtime_policy"] == "human approval required"


def test_browser_and_mobile_capabilities() -> None:
    client = _client()

    browser = client.post(
        "/v1/capabilities/browser-task",
        json={
            "url": "https://example.test/expenses",
            "objective": "Enter expense rows from invoice data",
            "extracted_fields": ["date", "amount", "vendor"],
        },
    )
    assert browser.status_code == 200
    assert "Present extracted table for validation" in browser.json()["steps"]

    mobile = client.post(
        "/v1/capabilities/mobile-command",
        json={
            "command": "Build daily OpenAI trend tracker app",
            "project_id": "usage-codex",
            "requested_from": "mobile",
        },
    )
    assert mobile.status_code == 200
    assert mobile.json()["mobile_command"]["project_id"] == "usage-codex"
