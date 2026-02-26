from __future__ import annotations

from orchestrator.contracts import AgentArtifact


def run(prompt: str) -> AgentArtifact:
    """Parse high-level user intent into a normalized requirements artifact."""
    return AgentArtifact(
        agent_id="intent_parser",
        artifact_type="requirements",
        summary=f"Parsed intent from prompt: {prompt[:80]}",
    )
