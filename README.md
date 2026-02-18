# KriolGB IA Voice

Production-ready scaffold implementing the **Book of Charge** architecture with:

- Ntopy-4-aligned module boundaries
- canonical lock hooks for `Tira Boka Na Binhu`
- anti-drift and validation pipeline
- voice-first API surfaces
- memory-efficient retrieval-oriented design stubs
- creative Voice Labs and preset functionality
- full production database schema and REST API blueprint artifacts

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
- `POST /v1/files/import`
- `POST /v1/files/export`
- `POST /v1/qr/create`
- `GET /v1/qr/{token}/stats`
- `POST /v1/transcription/analyze`
- `POST /v1/voice/clone/train`
- `GET /v1/billing/invoices`
- `POST /v1/billing/invoices`
- `POST /v1/billing/webhook/payment`
- `GET /v1/system/health`

## Architecture artifacts

- Full DB schema: `database/full_schema.sql`
- REST API blueprint (OpenAPI-style JSON): `api/contracts/rest_api_blueprint.json`
- Blueprint guide: `docs/rest_api_blueprint.md`

Compatibility alias (legacy typo): `POST /v1/generhate/text` -> handled as `POST /v1/generate/text`.
