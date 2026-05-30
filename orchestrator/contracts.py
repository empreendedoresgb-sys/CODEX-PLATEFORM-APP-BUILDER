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


class BuildType(StrEnum):
    APP = "APP"
    SOFTWARE = "SOFTWARE"
    MOBILE_APP = "MOBILE_APP"
    WEB_PAGE = "WEB_PAGE"
    WEBSITE = "WEBSITE"
    AGENT = "AGENT"
    BOT = "BOT"


class ControlPlane(StrEnum):
    BUILD = "BUILD"
    OPS = "OPS"
    POLICY = "POLICY"


class KpiFocus(StrEnum):
    PR_THROUGHPUT_MTTR = "PR_THROUGHPUT_MTTR"
    CROSS_SYSTEM_AUTONOMY = "CROSS_SYSTEM_AUTONOMY"


class RiskLevel(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class SandboxTier(StrEnum):
    READ_ONLY = "READ_ONLY"
    RESTRICTED_EXEC = "RESTRICTED_EXEC"
    FULLY_ISOLATED = "FULLY_ISOLATED"


class CapabilityType(StrEnum):
    DOCUMENT = "DOCUMENT"
    SPREADSHEET = "SPREADSHEET"
    WEB_AUDIT = "WEB_AUDIT"
    SKILL = "SKILL"
    MCP_CONNECTOR = "MCP_CONNECTOR"
    PLUGIN_CHAIN = "PLUGIN_CHAIN"
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    AUTOMATION = "AUTOMATION"
    BROWSER_TASK = "BROWSER_TASK"
    MOBILE_REQUEST = "MOBILE_REQUEST"
    DESIGN_SYSTEM = "DESIGN_SYSTEM"
    AGENT_BLUEPRINT = "AGENT_BLUEPRINT"
    JOB_TEMPLATE = "JOB_TEMPLATE"


class ProjectSpecIR(BaseModel):
    project_name: str = Field(min_length=2)
    build_type: BuildType
    target_runtime: str = "web"
    frontend_stack: str = "react"
    backend_stack: str = "python-fastapi"
    infra_profile: str = "cloud"
    quality_gates: list[str] = Field(default_factory=lambda: ["tests", "security", "kpi"])
    capabilities: list[CapabilityType] = Field(default_factory=list)


class TaskEnvelope(BaseModel):
    intent: str = Field(min_length=3)
    risk_level: RiskLevel = RiskLevel.MEDIUM
    required_permissions: list[str] = Field(default_factory=list)
    rollback_plan: str = Field(min_length=3)
    tool_class: str = "repo"
    plugin_signature: str | None = None
    agent_id: str = "release_agent"


class PolicyDecision(BaseModel):
    allowed: bool
    sandbox_tier: SandboxTier
    reasons: list[str] = Field(default_factory=list)


class AuditEvent(BaseModel):
    actor: str
    action: str
    details: str


class LiveMetricsSnapshot(BaseModel):
    pr_throughput: float = 0.0
    bug_mttr_hours: float = 0.0
    autonomous_ops_success_rate: float = 0.0


class RunScorecard(BaseModel):
    quality_score: float
    security_score: float
    kpi_score: float
    pass_gate: bool
    reasons: list[str] = Field(default_factory=list)


class OrchestratorRunRequest(BaseModel):
    prompt: str = Field(min_length=3)
    target: str = "web"
    mode: str = "prototype"
    language_id: str = "en"
    build_type: BuildType = BuildType.WEBSITE
    kpi_focus: KpiFocus = KpiFocus.PR_THROUGHPUT_MTTR
    task: TaskEnvelope | None = None
    spec: ProjectSpecIR | None = None


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
    build_type: BuildType = BuildType.WEBSITE
    selected_plane: ControlPlane = ControlPlane.BUILD
    artifacts: list[AgentArtifact] = Field(default_factory=list)
    preview_url: str | None = None
    deploy_url: str | None = None
    deploy_approved: bool = False
    quality_score: float = 0.0
    blocking_issues: list[str] = Field(default_factory=list)
    policy_decision: PolicyDecision | None = None
    audit_trail: list[AuditEvent] = Field(default_factory=list)
    spec: ProjectSpecIR | None = None
    scorecard: RunScorecard | None = None


class WorkspaceDocumentRequest(BaseModel):
    source_folder: str = "workspace"
    output_type: CapabilityType = CapabilityType.DOCUMENT
    title: str
    summary_goal: str


class WorkspaceDocumentResult(BaseModel):
    artifact_type: CapabilityType
    title: str
    output_path: str
    sections: list[str]


class SkillDefinition(BaseModel):
    name: str = Field(min_length=2)
    description: str
    required_connectors: list[str] = Field(default_factory=list)
    required_skills: list[str] = Field(default_factory=list)
    instructions: list[str] = Field(default_factory=list)


class MCPConnectorDefinition(BaseModel):
    name: str = Field(min_length=2)
    provider: str
    scopes: list[str] = Field(default_factory=list)
    endpoint: str | None = None


class PluginChainDefinition(BaseModel):
    name: str = Field(min_length=2)
    skills: list[str] = Field(min_length=1)
    connectors: list[str] = Field(default_factory=list)
    output_goal: str


class MediaGenerationRequest(BaseModel):
    prompt: str
    media_type: CapabilityType = CapabilityType.IMAGE
    brand_reference: str | None = None
    aspect_ratio: str = "4:5"


class MediaGenerationPlan(BaseModel):
    media_type: CapabilityType
    prompt: str
    generation_steps: list[str]
    quality_checks: list[str]


class AutomationRecipe(BaseModel):
    title: str = Field(min_length=2)
    schedule: str
    trigger_condition: str
    steps: list[str] = Field(min_length=1)
    connectors: list[str] = Field(default_factory=list)
    approval_required: bool = True


class BrowserTaskPlan(BaseModel):
    url: str
    objective: str
    extracted_fields: list[str] = Field(default_factory=list)
    requires_human_validation: bool = True


class MobileCommandRequest(BaseModel):
    command: str
    project_id: str = "default"
    requested_from: str = "mobile"


class MobileCommandPlan(BaseModel):
    command: str
    project_id: str
    queued_actions: list[str]


class DesignSystemRequest(BaseModel):
    brand_name: str = Field(min_length=2)
    product_type: BuildType = BuildType.WEBSITE
    visual_direction: str = "modern, accessible, conversion-focused"
    primary_color: str = "#2563eb"
    secondary_color: str = "#0f172a"


class DesignSystemBlueprint(BaseModel):
    brand_name: str
    tokens: dict[str, str]
    components: list[str]
    accessibility_checks: list[str]
    implementation_notes: list[str]


class AgentBlueprintRequest(BaseModel):
    objective: str = Field(min_length=3)
    tasks: list[str] = Field(min_length=1)
    preferred_connectors: list[str] = Field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.MEDIUM


class AgentBlueprint(BaseModel):
    name: str
    objective: str
    role: str
    tools: list[str]
    job_templates: list[str]
    guardrails: list[str]


class JobTemplateRequest(BaseModel):
    name: str = Field(min_length=2)
    trigger: str
    task: str
    expected_output: str
    approval_required: bool = True


class JobTemplate(BaseModel):
    name: str
    trigger: str
    task: str
    expected_output: str
    runbook: list[str]
    approval_required: bool
