from orchestrator.contracts import AgentArtifact


def run() -> list[AgentArtifact]:
    return [
        AgentArtifact(agent_id="ui_agent", artifact_type="ui", summary="Generated app shell and responsive layout"),
        AgentArtifact(agent_id="backend_agent", artifact_type="backend", summary="Generated API and service layer"),
        AgentArtifact(agent_id="data_agent", artifact_type="data_model", summary="Generated schema and migrations"),
    ]
