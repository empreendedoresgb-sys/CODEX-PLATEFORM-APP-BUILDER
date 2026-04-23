from __future__ import annotations

from orchestrator.contracts import (
    AuditEvent,
    ControlPlane,
    KpiFocus,
    LiveMetricsSnapshot,
    PolicyDecision,
    RiskLevel,
    SandboxTier,
    TaskEnvelope,
)

_TOOL_SANDBOX_MAP: dict[str, SandboxTier] = {
    "read": SandboxTier.READ_ONLY,
    "repo": SandboxTier.RESTRICTED_EXEC,
    "ci": SandboxTier.RESTRICTED_EXEC,
    "deployment": SandboxTier.FULLY_ISOLATED,
    "connector": SandboxTier.RESTRICTED_EXEC,
    "plugin": SandboxTier.RESTRICTED_EXEC,
}


def route_control_plane(kpi_focus: KpiFocus) -> ControlPlane:
    if kpi_focus == KpiFocus.PR_THROUGHPUT_MTTR:
        return ControlPlane.BUILD
    return ControlPlane.OPS


def route_control_plane_by_live_metrics(kpi_focus: KpiFocus, metrics: LiveMetricsSnapshot) -> ControlPlane:
    if kpi_focus == KpiFocus.PR_THROUGHPUT_MTTR:
        if metrics.pr_throughput < 5 or metrics.bug_mttr_hours > 24:
            return ControlPlane.BUILD
        return ControlPlane.OPS

    if metrics.autonomous_ops_success_rate < 0.8:
        return ControlPlane.OPS
    return ControlPlane.BUILD


def evaluate_policy(task: TaskEnvelope) -> PolicyDecision:
    reasons: list[str] = []
    sandbox = _TOOL_SANDBOX_MAP.get(task.tool_class, SandboxTier.RESTRICTED_EXEC)

    if task.tool_class == "plugin" and (not task.plugin_signature or not task.plugin_signature.startswith("sig:")):
        reasons.append("Unsigned plugin execution is blocked")

    invalid_permissions = [scope for scope in task.required_permissions if not scope.startswith("scope:")]
    if invalid_permissions:
        reasons.append("Permissions must use least-privilege scope:* notation")

    if task.risk_level == RiskLevel.CRITICAL and sandbox != SandboxTier.FULLY_ISOLATED:
        reasons.append("Critical-risk tasks require FULLY_ISOLATED sandbox")

    return PolicyDecision(allowed=len(reasons) == 0, sandbox_tier=sandbox, reasons=reasons)


def build_audit_event(actor: str, action: str, details: str) -> AuditEvent:
    return AuditEvent(actor=actor, action=action, details=details)
