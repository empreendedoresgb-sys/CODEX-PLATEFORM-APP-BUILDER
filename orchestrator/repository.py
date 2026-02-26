from __future__ import annotations

import uuid

from orchestrator.contracts import OrchestratorRunResult, RunStage

_RUNS: dict[str, OrchestratorRunResult] = {}


def create_run(prompt: str, target: str, mode: str, language_id: str) -> OrchestratorRunResult:
    run_id = f"run_{uuid.uuid4().hex[:12]}"
    result = OrchestratorRunResult(
        run_id=run_id,
        stage=RunStage.RECEIVED,
        prompt=prompt,
        target=target,
        mode=mode,
        language_id=language_id,
        artifacts=[],
        preview_url=None,
        blocking_issues=[],
    )
    _RUNS[run_id] = result
    return result


def save_run(run: OrchestratorRunResult) -> None:
    _RUNS[run.run_id] = run


def get_run(run_id: str) -> OrchestratorRunResult:
    if run_id not in _RUNS:
        raise ValueError(f"Unknown run_id: {run_id}")
    return _RUNS[run_id]
