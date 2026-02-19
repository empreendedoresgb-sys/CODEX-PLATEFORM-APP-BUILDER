# APBUILDER.APP — Product Boundary and Scope

## Identity
**APBUILDER.APP** is the app/web builder product in this repository.
It is separate from **KriolGB IA Voice**.

## Current code scope
- `ai_assistant/platform_orchestrator.py`
- `core/platform_modes.py`
- API route: `POST /v1/platform/build-plan`

## Separation rule
- Voice-related naming, schemas, and docs remain under KriolGB IA Voice identity.
- Builder-related orchestration remains under APBUILDER.APP identity.
- Shared runtime/API container may host both domains, but product naming must stay explicit per endpoint/module.

## Next extraction path (recommended)
1. Move APBUILDER.APP modules into top-level `apbuilder/` package.
2. Split API routers into:
   - `api/routers/kriol_voice.py`
   - `api/routers/apbuilder.py`
3. Assign separate OpenAPI tags and grouped docs.
4. Optional: expose separate subdomains and deployment manifests.
