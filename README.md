# APBUILDER.APP

APBUILDER.APP is a unified AI-first app and web builder platform.

## Core architecture highlights
- Builder API and orchestration core
- Registry-driven language abstraction layer
- External language-core dependency support (`kriol-guinea-language-core`)
- Multi-layer validation and anti-drift pipeline

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
- `POST /v1/generate/multilingual`
- `POST /v1/validate`

- `POST /v1/orchestrator/run`
- `GET /v1/orchestrator/runs/{run_id}`
- `POST /v1/orchestrator/runs/{run_id}/deploy`
