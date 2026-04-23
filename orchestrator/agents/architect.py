from __future__ import annotations

from orchestrator.contracts import AgentArtifact, BuildType


def run(target: str, mode: str, build_type: BuildType) -> AgentArtifact:
    """Produce an architecture plan artifact for the selected deployment target and mode."""
    return AgentArtifact(
        agent_id="architect",
        artifact_type="architecture_plan",
        summary=f"Planned {build_type} on {target} architecture in {mode} mode",
    )
