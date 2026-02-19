# KriolGB IA Voice + APBUILDER.APP (Monorepo)

This repository now hosts **two distinct products** with separate identities:

1. **KriolGB IA Voice** (voice specialization)
2. **APBUILDER.APP** (AI app/web builder specialization)

## Product boundaries

### 1) KriolGB IA Voice
Voice-focused modules and APIs:
- Linguistic enforcement, voice synthesis, presets, phonetic validation
- Endpoints under `/v1/generate/*`, `/v1/voice/*`, `/v1/validate`

### 2) APBUILDER.APP
Builder-focused orchestration modules and APIs:
- Platform mode engine (`developer`, `nocode`, `hybrid`)
- Multi-agent build plan generation
- Endpoint under `/v1/platform/build-plan`

## Run API

```bash
uvicorn api.rest_endpoints:app --reload
```

## Run tests

```bash
pytest
```

## Key API endpoints

- `POST /v1/generate/text`
- `POST /v1/generate/voice`
- `POST /v1/generate/multilingual`
- `POST /v1/validate`
- `GET /v1/voice/templates`
- `POST /v1/voice/presets`
- `GET /v1/voice/presets`
- `GET /v1/monetization/tiers/{tier_name}`
- `POST /v1/platform/build-plan`
