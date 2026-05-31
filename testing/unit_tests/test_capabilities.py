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


def test_design_system_agent_blueprint_and_job_template_capabilities() -> None:
    client = _client()

    design_system = client.post(
        "/v1/capabilities/design-system",
        json={
            "brand_name": "APBUILDER",
            "product_type": "WEBSITE",
            "visual_direction": "AI-first enterprise builder",
            "primary_color": "#2563eb",
            "secondary_color": "#14b8a6",
        },
    )
    assert design_system.status_code == 200
    design = design_system.json()["design_system"]
    assert design["tokens"]["color.primary"] == "#2563eb"
    assert "PreviewWorkbench" in design["components"]

    agent = client.post(
        "/v1/capabilities/agent-blueprint",
        json={
            "objective": "Build and secure SaaS release pipeline",
            "tasks": ["generate app", "run tests", "prepare release"],
            "preferred_connectors": ["github", "slack"],
            "risk_level": "HIGH",
        },
    )
    assert agent.status_code == 200
    blueprint = agent.json()["agent_blueprint"]
    assert "github" in blueprint["tools"]
    assert "human approval required before external side effects" in blueprint["guardrails"]

    job = client.post(
        "/v1/capabilities/job-template",
        json={
            "name": "nightly quality review",
            "trigger": "0 2 * * *",
            "task": "run evaluator and summarize regressions",
            "expected_output": "quality report",
        },
    )
    assert job.status_code == 200
    template = job.json()["job_template"]
    assert template["approval_required"] is True
    assert "load project context and Project Spec IR" in template["runbook"]


def test_interaction_suite_maps_claude_style_capabilities() -> None:
    client = _client()

    response = client.post(
        "/v1/capabilities/interaction-suite",
        json={
            "product_goal": "Build the most advanced AI app builder",
            "autonomy_level": "supervised",
            "target_channels": ["web", "mobile", "desktop"],
            "include_remote_dispatch": True,
        },
    )
    assert response.status_code == 200
    suite = response.json()["interaction_suite"]
    module_names = {module["name"] for module in suite["modules"]}
    capability_types = {module["capability_type"] for module in suite["modules"]}

    assert "Ask / Chat" in module_names
    assert "Mic / Speech" in module_names
    assert "Click / Computer Use" in module_names
    assert "Browse / Browser Extension" in module_names
    assert "REMOTE_DISPATCH" in capability_types
    assert "DEEP_MODEL" in capability_types
    assert "SPEED_OPTIMIZATION" in capability_types
    assert "policy approval before side effects" in suite["quality_gates"]
    assert len(suite["modules"]) >= 20


def test_foundation_suite_includes_auth_payments_and_rbac() -> None:
    client = _client()

    response = client.post(
        "/v1/capabilities/foundation-suite",
        json={
            "product_goal": "Launch APBUILDER as a paid AI app builder",
            "launch_tier": "pro",
            "include_payments": True,
            "include_enterprise": True,
        },
    )
    assert response.status_code == 200
    suite = response.json()["foundation_suite"]
    capability_types = {foundation["capability_type"] for foundation in suite["foundations"]}
    data_tables = {table for foundation in suite["foundations"] for table in foundation["data_tables"]}

    assert "AUTHENTICATION" in capability_types
    assert "BILLING" in capability_types
    assert "TEAM_RBAC" in capability_types
    assert "auth_identities" in data_tables
    assert "billing_accounts" in data_tables
    assert "payment_events" in data_tables
    assert "billing blueprint avoids raw card storage and requires signed webhooks" in suite["readiness_checks"]
