from __future__ import annotations

from orchestrator.contracts import AgentArtifact


def run(target: str, mode: str) -> AgentArtifact:
    """Produce an architecture plan artifact for the selected deployment target and mode."""
    return AgentArtifact(
        agent_id="architect",
        artifact_type="architecture_plan",
        summary=f"Planned {target} architecture in {mode} mode",
    )
