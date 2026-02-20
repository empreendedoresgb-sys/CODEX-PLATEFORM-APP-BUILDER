# KriolGB IA Voice

Production-ready scaffold implementing the **Book of Charge** architecture with:

- Ntopy-4-aligned module boundaries
- canonical lock hooks for `Tira Boka Na Binhu`
- anti-drift and validation pipeline
- voice-first API surfaces
- memory-efficient retrieval-oriented design stubs
- creative Voice Labs and preset functionality

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
