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
