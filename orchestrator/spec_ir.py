from __future__ import annotations

from orchestrator.contracts import BuildType, ProjectSpecIR


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
    )
