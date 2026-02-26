from __future__ import annotations

from orchestrator.contracts import RunStage

_ALLOWED_TRANSITIONS: dict[RunStage, tuple[RunStage, ...]] = {
    RunStage.RECEIVED: (RunStage.PARSED, RunStage.FAILED),
    RunStage.PARSED: (RunStage.PLANNED, RunStage.FAILED),
    RunStage.PLANNED: (RunStage.GENERATED, RunStage.FAILED),
    RunStage.GENERATED: (RunStage.VERIFIED, RunStage.FAILED),
    RunStage.VERIFIED: (RunStage.DEPLOY_READY, RunStage.FAILED),
    RunStage.DEPLOY_READY: (RunStage.RELEASED, RunStage.FAILED),
    RunStage.RELEASED: (),
    RunStage.FAILED: (),
}


def transition(current: RunStage, nxt: RunStage) -> RunStage:
    if nxt not in _ALLOWED_TRANSITIONS[current]:
        raise ValueError(f"Invalid transition: {current} -> {nxt}")
    return nxt
