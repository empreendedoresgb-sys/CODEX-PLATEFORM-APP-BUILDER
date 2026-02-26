from __future__ import annotations

from orchestrator.agents import architect, generator, intent_parser, validator
from orchestrator.contracts import OrchestratorRunRequest, OrchestratorRunResult, RunStage
from orchestrator.repository import add_event, create_run, get_run, save_run
from orchestrator.state_machine import transition


def run_orchestrator(req: OrchestratorRunRequest) -> OrchestratorRunResult:
    run = create_run(req.prompt, req.target, req.mode, req.language_id)

    run.stage = transition(run.stage, RunStage.PARSED)
    run.artifacts.append(intent_parser.run(req.prompt))
    add_event(run.run_id, run.stage, "Intent parsed")

    run.stage = transition(run.stage, RunStage.PLANNED)
    run.artifacts.append(architect.run(req.target, req.mode))
    add_event(run.run_id, run.stage, "Architecture planned")

    run.stage = transition(run.stage, RunStage.GENERATED)
    run.artifacts.extend(generator.run())
    add_event(run.run_id, run.stage, "Artifacts generated")

    run.stage = transition(run.stage, RunStage.VERIFIED)
    run.blocking_issues = validator.run(req.prompt)
    if run.blocking_issues:
        run.stage = RunStage.FAILED
        run.quality_score = 0.0
        add_event(run.run_id, run.stage, "Run failed validation")
        save_run(run)
        return run

    run.stage = transition(run.stage, RunStage.DEPLOY_READY)
    run.preview_url = f"https://preview.apbuilder.app/{run.run_id}"
    run.quality_score = 1.0
    add_event(run.run_id, run.stage, "Run ready for deployment")

    save_run(run)
    return run


def deploy_run(run_id: str) -> OrchestratorRunResult:
    run = get_run(run_id)
    if run.stage != RunStage.DEPLOY_READY:
        raise ValueError("Run must be DEPLOY_READY before deployment")

    run.deploy_approved = True
    run.deploy_url = f"https://app.apbuilder.app/{run.run_id}"
    run.stage = transition(run.stage, RunStage.RELEASED)
    add_event(run.run_id, run.stage, "Run released")
    save_run(run)
    return run


def get_orchestrator_run(run_id: str) -> OrchestratorRunResult:
    return get_run(run_id)
