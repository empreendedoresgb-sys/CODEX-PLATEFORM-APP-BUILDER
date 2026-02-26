from __future__ import annotations

from typing import Protocol

from orchestrator.contracts import AgentArtifact


class IntentParserAgent(Protocol):
    """Contract for prompt-to-requirements extraction agents."""

    def run(self, prompt: str) -> AgentArtifact: ...


class ArchitectAgent(Protocol):
    """Contract for architecture-planning agents."""

    def run(self, target: str, mode: str) -> AgentArtifact: ...


class GeneratorAgent(Protocol):
    """Contract for code/artifact generation agents."""

    def run(self) -> list[AgentArtifact]: ...


class ValidatorAgent(Protocol):
    """Contract for orchestration safety and quality validators."""

    def run(self, prompt: str) -> list[str]: ...
