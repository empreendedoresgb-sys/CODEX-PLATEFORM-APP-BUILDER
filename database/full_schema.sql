-- KriolGB IA Voice Full Production Schema
-- PostgreSQL 15+

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =========
-- Identity
-- =========
CREATE TABLE IF NOT EXISTS organizations (
    org_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    plan TEXT NOT NULL CHECK (plan IN ('free', 'pro', 'enterprise')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID REFERENCES organizations(org_id) ON DELETE SET NULL,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    role TEXT NOT NULL DEFAULT 'member',
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'suspended', 'invited')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- =========
-- Projects & Assets
-- =========
CREATE TABLE IF NOT EXISTS projects (
    project_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID NOT NULL REFERENCES organizations(org_id) ON DELETE CASCADE,
    owner_user_id UUID NOT NULL REFERENCES users(user_id),
    name TEXT NOT NULL,
    description TEXT,
    visibility TEXT NOT NULL DEFAULT 'private' CHECK (visibility IN ('private', 'team', 'public')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS media_assets (
    asset_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(project_id) ON DELETE CASCADE,
    uploaded_by UUID REFERENCES users(user_id),
    storage_uri TEXT NOT NULL,
    media_type TEXT NOT NULL CHECK (media_type IN ('audio', 'video', 'image', 'document')),
    format TEXT NOT NULL,
    size_bytes BIGINT NOT NULL,
    checksum_sha256 TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS imports (
    import_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id UUID NOT NULL REFERENCES media_assets(asset_id) ON DELETE CASCADE,
    source_format TEXT NOT NULL,
    parser_status TEXT NOT NULL CHECK (parser_status IN ('queued', 'processing', 'done', 'failed')),
    parser_report JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS exports (
    export_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    generated_by UUID REFERENCES users(user_id),
    output_format TEXT NOT NULL,
    output_uri TEXT,
    status TEXT NOT NULL CHECK (status IN ('queued', 'processing', 'done', 'failed')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- =========
-- Voice Domain
-- =========
CREATE TABLE IF NOT EXISTS voice_profiles (
    profile_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID NOT NULL REFERENCES organizations(org_id) ON DELETE CASCADE,
    owner_user_id UUID NOT NULL REFERENCES users(user_id),
    profile_name TEXT NOT NULL,
    voice_id TEXT NOT NULL,
    language TEXT NOT NULL,
    phonetic_mode TEXT NOT NULL DEFAULT 'african',
    cadence_type TEXT,
    emotional_mode TEXT,
    character_mode TEXT,
    tonal_variant TEXT,
    pitch NUMERIC(4,2) NOT NULL DEFAULT 1.0,
    tempo NUMERIC(4,2) NOT NULL DEFAULT 1.0,
    energy NUMERIC(4,2) NOT NULL DEFAULT 1.0,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS voice_clones (
    clone_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID NOT NULL REFERENCES voice_profiles(profile_id) ON DELETE CASCADE,
    training_asset_id UUID REFERENCES media_assets(asset_id),
    model_version TEXT NOT NULL,
    training_status TEXT NOT NULL CHECK (training_status IN ('queued', 'training', 'ready', 'failed')),
    quality_score NUMERIC(5,4),
    consent_token TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS voice_presets (
    preset_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID NOT NULL REFERENCES voice_profiles(profile_id) ON DELETE CASCADE,
    preset_name TEXT NOT NULL,
    serialized_config JSONB NOT NULL,
    is_locked BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (profile_id, preset_name)
);

CREATE TABLE IF NOT EXISTS generation_jobs (
    job_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(project_id) ON DELETE SET NULL,
    requested_by UUID REFERENCES users(user_id),
    input_text TEXT,
    source_asset_id UUID REFERENCES media_assets(asset_id),
    output_asset_id UUID REFERENCES media_assets(asset_id),
    mode TEXT NOT NULL CHECK (mode IN ('text', 'voice', 'multilingual', 'transcription')),
    status TEXT NOT NULL CHECK (status IN ('queued', 'processing', 'done', 'failed')),
    compliance_score NUMERIC(5,4) NOT NULL DEFAULT 0,
    latency_ms INTEGER,
    error_message TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- =========
-- Transcription & Analysis
-- =========
CREATE TABLE IF NOT EXISTS transcripts (
    transcript_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID NOT NULL REFERENCES generation_jobs(job_id) ON DELETE CASCADE,
    language_detected TEXT,
    confidence NUMERIC(5,4),
    transcript_text TEXT NOT NULL,
    srt_uri TEXT,
    json_uri TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS linguistic_analyses (
    analysis_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transcript_id UUID NOT NULL REFERENCES transcripts(transcript_id) ON DELETE CASCADE,
    ntopy4_compliance BOOLEAN NOT NULL DEFAULT FALSE,
    operators_detected JSONB NOT NULL DEFAULT '[]'::jsonb,
    oral_markers JSONB NOT NULL DEFAULT '[]'::jsonb,
    cultural_keywords JSONB NOT NULL DEFAULT '[]'::jsonb,
    semantic_intent TEXT,
    canonical_source TEXT NOT NULL DEFAULT 'TIRA BOKA NA BINHU',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- =========
-- QR, Billing, Audit
-- =========
CREATE TABLE IF NOT EXISTS qr_links (
    qr_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(project_id) ON DELETE CASCADE,
    target_type TEXT NOT NULL CHECK (target_type IN ('voice', 'transcript', 'invoice', 'template', 'demo')),
    target_id UUID,
    token TEXT UNIQUE NOT NULL,
    expires_at TIMESTAMPTZ,
    click_count BIGINT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS subscriptions (
    subscription_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID NOT NULL REFERENCES organizations(org_id) ON DELETE CASCADE,
    tier TEXT NOT NULL CHECK (tier IN ('free', 'pro', 'enterprise')),
    status TEXT NOT NULL CHECK (status IN ('active', 'paused', 'canceled')),
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ended_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS invoices (
    invoice_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID NOT NULL REFERENCES organizations(org_id) ON DELETE CASCADE,
    subscription_id UUID REFERENCES subscriptions(subscription_id) ON DELETE SET NULL,
    amount_cents BIGINT NOT NULL,
    currency TEXT NOT NULL DEFAULT 'USD',
    status TEXT NOT NULL CHECK (status IN ('draft', 'issued', 'paid', 'void')),
    pdf_uri TEXT,
    issued_at TIMESTAMPTZ,
    due_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS payments (
    payment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_id UUID NOT NULL REFERENCES invoices(invoice_id) ON DELETE CASCADE,
    provider TEXT NOT NULL,
    provider_ref TEXT UNIQUE NOT NULL,
    amount_cents BIGINT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('pending', 'succeeded', 'failed')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    actor_user_id UUID REFERENCES users(user_id),
    event_type TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id UUID,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- =========
-- Indexes
-- =========
CREATE INDEX IF NOT EXISTS idx_projects_org ON projects(org_id);
CREATE INDEX IF NOT EXISTS idx_assets_project ON media_assets(project_id);
CREATE INDEX IF NOT EXISTS idx_jobs_status_created ON generation_jobs(status, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_transcripts_job ON transcripts(job_id);
CREATE INDEX IF NOT EXISTS idx_analysis_transcript ON linguistic_analyses(transcript_id);
CREATE INDEX IF NOT EXISTS idx_qr_token ON qr_links(token);
CREATE INDEX IF NOT EXISTS idx_invoices_org_status ON invoices(org_id, status);
CREATE INDEX IF NOT EXISTS idx_audit_events_entity ON audit_events(entity_type, entity_id);
