from __future__ import annotations

from dataclasses import dataclass

from core.platform_modes import get_mode


@dataclass(frozen=True)
class AgentTask:
    agent: str
    objective: str


_DEPLOYMENT_MATRIX: dict[str, tuple[str, ...]] = {
    "cloud": ("container_plan", "autoscaling_profile", "managed_observability"),
    "hybrid": ("container_plan", "private_node_connector", "compliance_controls"),
    "edge": ("container_plan", "edge_bundle", "offline_fallback"),
}


_BASE_AGENT_TASKS: tuple[AgentTask, ...] = (
    AgentTask("architect", "Define modular domain boundaries and service contracts."),
    AgentTask("ui", "Generate responsive shell with accessibility and role-aware navigation."),
    AgentTask("backend", "Design APIs, data model, and auth policies for the requested product."),
    AgentTask("security", "Run OWASP-oriented threat checks and recommend hardening."),
    AgentTask("devops", "Prepare CI/CD, observability, and release checks."),
    AgentTask("optimization", "Profile performance, runtime cost, and dependency footprint."),
    AgentTask("monetization", "Propose pricing levers and growth loops aligned to target users."),
)


def build_plan(prompt: str, mode: str, deployment_target: str) -> dict:
    if not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    selected_mode = get_mode(mode)
    deployment_key = deployment_target.lower().strip()
    if deployment_key not in _DEPLOYMENT_MATRIX:
        valid = ", ".join(sorted(_DEPLOYMENT_MATRIX))
        raise ValueError(f"Unsupported deployment target '{deployment_target}'. Supported targets: {valid}.")

    agent_plan = [
        {
            "agent": task.agent,
            "objective": task.objective,
            "status": "planned",
        }
        for task in _BASE_AGENT_TASKS
    ]

    return {
        "status": "ok",
        "product": "APBUILDER.APP",
        "plan": {
            "prompt": prompt,
            "mode": selected_mode.name,
            "mode_description": selected_mode.description,
            "modules": list(selected_mode.modules),
            "deployment_target": deployment_key,
            "deployment_steps": list(_DEPLOYMENT_MATRIX[deployment_key]),
            "agents": agent_plan,
            "validation": {
                "state_guards": True,
                "error_boundaries": True,
                "pre_deploy_checks": True,
            },
        },
    }
