from __future__ import annotations

from orchestrator.contracts import BuildType, CapabilityType, ProjectSpecIR

_BUILD_CAPABILITIES: dict[BuildType, list[CapabilityType]] = {
    BuildType.APP: [
        CapabilityType.DOCUMENT,
        CapabilityType.DESIGN_SYSTEM,
        CapabilityType.AUTOMATION,
        CapabilityType.BROWSER_TASK,
        CapabilityType.JOB_TEMPLATE,
        CapabilityType.CHAT,
        CapabilityType.ARTIFACT,
    ],
    BuildType.SOFTWARE: [
        CapabilityType.DOCUMENT,
        CapabilityType.SKILL,
        CapabilityType.PLUGIN_CHAIN,
        CapabilityType.AGENT_BLUEPRINT,
        CapabilityType.JOB_TEMPLATE,
        CapabilityType.MODEL_ROUTING,
    ],
    BuildType.MOBILE_APP: [
        CapabilityType.MOBILE_REQUEST,
        CapabilityType.DESIGN_SYSTEM,
        CapabilityType.AUTOMATION,
        CapabilityType.IMAGE,
        CapabilityType.SPEECH,
    ],
    BuildType.WEB_PAGE: [
        CapabilityType.WEB_AUDIT,
        CapabilityType.DESIGN_SYSTEM,
        CapabilityType.IMAGE,
        CapabilityType.MOCKUP,
    ],
    BuildType.WEBSITE: [
        CapabilityType.WEB_AUDIT,
        CapabilityType.DESIGN_SYSTEM,
        CapabilityType.DOCUMENT,
        CapabilityType.AUTOMATION,
        CapabilityType.JOB_TEMPLATE,
        CapabilityType.WEB_SEARCH,
        CapabilityType.SLIDES,
    ],
    BuildType.AGENT: [
        CapabilityType.SKILL,
        CapabilityType.MCP_CONNECTOR,
        CapabilityType.PLUGIN_CHAIN,
        CapabilityType.AGENT_BLUEPRINT,
        CapabilityType.JOB_TEMPLATE,
        CapabilityType.EXTENDED_THINKING,
        CapabilityType.RESEARCH,
        CapabilityType.REMOTE_DISPATCH,
    ],
    BuildType.BOT: [
        CapabilityType.MCP_CONNECTOR,
        CapabilityType.AUTOMATION,
        CapabilityType.BROWSER_TASK,
        CapabilityType.AGENT_BLUEPRINT,
        CapabilityType.JOB_TEMPLATE,
        CapabilityType.COMPUTER_USE,
        CapabilityType.BROWSER_EXTENSION,
    ],
}


def build_spec_ir(prompt: str, build_type: BuildType, target_runtime: str) -> ProjectSpecIR:
    project_name = " ".join(prompt.split()[:4]) or "apbuilder-project"
    if build_type == BuildType.MOBILE_APP:
        frontend = "react-native"
        backend = "python-fastapi"
        infra = "cloud-edge"
    elif build_type == BuildType.AGENT:
        frontend = "nextjs-dashboard"
        backend = "python-fastapi-workers"
        infra = "cloud"
    elif build_type == BuildType.BOT:
        frontend = "admin-console"
        backend = "python-webhooks"
        infra = "cloud"
    else:
        frontend = "react"
        backend = "python-fastapi"
        infra = "cloud"

    return ProjectSpecIR(
        project_name=project_name,
        build_type=build_type,
        target_runtime=target_runtime,
        frontend_stack=frontend,
        backend_stack=backend,
        infra_profile=infra,
        capabilities=_BUILD_CAPABILITIES.get(build_type, []),
    )
