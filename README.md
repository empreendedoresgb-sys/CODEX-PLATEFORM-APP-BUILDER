# APBUILDER.APP

APBUILDER.APP is a unified AI-first app and web builder platform.

## Core architecture highlights
- Multi-layer validation and anti-drift pipeline
- Language abstraction layer for infrastructure-level language systems
- Kriol Guinea integrated as a first-class language module (`kriol-guinea`)
- Voice and multilingual generation surfaces

## Run API

```bash
uvicorn api.rest_endpoints:app --reload
```

## Run tests

```bash
pytest
```

## Key API endpoints

- `GET /v1/languages`
- `POST /v1/generate/text`
- `POST /v1/generate/voice`
- `POST /v1/generate/multilingual`
- `POST /v1/validate`
- `GET /v1/voice/templates`
- `POST /v1/voice/presets`
- `GET /v1/voice/presets`
- `GET /v1/monetization/tiers/{tier_name}`
