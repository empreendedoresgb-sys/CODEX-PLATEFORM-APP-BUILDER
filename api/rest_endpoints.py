from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from api.websocket_handler import router as ws_router
from core.engine_controller import process
from core.languages.registry import list_languages
from multilingual.translation_router import route_translation
from orchestrator import get_orchestrator_run, run_orchestrator
from orchestrator.capabilities import (
    build_agent_blueprint,
    build_design_system,
    build_interaction_suite,
    build_job_template,
    build_plugin_chain,
    build_workspace_document,
    create_automation,
    plan_browser_task,
    plan_media_generation,
    queue_mobile_command,
    register_mcp_connector,
    register_skill,
)
from orchestrator.contracts import (
    AgentBlueprintRequest,
    AutomationRecipe,
    BrowserTaskPlan,
    BuildType,
    DesignSystemRequest,
    InteractionSuiteRequest,
    JobTemplateRequest,
    KpiFocus,
    LiveMetricsSnapshot,
    MCPConnectorDefinition,
    MediaGenerationRequest,
    MobileCommandRequest,
    OrchestratorRunRequest,
    PluginChainDefinition,
    ProjectSpecIR,
    SkillDefinition,
    TaskEnvelope,
    WorkspaceDocumentRequest,
)
from orchestrator.control_plane import evaluate_policy, route_control_plane, route_control_plane_by_live_metrics
from orchestrator.master import deploy_run
from orchestrator.repository import get_events
from orchestrator.spec_ir import build_spec_ir

app = FastAPI(title="APBUILDER.APP API", version="v1")
app.include_router(ws_router)


LANDING_PAGE_HTML = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>APBUILDER.APP — AI App Builder</title>
    <style>
      :root {
        color-scheme: dark;
        --bg: #020617;
        --panel: rgba(15, 23, 42, 0.72);
        --line: rgba(148, 163, 184, 0.22);
        --text: #e2e8f0;
        --muted: #94a3b8;
        --blue: #38bdf8;
        --violet: #8b5cf6;
        --green: #2dd4bf;
        --pink: #f472b6;
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        min-height: 100vh;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        color: var(--text);
        background:
          radial-gradient(circle at 20% 20%, rgba(56, 189, 248, 0.28), transparent 26rem),
          radial-gradient(circle at 80% 10%, rgba(139, 92, 246, 0.26), transparent 24rem),
          radial-gradient(circle at 55% 80%, rgba(45, 212, 191, 0.22), transparent 28rem),
          var(--bg);
        overflow-x: hidden;
      }
      .grid-glow {
        position: fixed;
        inset: 0;
        pointer-events: none;
        background-image:
          linear-gradient(rgba(148, 163, 184, 0.08) 1px, transparent 1px),
          linear-gradient(90deg, rgba(148, 163, 184, 0.08) 1px, transparent 1px);
        background-size: 48px 48px;
        mask-image: linear-gradient(to bottom, black, transparent 85%);
      }
      header, main { position: relative; z-index: 1; }
      header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        padding: 24px clamp(20px, 5vw, 72px);
      }
      .brand {
        display: inline-flex;
        align-items: center;
        gap: 12px;
        font-weight: 800;
        letter-spacing: 0.08em;
      }
      .brand-mark {
        width: 38px;
        height: 38px;
        border-radius: 14px;
        background: linear-gradient(135deg, var(--blue), var(--violet), var(--green));
        box-shadow: 0 0 34px rgba(56, 189, 248, 0.55);
      }
      nav { display: flex; gap: 14px; flex-wrap: wrap; }
      nav a {
        color: var(--muted);
        text-decoration: none;
        font-size: 0.92rem;
      }
      nav a:hover { color: white; }
      .hero {
        max-width: 1180px;
        margin: 0 auto;
        padding: 64px clamp(20px, 5vw, 40px) 84px;
        display: grid;
        grid-template-columns: minmax(0, 1.08fr) minmax(320px, 0.92fr);
        gap: 40px;
        align-items: center;
      }
      .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 9px 13px;
        border: 1px solid var(--line);
        border-radius: 999px;
        color: #bae6fd;
        background: rgba(14, 165, 233, 0.1);
        box-shadow: inset 0 0 28px rgba(56, 189, 248, 0.08);
      }
      .pulse-dot {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: var(--green);
        box-shadow: 0 0 0 rgba(45, 212, 191, 0.6);
        animation: pulse 1.7s infinite;
      }
      h1 {
        margin: 22px 0 18px;
        font-size: clamp(3rem, 8vw, 6.7rem);
        line-height: 0.9;
        letter-spacing: -0.08em;
      }
      .gradient-text {
        background: linear-gradient(100deg, white, #bfdbfe 28%, #c4b5fd 58%, #5eead4);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
      }
      .lede {
        color: var(--muted);
        font-size: clamp(1rem, 2vw, 1.2rem);
        line-height: 1.75;
        max-width: 760px;
      }
      .actions { display: flex; flex-wrap: wrap; gap: 16px; margin-top: 32px; }
      .primary-button, .secondary-button {
        position: relative;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        min-height: 54px;
        padding: 0 22px;
        border-radius: 999px;
        color: white;
        text-decoration: none;
        font-weight: 800;
        overflow: hidden;
        transform: translateZ(0);
      }
      .primary-button {
        border: 0;
        background: linear-gradient(90deg, var(--blue), var(--violet), var(--pink), var(--green));
        background-size: 280% 100%;
        box-shadow: 0 18px 48px rgba(56, 189, 248, 0.25), 0 0 0 1px rgba(255,255,255,0.1) inset;
        animation: shimmer 4.5s linear infinite, float 3.8s ease-in-out infinite;
      }
      .primary-button::after {
        content: "";
        position: absolute;
        inset: -40% -20%;
        background: linear-gradient(110deg, transparent 35%, rgba(255,255,255,0.55), transparent 65%);
        transform: translateX(-120%);
        animation: sweep 2.8s ease-in-out infinite;
      }
      .primary-button span { position: relative; z-index: 1; }
      .secondary-button {
        border: 1px solid var(--line);
        background: rgba(15, 23, 42, 0.58);
      }
      .panel {
        border: 1px solid var(--line);
        border-radius: 28px;
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.82), rgba(15, 23, 42, 0.54));
        box-shadow: 0 24px 80px rgba(0, 0, 0, 0.35);
        padding: 22px;
        backdrop-filter: blur(18px);
      }
      .terminal {
        border-radius: 20px;
        overflow: hidden;
        background: rgba(2, 6, 23, 0.9);
        border: 1px solid rgba(148, 163, 184, 0.18);
      }
      .terminal-head {
        display: flex;
        gap: 7px;
        padding: 14px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.14);
      }
      .terminal-head i { width: 11px; height: 11px; border-radius: 50%; background: var(--pink); }
      .terminal-head i:nth-child(2) { background: #facc15; }
      .terminal-head i:nth-child(3) { background: var(--green); }
      .terminal-body { padding: 18px; color: #bfdbfe; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.9rem; line-height: 1.75; }
      .terminal-body strong { color: #5eead4; }
      .cards {
        max-width: 1180px;
        margin: 0 auto 72px;
        padding: 0 clamp(20px, 5vw, 40px);
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 16px;
      }
      .card {
        border: 1px solid var(--line);
        border-radius: 22px;
        padding: 20px;
        background: rgba(15, 23, 42, 0.58);
      }
      .card h3 { margin: 0 0 10px; }
      .card p { margin: 0; color: var(--muted); line-height: 1.6; }
      @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(45, 212, 191, 0.55); } 70% { box-shadow: 0 0 0 12px rgba(45, 212, 191, 0); } 100% { box-shadow: 0 0 0 0 rgba(45, 212, 191, 0); } }
      @keyframes shimmer { 0% { background-position: 0% 50%; } 100% { background-position: 280% 50%; } }
      @keyframes sweep { 0%, 30% { transform: translateX(-120%); } 70%, 100% { transform: translateX(120%); } }
      @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-5px); } }
      @media (max-width: 860px) {
        header { align-items: flex-start; flex-direction: column; }
        .hero { grid-template-columns: 1fr; padding-top: 34px; }
        .cards { grid-template-columns: 1fr; }
      }
    </style>
  </head>
  <body>
    <div class="grid-glow"></div>
    <header>
      <div class="brand"><span class="brand-mark"></span><span>APBUILDER.APP</span></div>
      <nav aria-label="Primary navigation">
        <a href="/docs">API Docs</a>
        <a href="/v1/preview/button">Preview</a>
        <a href="/v1/health">Health</a>
      </nav>
    </header>
    <main>
      <section class="hero">
        <div>
          <div class="eyebrow"><span class="pulse-dot"></span>AI-first app, web, agent & bot builder</div>
          <h1><span class="gradient-text">Build software at orchestration speed.</span></h1>
          <p class="lede">
            APBUILDER combines project spec IR, multi-agent orchestration, policy gates,
            design-system blueprints, capability plugins, live preview tooling, and deployment
            scorecards into one app-building control plane.
          </p>
          <div class="actions">
            <a class="primary-button" href="/docs"><span>Launch Live Preview ✨</span></a>
            <a class="secondary-button" href="/v1/preview/button">Open Preview Button</a>
            <a class="secondary-button" href="/docs">Explore Capabilities</a>
          </div>
        </div>
        <aside class="panel" aria-label="Build pipeline preview">
          <div class="terminal">
            <div class="terminal-head"><i></i><i></i><i></i></div>
            <div class="terminal-body">
              <div><strong>intent</strong> → app / website / bot / agent</div>
              <div><strong>plan</strong> → Project Spec IR + design system</div>
              <div><strong>generate</strong> → frontend + backend + automation</div>
              <div><strong>validate</strong> → tests + security + KPI scorecard</div>
              <div><strong>ship</strong> → deploy-ready with rollback control</div>
            </div>
          </div>
        </aside>
      </section>
      <section class="cards" aria-label="Platform pillars">
        <article class="card"><h3>Design</h3><p>Animated landing pages, mockups, tokens, responsive layouts, and accessibility checks.</p></article>
        <article class="card"><h3>Agents</h3><p>Intent, architect, generator, validator, release, research, UX, security, and growth roles.</p></article>
        <article class="card"><h3>Automation</h3><p>Scheduled tasks, skills, plugins, connectors, browser actions, and mobile-to-workspace commands.</p></article>
        <article class="card"><h3>Governance</h3><p>Policy plane, sandbox tiers, audit trails, scorecards, approvals, and rollback plans.</p></article>
      </section>
    </main>
  </body>
</html>
"""


class TextRequest(BaseModel):
    input: str
    language_id: str = "en"


class MultilingualRequest(BaseModel):
    text: str
    source_language_id: str = "en"
    target_language_id: str = "fr"


class ValidateRequest(BaseModel):
    text: str
    language_id: str = "en"


class ControlPlaneRouteRequest(BaseModel):
    kpi_focus: KpiFocus


class ControlPlaneLiveRouteRequest(BaseModel):
    kpi_focus: KpiFocus
    metrics: LiveMetricsSnapshot


class ProjectSpecBuildRequest(BaseModel):
    prompt: str
    build_type: BuildType
    target_runtime: str = "web"




@app.get("/", response_class=HTMLResponse)
def landing_page() -> str:
    return LANDING_PAGE_HTML


@app.get("/v1/landing", response_class=HTMLResponse)
def landing_page_v1() -> str:
    return LANDING_PAGE_HTML


@app.get("/v1/health")
def health() -> dict:
    return {"status": "ok", "service": "apbuilder.api", "version": "v1"}



@app.get("/v1/preview/button", response_class=HTMLResponse)
def preview_button() -> str:
    return """
    <html>
      <head><title>APBUILDER Preview</title></head>
      <body style="font-family:Arial;padding:24px">
        <h2>APBUILDER.APP Preview Button</h2>
        <a href="/docs" style="background:#2563eb;color:#fff;padding:10px 14px;border-radius:8px;text-decoration:none">
          Launch App Preview
        </a>
      </body>
    </html>
    """

@app.get("/v1/languages")
def languages() -> dict:
    return {"status": "ok", "languages": list_languages()}


@app.post("/v1/generate/text")
def generate_text(req: TextRequest) -> dict:
    return process(req.model_dump(), language_id=req.language_id)


@app.post("/v1/generate/multilingual")
def generate_multilingual(req: MultilingualRequest) -> dict:
    translated = route_translation(req.text, req.source_language_id, req.target_language_id)
    return {"status": "ok", "data": {"text": translated}}


@app.post("/v1/validate")
def validate(req: ValidateRequest) -> dict:
    try:
        process({"input": req.text}, language_id=req.language_id)
        return {"status": "ok", "compliance": 1.0, "errors": []}
    except ValueError as exc:
        return {
            "status": "failed",
            "compliance": 0.0,
            "errors": [str(exc)],
            "suggested_correction": "Adjust output to selected language rules.",
        }


@app.post("/v1/spec-ir/build")
def spec_ir_build(req: ProjectSpecBuildRequest) -> dict:
    spec = build_spec_ir(prompt=req.prompt, build_type=req.build_type, target_runtime=req.target_runtime)
    return {"status": "ok", "spec": spec.model_dump()}


@app.post("/v1/spec-ir/validate")
def spec_ir_validate(req: ProjectSpecIR) -> dict:
    return {"status": "ok", "valid": True, "spec": req.model_dump()}


@app.post("/v1/control-plane/route")
def control_plane_route(req: ControlPlaneRouteRequest) -> dict:
    selected = route_control_plane(req.kpi_focus)
    return {"status": "ok", "selected_plane": selected}


@app.post("/v1/control-plane/route/live")
def control_plane_route_live(req: ControlPlaneLiveRouteRequest) -> dict:
    selected = route_control_plane_by_live_metrics(req.kpi_focus, req.metrics)
    return {"status": "ok", "selected_plane": selected, "metrics": req.metrics.model_dump()}


@app.post("/v1/policy/evaluate")
def policy_evaluate(req: TaskEnvelope) -> dict:
    decision = evaluate_policy(req)
    return {"status": "ok", "decision": decision.model_dump()}



@app.post("/v1/capabilities/workspace-document")
def capability_workspace_document(req: WorkspaceDocumentRequest) -> dict:
    result = build_workspace_document(req)
    return {"status": "ok", "artifact": result.model_dump()}


@app.post("/v1/capabilities/skills")
def capability_register_skill(req: SkillDefinition) -> dict:
    return register_skill(req)


@app.post("/v1/capabilities/mcp-connectors")
def capability_register_mcp(req: MCPConnectorDefinition) -> dict:
    return register_mcp_connector(req)


@app.post("/v1/capabilities/plugin-chains")
def capability_plugin_chain(req: PluginChainDefinition) -> dict:
    return build_plugin_chain(req)


@app.post("/v1/capabilities/media-plan")
def capability_media_plan(req: MediaGenerationRequest) -> dict:
    result = plan_media_generation(req)
    return {"status": "ok", "plan": result.model_dump()}


@app.post("/v1/capabilities/automations")
def capability_automation(req: AutomationRecipe) -> dict:
    return create_automation(req)


@app.post("/v1/capabilities/browser-task")
def capability_browser_task(req: BrowserTaskPlan) -> dict:
    return plan_browser_task(req)


@app.post("/v1/capabilities/mobile-command")
def capability_mobile_command(req: MobileCommandRequest) -> dict:
    result = queue_mobile_command(req)
    return {"status": "ok", "mobile_command": result.model_dump()}


@app.post("/v1/capabilities/design-system")
def capability_design_system(req: DesignSystemRequest) -> dict:
    result = build_design_system(req)
    return {"status": "ok", "design_system": result.model_dump()}


@app.post("/v1/capabilities/agent-blueprint")
def capability_agent_blueprint(req: AgentBlueprintRequest) -> dict:
    result = build_agent_blueprint(req)
    return {"status": "ok", "agent_blueprint": result.model_dump()}


@app.post("/v1/capabilities/job-template")
def capability_job_template(req: JobTemplateRequest) -> dict:
    result = build_job_template(req)
    return {"status": "ok", "job_template": result.model_dump()}


@app.post("/v1/capabilities/interaction-suite")
def capability_interaction_suite(req: InteractionSuiteRequest) -> dict:
    result = build_interaction_suite(req)
    return {"status": "ok", "interaction_suite": result.model_dump()}


@app.post("/v1/orchestrator/run")
def orchestrator_run(req: OrchestratorRunRequest) -> dict:
    result = run_orchestrator(req)
    return {"status": "ok", "run": result.model_dump()}


@app.get("/v1/orchestrator/runs/{run_id}")
def orchestrator_get_run(run_id: str) -> dict:
    try:
        run = get_orchestrator_run(run_id)
        return {"status": "ok", "run": run.model_dump()}
    except ValueError as exc:
        return {"status": "failed", "error": str(exc)}


@app.get("/v1/orchestrator/runs/{run_id}/events")
def orchestrator_get_events(run_id: str) -> dict:
    try:
        events = get_events(run_id)
        return {"status": "ok", "events": [event.model_dump() for event in events]}
    except ValueError as exc:
        return {"status": "failed", "error": str(exc)}


@app.post("/v1/orchestrator/runs/{run_id}/deploy")
def orchestrator_deploy_run(run_id: str) -> dict:
    try:
        run = deploy_run(run_id)
        return {"status": "ok", "run": run.model_dump()}
    except ValueError as exc:
        return {"status": "failed", "error": str(exc)}
