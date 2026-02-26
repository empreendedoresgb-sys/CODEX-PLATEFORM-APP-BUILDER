from orchestrator.contracts import AgentArtifact


def run(target: str, mode: str) -> AgentArtifact:
    return AgentArtifact(
        agent_id="architect",
        artifact_type="architecture_plan",
        summary=f"Planned {target} architecture in {mode} mode",
    )
