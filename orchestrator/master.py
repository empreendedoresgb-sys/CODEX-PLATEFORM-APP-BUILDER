from __future__ import annotations

from orchestrator.agents import architect, generator, intent_parser, validator
from orchestrator.contracts import (
    OrchestratorRunRequest,
    OrchestratorRunResult,
    RunStage,
)
from orchestrator.control_plane import build_audit_event, evaluate_policy, route_control_plane
from orchestrator.evaluator import evaluate_run
from orchestrator.repository import add_event, create_run, get_run, save_run
from orchestrator.spec_ir import build_spec_ir
from orchestrator.state_machine import transition


def run_orchestrator(req: OrchestratorRunRequest) -> OrchestratorRunResult:
    run = create_run(req.prompt, req.target, req.mode, req.language_id, req.build_type)
    run.selected_plane = route_control_plane(req.kpi_focus)
    run.spec = req.spec or build_spec_ir(req.prompt, req.build_type, req.target)
    run.audit_trail.append(
        build_audit_event("control_plane_router", "route", f"Selected plane: {run.selected_plane}")
    )

    if req.task:
        decision = evaluate_policy(req.task)
        run.policy_decision = decision
        run.audit_trail.append(
            build_audit_event(req.task.agent_id, "policy_evaluation", f"allowed={decision.allowed} tier={decision.sandbox_tier}")
        )
        if not decision.allowed:
            run.stage = RunStage.FAILED
            run.blocking_issues.extend(decision.reasons)
            add_event(run.run_id, run.stage, "Policy gate blocked task")
            save_run(run)
            return run

    run.stage = transition(run.stage, RunStage.PARSED)
    run.artifacts.append(intent_parser.run(req.prompt))
    add_event(run.run_id, run.stage, "Intent parsed")

    run.stage = transition(run.stage, RunStage.PLANNED)
    run.artifacts.append(architect.run(req.target, req.mode, req.build_type))
    add_event(run.run_id, run.stage, "Architecture planned")

    run.stage = transition(run.stage, RunStage.GENERATED)
    run.artifacts.extend(generator.run(req.build_type))
    add_event(run.run_id, run.stage, "Artifacts generated")

    run.stage = transition(run.stage, RunStage.VERIFIED)
    run.blocking_issues.extend(validator.run(req.prompt))

    run.scorecard = evaluate_run(run)
    run.quality_score = run.scorecard.quality_score
    if not run.scorecard.pass_gate:
        run.blocking_issues.extend(run.scorecard.reasons)

    if run.blocking_issues:
        run.stage = RunStage.FAILED
        add_event(run.run_id, run.stage, "Run failed validation/evaluation gates")
        save_run(run)
        return run

    run.stage = transition(run.stage, RunStage.DEPLOY_READY)
    run.preview_url = f"https://preview.apbuilder.app/{run.run_id}"
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
