from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class RunStage(StrEnum):
    RECEIVED = "RECEIVED"
    PARSED = "PARSED"
    PLANNED = "PLANNED"
    GENERATED = "GENERATED"
    VERIFIED = "VERIFIED"
    DEPLOY_READY = "DEPLOY_READY"
    RELEASED = "RELEASED"
    FAILED = "FAILED"


class OrchestratorRunRequest(BaseModel):
    prompt: str = Field(min_length=3)
    target: str = "web"
    mode: str = "prototype"
    language_id: str = "en"


class AgentArtifact(BaseModel):
    agent_id: str
    artifact_type: str
    summary: str


class RunEvent(BaseModel):
    run_id: str
    stage: RunStage
    message: str


class OrchestratorRunResult(BaseModel):
    run_id: str
    stage: RunStage
    prompt: str
    target: str
    mode: str
    language_id: str
    artifacts: list[AgentArtifact] = Field(default_factory=list)
    preview_url: str | None = None
    deploy_url: str | None = None
    deploy_approved: bool = False
    quality_score: float = 0.0
    blocking_issues: list[str] = Field(default_factory=list)
