from __future__ import annotations

from orchestrator.contracts import (
    AgentBlueprint,
    AgentBlueprintRequest,
    AutomationRecipe,
    BrowserTaskPlan,
    CapabilityType,
    DesignSystemBlueprint,
    DesignSystemRequest,
    FoundationBlueprint,
    FoundationSuiteBlueprint,
    FoundationSuiteRequest,
    CapabilityModule,
    JobTemplate,
    JobTemplateRequest,
    InteractionSuiteBlueprint,
    InteractionSuiteRequest,
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



def build_interaction_suite(req: InteractionSuiteRequest) -> InteractionSuiteBlueprint:
    base_guardrails = [
        "policy-plane approval before external side effects",
        "audit trail for every connector, browser, remote, and file action",
        "least-privilege connector scopes with revocation support",
    ]
    modules = [
        CapabilityModule(
            name="Ask / Chat",
            capability_type=CapabilityType.CHAT,
            status="available",
            api_surface="/v1/generate/text + /v1/orchestrator/run",
            guardrails=["conversation payload validation", "language runtime validation"],
            implementation_notes=["Use as the natural-language entry point for app, web, bot, and agent build requests."],
        ),
        CapabilityModule(
            name="Mic / Speech",
            capability_type=CapabilityType.SPEECH,
            status="planned-blueprint",
            api_surface="/v1/capabilities/interaction-suite",
            guardrails=["explicit microphone consent", "transcript redaction before storage"],
            implementation_notes=["Add STT/TTS adapters behind the capability registry; emit text into the orchestrator."],
        ),
        CapabilityModule(
            name="Render / Artifacts",
            capability_type=CapabilityType.ARTIFACT,
            status="available-blueprint",
            api_surface="/v1/capabilities/workspace-document + /v1/capabilities/media-plan",
            guardrails=["artifact metadata scan", "download links expire by policy"],
            implementation_notes=["Standardize generated docs, spreadsheets, slides, mockups, and previews as typed artifacts."],
        ),
        CapabilityModule(
            name="Think / Extended Reasoning",
            capability_type=CapabilityType.EXTENDED_THINKING,
            status="available-blueprint",
            api_surface="/v1/orchestrator/run",
            guardrails=["scorecard gates before deploy", "explain blocking issues"],
            implementation_notes=["Represent deeper reasoning as longer plan/validate loops, not unsafe hidden execution."],
        ),
        CapabilityModule(
            name="Model Routing",
            capability_type=CapabilityType.MODEL_ROUTING,
            status="planned-blueprint",
            api_surface="/v1/control-plane/route/live",
            guardrails=["route by KPI and risk", "downgrade to safer model for high-risk tools"],
            implementation_notes=["Route fast, deep, vision, speech, and code models by task envelope, live metrics, risk, and complexity."],
        ),
        CapabilityModule(
            name="Deep Model Tier",
            capability_type=CapabilityType.DEEP_MODEL,
            status="planned-blueprint",
            api_surface="/v1/control-plane/route/live",
            guardrails=["reserve deep models for high-value reasoning", "record cost and latency budgets"],
            implementation_notes=["Represent Opus-class/deep reasoning choices as a provider-neutral model tier selected by risk and complexity."],
        ),
        CapabilityModule(
            name="Speed / Fast Path",
            capability_type=CapabilityType.SPEED_OPTIMIZATION,
            status="available-blueprint",
            api_surface="/v1/control-plane/route/live",
            guardrails=["never bypass security gates for speed", "fallback to deep validation on low confidence"],
            implementation_notes=["Route simple tasks to fast paths, cache reusable artifacts, and parallelize independent agent work."],
        ),
        CapabilityModule(
            name="Connectors",
            capability_type=CapabilityType.MCP_CONNECTOR,
            status="available",
            api_surface="/v1/capabilities/mcp-connectors",
            guardrails=base_guardrails,
            implementation_notes=["Register Gmail, Drive, Calendar, GitHub, Notion, Slack, CRM, data, research, and enterprise connectors declaratively."],
        ),
        CapabilityModule(
            name="Scheduled Tasks / Automate",
            capability_type=CapabilityType.AUTOMATION,
            status="available",
            api_surface="/v1/capabilities/automations + /v1/capabilities/job-template",
            guardrails=["human approval default", "rollback plan required", "event trail required"],
            implementation_notes=["Convert recurring tasks into policy-checked jobs with runbooks, scorecards, and notifications."],
        ),
        CapabilityModule(
            name="Persist / Projects",
            capability_type=CapabilityType.PROJECT_MEMORY,
            status="available-blueprint",
            api_surface="/v1/spec-ir/build + database project_spec_ir",
            guardrails=["project-scoped memory", "no cross-tenant context leakage"],
            implementation_notes=["Use Project Spec IR as the source of truth for product state, stack, quality gates, and capabilities."],
        ),
        CapabilityModule(
            name="Build / Cowork",
            capability_type=CapabilityType.COWORK,
            status="available",
            api_surface="/v1/orchestrator/run",
            guardrails=["agent artifacts reviewed by validator", "deployment only from DEPLOY_READY"],
            implementation_notes=["Coordinate intent, architecture, generation, validation, release, UX, security, and growth agents."],
        ),
        CapabilityModule(
            name="Stack / Plugins",
            capability_type=CapabilityType.PLUGIN_CHAIN,
            status="available",
            api_surface="/v1/capabilities/plugin-chains",
            guardrails=["signed plugin requirement", "scoped connector binding"],
            implementation_notes=["Compose skills/connectors into higher-order app-builder workflows."],
        ),
        CapabilityModule(
            name="Ship / Release",
            capability_type=CapabilityType.JOB_TEMPLATE,
            status="available",
            api_surface="/v1/orchestrator/runs/{run_id}/deploy",
            guardrails=["scorecard pass gate", "deploy approval flag", "rollback runbook"],
            implementation_notes=["Use quality, security, and KPI scorecards before release transitions."],
        ),
        CapabilityModule(
            name="Trigger / Skills",
            capability_type=CapabilityType.SKILL,
            status="available",
            api_surface="/v1/capabilities/skills",
            guardrails=["declarative skill instructions", "required connectors listed before execution"],
            implementation_notes=["Expose slash-command-style skills for design, research, coding, growth, ops, and support work."],
        ),
        CapabilityModule(
            name="Model in Excel",
            capability_type=CapabilityType.EXCEL_MODEL,
            status="available-blueprint",
            api_surface="/v1/capabilities/workspace-document",
            guardrails=["formula injection checks", "source file allowlist"],
            implementation_notes=["Use spreadsheet artifacts for analysis, charts, invoices, KPI reports, and finance models."],
        ),
        CapabilityModule(
            name="Investigate / Research",
            capability_type=CapabilityType.RESEARCH,
            status="available-blueprint",
            api_surface="/v1/capabilities/agent-blueprint + /v1/capabilities/mcp-connectors",
            guardrails=["source capture", "confidence labels", "no unsourced critical claims"],
            implementation_notes=["Bind research agents to approved web/search/MCP providers and feed findings into specs and scorecards."],
        ),
        CapabilityModule(
            name="Search / Web Search",
            capability_type=CapabilityType.WEB_SEARCH,
            status="planned-blueprint",
            api_surface="/v1/capabilities/interaction-suite",
            guardrails=["domain allow/deny lists", "citation metadata", "recency requirements"],
            implementation_notes=["Add provider adapters so app generation can use current market, API, and compliance data."],
        ),
        CapabilityModule(
            name="Slides / Presentations",
            capability_type=CapabilityType.SLIDES,
            status="available-blueprint",
            api_surface="/v1/capabilities/workspace-document + /v1/capabilities/design-system",
            guardrails=["brand token validation", "export metadata review"],
            implementation_notes=["Generate decks from research, KPI analysis, and product plans using design-system tokens."],
        ),
        CapabilityModule(
            name="Mockup / Design",
            capability_type=CapabilityType.MOCKUP,
            status="available",
            api_surface="/v1/capabilities/design-system + /v1/capabilities/media-plan",
            guardrails=["accessibility checks", "responsive preview required"],
            implementation_notes=["Create app/page mockups, component inventories, mobile/tablet layouts, and preview-ready UI plans."],
        ),
        CapabilityModule(
            name="Remote / Dispatch",
            capability_type=CapabilityType.REMOTE_DISPATCH,
            status="planned-blueprint" if req.include_remote_dispatch else "disabled-by-request",
            api_surface="/v1/capabilities/mobile-command + future worker queue",
            guardrails=["device registration", "remote kill switch", "workstation availability check"],
            implementation_notes=["Dispatch phone-originated or remote jobs to cloud/desktop workers when policy allows."],
        ),
        CapabilityModule(
            name="Click / Computer Use",
            capability_type=CapabilityType.COMPUTER_USE,
            status="available-blueprint",
            api_surface="/v1/capabilities/browser-task",
            guardrails=["validation-before-submit", "screen/action audit", "credential isolation"],
            implementation_notes=["Plan browser/computer-use flows for legacy apps without APIs; require confirmation for submissions by default."],
        ),
        CapabilityModule(
            name="Browse / Browser Extension",
            capability_type=CapabilityType.BROWSER_EXTENSION,
            status="available-blueprint",
            api_surface="scripts/codex_workspace_preview_button.user.js + /v1/preview/button",
            guardrails=["user-installed script only", "local preview URL storage", "no secret capture"],
            implementation_notes=["Use browser-side helpers for preview buttons, Chrome-style browse actions, and future extension integrations."],
        ),
    ]
    return InteractionSuiteBlueprint(
        product_goal=req.product_goal,
        autonomy_level=req.autonomy_level,
        modules=modules,
        rollout_phases=[
            "Phase 1: declarative blueprints and API contracts",
            "Phase 2: signed connector/plugin execution with policy gates",
            "Phase 3: live worker dispatch, browser actions, speech, and search adapters",
            "Phase 4: enterprise audit, tenant isolation, edge/on-prem execution, and revenue/KPI optimization",
        ],
        quality_gates=[
            "unit tests for every capability endpoint",
            "schema presence checks for persisted blueprint tables",
            "policy approval before side effects",
            "scorecard pass gate before deployment",
            "preview button smoke test after app modifications",
        ],
    )



def build_foundation_suite(req: FoundationSuiteRequest) -> FoundationSuiteBlueprint:
    foundations = [
        FoundationBlueprint(
            name="Authentication & Identity",
            capability_type=CapabilityType.AUTHENTICATION,
            priority="P0",
            api_surface="/v1/foundation/auth/blueprint",
            data_tables=["auth_identities", "team_memberships"],
            guardrails=["passwordless/OAuth-ready", "MFA-ready for enterprise", "tenant isolation required"],
            implementation_notes=["Support email magic link, OAuth providers, service tokens, and project-scoped sessions."],
        ),
        FoundationBlueprint(
            name="Payments, Billing & Plans",
            capability_type=CapabilityType.BILLING,
            priority="P0" if req.include_payments else "P2",
            api_surface="/v1/foundation/billing/blueprint",
            data_tables=["billing_accounts", "subscriptions", "payment_events"],
            guardrails=["never store raw card data", "webhook signature verification", "idempotent payment events"],
            implementation_notes=["Model free/pro/enterprise plans, usage credits, invoices, refunds, tax metadata, and upgrade prompts."],
        ),
        FoundationBlueprint(
            name="Onboarding & Activation",
            capability_type=CapabilityType.ONBOARDING,
            priority="P0",
            api_surface="/v1/foundation/onboarding/blueprint",
            data_tables=["app_foundation_blueprints"],
            guardrails=["progressive disclosure", "accessibility-first setup"],
            implementation_notes=["Guide users from idea to first generated app with templates, prompts, and preview milestones."],
        ),
        FoundationBlueprint(
            name="App Shell, Navigation & Modes",
            capability_type=CapabilityType.APP_SHELL,
            priority="P0",
            api_surface="/ + /v1/landing + future dashboard routes",
            data_tables=["project_spec_ir"],
            guardrails=["responsive layout", "dark/light mode token parity", "keyboard navigation"],
            implementation_notes=["Unify landing, dashboard, project workspace, preview, billing, and settings under one design system."],
        ),
        FoundationBlueprint(
            name="Template Marketplace",
            capability_type=CapabilityType.TEMPLATE_MARKETPLACE,
            priority="P1",
            api_surface="/v1/capabilities/design-system + /v1/spec-ir/build",
            data_tables=["capability_blueprints"],
            guardrails=["signed templates", "license metadata", "security scan before install"],
            implementation_notes=["Offer app, SaaS, marketplace, portfolio, internal tool, agent, bot, ecommerce, and mobile starter templates."],
        ),
        FoundationBlueprint(
            name="Analytics & Revenue Intelligence",
            capability_type=CapabilityType.ANALYTICS,
            priority="P1",
            api_surface="/v1/control-plane/route/live",
            data_tables=["live_kpi_metrics", "run_scorecards"],
            guardrails=["privacy-safe telemetry", "tenant-scoped analytics", "metric provenance"],
            implementation_notes=["Track activation, preview launches, deploys, conversion, build success, MTTR, and autonomous ops success."],
        ),
        FoundationBlueprint(
            name="Notifications & Collaboration",
            capability_type=CapabilityType.NOTIFICATIONS,
            priority="P1",
            api_surface="/v1/ws/events + future notification routes",
            data_tables=["team_memberships"],
            guardrails=["unsubscribe and preference controls", "no secret leakage in notifications"],
            implementation_notes=["Notify users and teams about run status, approvals, failed gates, payments, and deployments."],
        ),
        FoundationBlueprint(
            name="Team RBAC & Enterprise Controls",
            capability_type=CapabilityType.TEAM_RBAC,
            priority="P1" if req.include_enterprise else "P2",
            api_surface="/v1/policy/evaluate",
            data_tables=["team_memberships", "builder_projects"],
            guardrails=["least privilege roles", "audit all privilege changes", "enterprise SSO-ready"],
            implementation_notes=["Support owner/admin/builder/viewer roles, org projects, policy approvals, and scoped API tokens."],
        ),
    ]
    return FoundationSuiteBlueprint(
        product_goal=req.product_goal,
        launch_tier=req.launch_tier,
        foundations=foundations,
        launch_sequence=[
            "1. Ship landing + auth + project creation",
            "2. Add billing plans, payment webhooks, and usage credits",
            "3. Add templates, onboarding, preview-to-deploy conversion funnels",
            "4. Add team RBAC, analytics, notifications, and enterprise controls",
        ],
        readiness_checks=[
            "landing page has animated CTA and preview path",
            "auth blueprint includes tenant isolation and MFA-ready controls",
            "billing blueprint avoids raw card storage and requires signed webhooks",
            "analytics events are privacy-safe and tied to scorecards",
            "RBAC policies are enforced before destructive actions",
        ],
    )
