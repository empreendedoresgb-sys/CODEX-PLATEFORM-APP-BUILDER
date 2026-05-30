from __future__ import annotations

from orchestrator.contracts import (
    AutomationRecipe,
    BrowserTaskPlan,
    CapabilityType,
    MCPConnectorDefinition,
    MediaGenerationPlan,
    MediaGenerationRequest,
    MobileCommandPlan,
    MobileCommandRequest,
    PluginChainDefinition,
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
