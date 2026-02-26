from __future__ import annotations

import uuid

from orchestrator.contracts import OrchestratorRunResult, RunEvent, RunStage

_RUNS: dict[str, OrchestratorRunResult] = {}
_EVENTS: dict[str, list[RunEvent]] = {}


def create_run(prompt: str, target: str, mode: str, language_id: str) -> OrchestratorRunResult:
    run_id = f"run_{uuid.uuid4().hex[:12]}"
    result = OrchestratorRunResult(
        run_id=run_id,
        stage=RunStage.RECEIVED,
        prompt=prompt,
        target=target,
        mode=mode,
        language_id=language_id,
    )
    _RUNS[run_id] = result
    _EVENTS[run_id] = [RunEvent(run_id=run_id, stage=RunStage.RECEIVED, message="Run created")]
    return result


def save_run(run: OrchestratorRunResult) -> None:
    _RUNS[run.run_id] = run


def get_run(run_id: str) -> OrchestratorRunResult:
    if run_id not in _RUNS:
        raise ValueError(f"Unknown run_id: {run_id}")
    return _RUNS[run_id]


def add_event(run_id: str, stage: RunStage, message: str) -> None:
    if run_id not in _EVENTS:
        _EVENTS[run_id] = []
    _EVENTS[run_id].append(RunEvent(run_id=run_id, stage=stage, message=message))


def get_events(run_id: str) -> list[RunEvent]:
    if run_id not in _RUNS:
        raise ValueError(f"Unknown run_id: {run_id}")
    return list(_EVENTS.get(run_id, []))
