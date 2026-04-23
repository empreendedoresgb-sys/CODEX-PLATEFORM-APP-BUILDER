from __future__ import annotations

from orchestrator.contracts import OrchestratorRunResult, RunScorecard


def evaluate_run(run: OrchestratorRunResult) -> RunScorecard:
    quality = 1.0 if len(run.artifacts) >= 4 else 0.5
    security = 1.0 if (run.policy_decision is None or run.policy_decision.allowed) else 0.0
    kpi = 1.0 if run.selected_plane.value in {"BUILD", "OPS"} else 0.5

    reasons: list[str] = []
    if quality < 0.8:
        reasons.append("Insufficient generated artifacts for quality gate")
    if security < 0.8:
        reasons.append("Policy/security gate failed")
    if kpi < 0.8:
        reasons.append("KPI-plane alignment below target")

    pass_gate = len(reasons) == 0
    return RunScorecard(
        quality_score=quality,
        security_score=security,
        kpi_score=kpi,
        pass_gate=pass_gate,
        reasons=reasons,
    )
