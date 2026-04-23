# APBUILDER Gold Blueprint (Concrete Implementation)

## 1) Directory-by-directory implementation map

```text
api/
  rest_endpoints.py                    # public API contracts
orchestrator/
  contracts.py                         # ProjectSpecIR + TaskEnvelope + Scorecard + metrics models
  spec_ir.py                           # IR builder (single source of truth for build targets)
  control_plane.py                     # static + live-metrics routing and policy evaluation
  evaluator.py                         # quality/security/KPI scoring + pass gates
  master.py                            # end-to-end execution with policy, evaluation, and deploy staging
  repository.py                        # run persistence and events
database/
  schema.sql                           # builder tables + spec_ir + scorecards + live metrics
.github/workflows/
  ci.yml                               # test + schema checks
```

## 2) API contracts

### Build and validate Project Spec IR

- `POST /v1/spec-ir/build`

Request:
```json
{
  "prompt": "Build enterprise billing platform",
  "build_type": "SOFTWARE",
  "target_runtime": "web"
}
```

Response:
```json
{
  "status": "ok",
  "spec": {
    "project_name": "Build enterprise billing platform",
    "build_type": "SOFTWARE",
    "target_runtime": "web",
    "frontend_stack": "react",
    "backend_stack": "python-fastapi",
    "infra_profile": "cloud",
    "quality_gates": ["tests", "security", "kpi"]
  }
}
```

- `POST /v1/spec-ir/validate`

Request body: `ProjectSpecIR`

### KPI-driven control-plane routing

- `POST /v1/control-plane/route`
- `POST /v1/control-plane/route/live`

Live route request:
```json
{
  "kpi_focus": "PR_THROUGHPUT_MTTR",
  "metrics": {
    "pr_throughput": 3.0,
    "bug_mttr_hours": 30.0,
    "autonomous_ops_success_rate": 0.76
  }
}
```

### Policy and run lifecycle

- `POST /v1/policy/evaluate`
- `POST /v1/orchestrator/run`
- `GET /v1/orchestrator/runs/{run_id}`
- `POST /v1/orchestrator/runs/{run_id}/deploy`

## 3) Database table additions

- `project_spec_ir`
  - stores per-project canonical spec IR for build generation.
- `run_scorecards`
  - stores run evaluator outputs (quality/security/KPI + pass/fail gate).
- `live_kpi_metrics`
  - stores runtime metrics used for control-plane routing.

## 4) CI pipeline YAML (minimum reliable baseline)

- Install Python dependencies.
- Run `pytest -q`.
- Validate schema presence for key tables (`builder_projects`, `project_spec_ir`, `run_scorecards`).

## 5) Integration sequence (practical)

1. Generate `ProjectSpecIR` from prompt + build type.
2. Route by KPI + live metrics to BUILD or OPS plane.
3. Evaluate policy constraints (sandbox/signature/scope).
4. Execute orchestrator stages.
5. Evaluate run scorecard and enforce pass gate.
6. Move to `DEPLOY_READY`, then explicit deploy.

## 6) Expansion targets

- Add OpenTelemetry traces around each stage and policy decision.
- Persist all run events + scorecards in PostgreSQL.
- Add signed skills registry and policy-as-code manifests.
