from __future__ import annotations

from orchestrator.contracts import (
    AgentBlueprint,
    AgentBlueprintRequest,
    AutomationRecipe,
    BrowserTaskPlan,
    CapabilityType,
    DesignSystemBlueprint,
    DesignSystemRequest,
    JobTemplate,
    JobTemplateRequest,
    MCPConnectorDefinition,
    MediaGenerationPlan,
    MediaGenerationRequest,
    MobileCommandPlan,
    MobileCommandRequest,
    PluginChainDefinition,
    RiskLevel,
    SkillDefinition,
    WorkspaceDocumentRequest,
    WorkspaceDocumentResult,
)


def build_workspace_document(req: WorkspaceDocumentRequest) -> WorkspaceDocumentResult:
    extension = {
        CapabilityType.SPREADSHEET: "xlsx",
        CapabilityType.DOCUMENT: "docx",
        CapabilityType.WEB_AUDIT: "html",
    }.get(req.output_type, "md")
    return WorkspaceDocumentResult(
        artifact_type=req.output_type,
        title=req.title,
        output_path=f"/generated/{req.title.lower().replace(' ', '-')}.{extension}",
        sections=[
            "Executive summary",
            f"Source folder analysis: {req.source_folder}",
            f"Goal: {req.summary_goal}",
            "Recommended next actions",
        ],
    )


def register_skill(definition: SkillDefinition) -> dict:
    return {
        "status": "ok",
        "skill": definition.model_dump(),
        "invocation": f"/{definition.name.lower().replace(' ', '-')}",
    }


def register_mcp_connector(definition: MCPConnectorDefinition) -> dict:
    return {
        "status": "ok",
        "connector": definition.model_dump(),
        "security_note": "Connector requires scoped authorization before execution.",
    }


def build_plugin_chain(definition: PluginChainDefinition) -> dict:
    steps = [f"Run skill: {skill}" for skill in definition.skills]
    steps.extend(f"Use connector: {connector}" for connector in definition.connectors)
    steps.append(f"Produce: {definition.output_goal}")
    return {"status": "ok", "plugin": definition.model_dump(), "execution_plan": steps}


def plan_media_generation(req: MediaGenerationRequest) -> MediaGenerationPlan:
    checks = ["brand consistency", "format fit", "safety review"]
    if req.media_type == CapabilityType.VIDEO:
        steps = ["derive storyboard", "generate keyframes", "animate sequence", "render short-form video"]
        checks.append("temporal consistency")
    else:
        steps = ["extract brand cues", "compose prompt", "generate image", "prepare social-ready variant"]
    if req.brand_reference:
        steps.insert(0, f"analyze brand reference: {req.brand_reference}")
    return MediaGenerationPlan(
        media_type=req.media_type,
        prompt=req.prompt,
        generation_steps=steps,
        quality_checks=checks,
    )


def create_automation(recipe: AutomationRecipe) -> dict:
    return {
        "status": "ok",
        "automation": recipe.model_dump(),
        "runtime_policy": "human approval required" if recipe.approval_required else "autonomous execution allowed",
    }


def plan_browser_task(plan: BrowserTaskPlan) -> dict:
    return {
        "status": "ok",
        "browser_task": plan.model_dump(),
        "steps": [
            f"Open {plan.url}",
            "Extract requested fields",
            "Present extracted table for validation",
            "Submit only after validation" if plan.requires_human_validation else "Submit automatically",
        ],
    }


def queue_mobile_command(req: MobileCommandRequest) -> MobileCommandPlan:
    return MobileCommandPlan(
        command=req.command,
        project_id=req.project_id,
        queued_actions=[
            "sync command to active workspace",
            "resolve project context",
            "execute via orchestrator when workstation is available",
        ],
    )


def build_design_system(req: DesignSystemRequest) -> DesignSystemBlueprint:
    return DesignSystemBlueprint(
        brand_name=req.brand_name,
        tokens={
            "color.primary": req.primary_color,
            "color.secondary": req.secondary_color,
            "radius.card": "16px",
            "shadow.elevated": "0 18px 40px rgba(15, 23, 42, 0.14)",
            "font.body": "Inter, system-ui, sans-serif",
            "motion.default": "180ms ease-out",
        },
        components=[
            "AppShell",
            "TopNavigation",
            "HeroSection",
            "FeatureCard",
            "PricingTier",
            "AgentActivityPanel",
            "PreviewWorkbench",
        ],
        accessibility_checks=[
            "WCAG AA contrast on primary/secondary colors",
            "keyboard focus states for all interactive components",
            "responsive tablet/mobile layouts",
            "reduced-motion fallback for animations",
        ],
        implementation_notes=[
            f"Optimize visual language for {req.product_type} builds.",
            f"Direction: {req.visual_direction}",
            "Export tokens to CSS variables, Tailwind config, and design handoff JSON.",
        ],
    )


def build_agent_blueprint(req: AgentBlueprintRequest) -> AgentBlueprint:
    slug = req.objective.lower().replace(" ", "-")[:48].strip("-") or "agent"
    tools = ["orchestrator.run", "policy.evaluate", "events.stream"]
    tools.extend(req.preferred_connectors)
    guardrails = [
        "least-privilege scopes only",
        "audit every action",
        "rollback plan required before execution",
    ]
    if req.risk_level in {RiskLevel.HIGH, RiskLevel.CRITICAL}:
        guardrails.append("human approval required before external side effects")
    return AgentBlueprint(
        name=f"{slug}-agent",
        objective=req.objective,
        role="autonomous builder specialist",
        tools=tools,
        job_templates=[f"job:{task.lower().replace(' ', '-')}" for task in req.tasks],
        guardrails=guardrails,
    )


def build_job_template(req: JobTemplateRequest) -> JobTemplate:
    return JobTemplate(
        name=req.name,
        trigger=req.trigger,
        task=req.task,
        expected_output=req.expected_output,
        approval_required=req.approval_required,
        runbook=[
            "load project context and Project Spec IR",
            "evaluate policy and required permissions",
            f"execute task: {req.task}",
            f"validate output: {req.expected_output}",
            "record scorecard and event trail",
        ],
    )
