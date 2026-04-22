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

## Preview smoke test

Start API:

```bash
uvicorn api.rest_endpoints:app --host 0.0.0.0 --port 8000
```

In another terminal, run:

```bash
./scripts/preview_smoke_test.sh
```

## Frontend preview button component

Use `PreviewWorkbench` to add a top-menu "Launch Live App Preview" button with live iframe preview, interactive mode toggle, and desktop/tablet/mobile simulator.

```tsx
import { PreviewWorkbench } from './frontend/components/PreviewWorkbench';

export default function App() {
  return <PreviewWorkbench previewUrl="http://127.0.0.1:8000/docs" />;
}
```

## Codex workspace preview button (browser userscript)

If you want a preview button in your workspace UI itself (outside repo app code), install this userscript in a browser extension like Tampermonkey:

- `scripts/codex_workspace_preview_button.user.js`

What it does:
- tries to insert **Launch App Preview** into top header/toolbar areas
- falls back to a floating top-right button if toolbar selectors are not found
- stores your preview URL in localStorage and opens it in a new tab

Default preview URL: `http://127.0.0.1:8000/docs`

