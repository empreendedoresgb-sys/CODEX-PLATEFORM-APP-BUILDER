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

- `WS /v1/ws/events?run_id={run_id}`
- `GET /v1/orchestrator/runs/{run_id}/events`
- `GET /v1/health`
- `GET /v1/preview/button`
- `GET /v1/languages`
- `POST /v1/generate/text`
- `POST /v1/generate/multilingual`
- `POST /v1/validate`

- `POST /v1/orchestrator/run`
- `GET /v1/orchestrator/runs/{run_id}`
- `POST /v1/orchestrator/runs/{run_id}/deploy`
- `POST /v1/spec-ir/build`
- `POST /v1/spec-ir/validate`
- `POST /v1/control-plane/route/live`
- `POST /v1/capabilities/workspace-document`
- `POST /v1/capabilities/skills`
- `POST /v1/capabilities/mcp-connectors`
- `POST /v1/capabilities/plugin-chains`
- `POST /v1/capabilities/media-plan`
- `POST /v1/capabilities/automations`
- `POST /v1/capabilities/browser-task`
- `POST /v1/capabilities/mobile-command`
- `POST /v1/capabilities/design-system`
- `POST /v1/capabilities/agent-blueprint`
- `POST /v1/capabilities/job-template`

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

## Dual control-plane architecture (APBUILDER 2035)

APBUILDER now includes practical scaffolding for:

- **Build plane** (PR throughput / MTTR optimization)
- **Ops plane** (cross-system autonomous operations)
- **Policy plane** (sandbox tiering, signed plugins, least-privilege scopes, audit trail)

### New API endpoints

- `POST /v1/control-plane/route`
- `POST /v1/policy/evaluate`

### Inter-agent task envelope fields

- `intent`
- `risk_level`
- `required_permissions`
- `rollback_plan`
- `tool_class`
- `plugin_signature`
- `agent_id`

### Builder mission specializations

APBUILDER orchestration now supports build specialization types:

- `APP`
- `SOFTWARE`
- `MOBILE_APP`
- `WEB_PAGE`
- `WEBSITE`
- `AGENT`
- `BOT`

Use `build_type` in `POST /v1/orchestrator/run` to steer generated domain artifacts for your product mission.


## Gold implementation blueprint

- `docs/architecture/apbuilder_gold_blueprint.md`


## Preview button quick link

Open: `http://127.0.0.1:8000/v1/preview/button` to click **Launch App Preview** and jump to `/docs`.


## Codex-inspired capability layer

APBUILDER now includes API scaffolding for the functionality extracted from the Codex workflow video:

- workspace document generation for invoices, spreadsheets, reports, and web audits
- skill creation and invocation metadata
- MCP connector registration with scoped authorization notes
- plugin-chain orchestration that sequences skills and connectors
- image/video generation planning with brand references and quality checks
- scheduled automation recipes with human approval defaults
- browser task planning with validation-before-submit guardrails
- mobile command queue planning for phone-to-workspace requests
- Claude-style design system blueprints with tokens, components, accessibility gates, and implementation notes
- automatic agent blueprint generation for app, software, site, bot, and ops specialists
- reusable job templates that turn prompts into scheduled, auditable, policy-checked work


## Design systems, automatic agents, and job templates

APBUILDER extends the Codex-style capability layer with builder-native product automation:

- **Design system blueprints** convert a brand direction into reusable tokens, component inventories, accessibility checks, and implementation notes for React/Next, mobile, and website builds.
- **Agent blueprints** transform objectives and task lists into role definitions, connector/tool access, job templates, and guardrails for least-privilege autonomous work.
- **Job templates** package recurring app-building work into triggers, runbooks, expected outputs, approvals, scorecards, and event trails.

These capabilities are intentionally declarative first: they create safe blueprints that the policy plane can approve, sign, audit, and later bind to real connector credentials.
