from fastapi import FastAPI
from pydantic import BaseModel

from core.engine_controller import process
from core.languages.registry import list_languages
from multilingual.translation_router import route_translation
from orchestrator import get_orchestrator_run, run_orchestrator
from orchestrator.contracts import BuildType, KpiFocus, LiveMetricsSnapshot, OrchestratorRunRequest, ProjectSpecIR, TaskEnvelope
from orchestrator.control_plane import evaluate_policy, route_control_plane, route_control_plane_by_live_metrics
from orchestrator.master import deploy_run
from orchestrator.spec_ir import build_spec_ir

app = FastAPI(title="APBUILDER.APP API", version="v1")


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


@app.post("/v1/orchestrator/runs/{run_id}/deploy")
def orchestrator_deploy_run(run_id: str) -> dict:
    try:
        run = deploy_run(run_id)
        return {"status": "ok", "run": run.model_dump()}
    except ValueError as exc:
        return {"status": "failed", "error": str(exc)}
