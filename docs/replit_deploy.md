# Replit Visual Test & Deploy Guide

## Run locally in Replit
- Start command: `uvicorn api.rest_endpoints:app --host 0.0.0.0 --port 3000`
- Visual demo page: `/demo`
- API docs: `/docs`
- Health: `/v1/system/health`

## Deployment settings
Use deployment run command:
`uvicorn api.rest_endpoints:app --host 0.0.0.0 --port ${PORT}`

## Recommended Replit secrets
- `PAYMENT_WEBHOOK_SECRET`

## Smoke test checklist
1. `GET /v1/system/health` returns `status=ok`
2. `POST /v1/generate/text` with canonical input returns `status=ok`
3. `GET /demo` renders HTML page
4. `/docs` loads all routes
