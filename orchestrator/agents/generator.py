from __future__ import annotations

from orchestrator.contracts import AgentArtifact, BuildType

_DOMAIN_ARTIFACTS: dict[BuildType, str] = {
    BuildType.APP: "Generated app shell, APIs, and domain services",
    BuildType.SOFTWARE: "Generated backend services, workers, and release scripts",
    BuildType.MOBILE_APP: "Generated mobile UI, API client, and offline sync modules",
    BuildType.WEB_PAGE: "Generated landing page layout, SEO metadata, and analytics tags",
    BuildType.WEBSITE: "Generated multi-page frontend, CMS hooks, and routing",
    BuildType.AGENT: "Generated agent planner, tool router, and memory interfaces",
    BuildType.BOT: "Generated bot command handlers, webhook adapters, and moderation rules",
}


def run(build_type: BuildType) -> list[AgentArtifact]:
    """Generate baseline multi-domain artifacts for UI, backend, and data layers."""
    domain_summary = _DOMAIN_ARTIFACTS.get(build_type, _DOMAIN_ARTIFACTS[BuildType.WEBSITE])
    return [
        AgentArtifact(agent_id="ui_agent", artifact_type="ui", summary="Generated app shell and responsive layout"),
        AgentArtifact(agent_id="backend_agent", artifact_type="backend", summary="Generated API and service layer"),
        AgentArtifact(agent_id="data_agent", artifact_type="data_model", summary="Generated schema and migrations"),
        AgentArtifact(agent_id="domain_agent", artifact_type="domain_package", summary=domain_summary),
    ]
