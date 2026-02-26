from __future__ import annotations

from orchestrator.agents import architect, generator, intent_parser, validator
from orchestrator.contracts import OrchestratorRunRequest, OrchestratorRunResult, RunStage
from orchestrator.repository import create_run, get_run, save_run
from orchestrator.state_machine import transition


def run_orchestrator(req: OrchestratorRunRequest) -> OrchestratorRunResult:
    run = create_run(req.prompt, req.target, req.mode, req.language_id)

    run.stage = transition(run.stage, RunStage.PARSED)
    run.artifacts.append(intent_parser.run(req.prompt))

    run.stage = transition(run.stage, RunStage.PLANNED)
    run.artifacts.append(architect.run(req.target, req.mode))

    run.stage = transition(run.stage, RunStage.GENERATED)
    run.artifacts.extend(generator.run())

    run.stage = transition(run.stage, RunStage.VERIFIED)
    run.blocking_issues = validator.run(req.prompt)
    if run.blocking_issues:
        run.stage = RunStage.FAILED
        save_run(run)
        return run

    run.stage = transition(run.stage, RunStage.DEPLOY_READY)
    run.preview_url = f"https://preview.apbuilder.app/{run.run_id}"

    run.stage = transition(run.stage, RunStage.RELEASED)
    save_run(run)
    return run


def get_orchestrator_run(run_id: str) -> OrchestratorRunResult:
    return get_run(run_id)
