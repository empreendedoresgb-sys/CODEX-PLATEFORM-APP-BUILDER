from orchestrator.contracts import AgentArtifact


def run(prompt: str) -> AgentArtifact:
    return AgentArtifact(
        agent_id="intent_parser",
        artifact_type="requirements",
        summary=f"Parsed intent from prompt: {prompt[:80]}",
    )
