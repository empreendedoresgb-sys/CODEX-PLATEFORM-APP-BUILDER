CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    plan TEXT NOT NULL CHECK (plan IN ('free', 'pro', 'enterprise')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS builder_projects (
    project_id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(user_id),
    name TEXT NOT NULL,
    target_runtime TEXT NOT NULL,
    language_id TEXT NOT NULL,
    config JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS build_jobs (
    job_id UUID PRIMARY KEY,
    project_id UUID NOT NULL REFERENCES builder_projects(project_id),
    input_prompt TEXT NOT NULL,
    output_uri TEXT,
    status TEXT NOT NULL CHECK (status IN ('queued', 'processing', 'done', 'failed')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS project_spec_ir (
    spec_id UUID PRIMARY KEY,
    project_id UUID NOT NULL REFERENCES builder_projects(project_id),
    build_type TEXT NOT NULL,
    target_runtime TEXT NOT NULL,
    frontend_stack TEXT NOT NULL,
    backend_stack TEXT NOT NULL,
    infra_profile TEXT NOT NULL,
    quality_gates JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS run_scorecards (
    scorecard_id UUID PRIMARY KEY,
    job_id UUID NOT NULL REFERENCES build_jobs(job_id),
    quality_score NUMERIC(4,3) NOT NULL,
    security_score NUMERIC(4,3) NOT NULL,
    kpi_score NUMERIC(4,3) NOT NULL,
    pass_gate BOOLEAN NOT NULL,
    reasons JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS live_kpi_metrics (
    metric_id UUID PRIMARY KEY,
    project_id UUID NOT NULL REFERENCES builder_projects(project_id),
    pr_throughput NUMERIC(10,2) NOT NULL DEFAULT 0,
    bug_mttr_hours NUMERIC(10,2) NOT NULL DEFAULT 0,
    autonomous_ops_success_rate NUMERIC(5,4) NOT NULL DEFAULT 0,
    captured_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS capability_blueprints (
    capability_id UUID PRIMARY KEY,
    project_id UUID REFERENCES builder_projects(project_id),
    capability_type TEXT NOT NULL,
    name TEXT NOT NULL,
    config JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS automation_recipes (
    automation_id UUID PRIMARY KEY,
    project_id UUID REFERENCES builder_projects(project_id),
    title TEXT NOT NULL,
    schedule TEXT NOT NULL,
    trigger_condition TEXT NOT NULL,
    steps JSONB NOT NULL,
    approval_required BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
