CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    tier TEXT NOT NULL CHECK (tier IN ('free', 'pro', 'enterprise')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS voice_profiles (
    profile_id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(user_id),
    voice_id TEXT NOT NULL,
    language TEXT NOT NULL,
    phonetic_mode TEXT NOT NULL DEFAULT 'african',
    cadence_type TEXT NOT NULL,
    emotional_mode TEXT,
    character_mode TEXT,
    pitch NUMERIC(4,2) NOT NULL DEFAULT 1.0,
    tempo NUMERIC(4,2) NOT NULL DEFAULT 1.0,
    energy NUMERIC(4,2) NOT NULL DEFAULT 1.0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS voice_presets (
    preset_id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(user_id),
    profile_id UUID NOT NULL REFERENCES voice_profiles(profile_id),
    preset_name TEXT NOT NULL,
    serialized_config JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS generation_jobs (
    job_id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(user_id),
    input_text TEXT NOT NULL,
    output_uri TEXT,
    status TEXT NOT NULL CHECK (status IN ('queued', 'processing', 'done', 'failed')),
    compliance_score NUMERIC(5,4) NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_generation_jobs_user_created
ON generation_jobs(user_id, created_at DESC);
