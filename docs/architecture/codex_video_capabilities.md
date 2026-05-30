# Codex Video Capability Extraction for APBUILDER

This document maps the transcript-proposed workflows into APBUILDER product capabilities.

## Extracted capability set

1. **Workspace document generation**
   - Analyze local folders and produce spreadsheets, reports, charts, web audit pages, and summaries.
   - API: `POST /v1/capabilities/workspace-document`.

2. **Skill creation**
   - Define reusable natural-language operations with required skills/connectors and strict instructions.
   - API: `POST /v1/capabilities/skills`.

3. **MCP connector registration**
   - Register external connectors such as Gmail, Drive, Calendar, Perplexity, Notion, or research providers.
   - API: `POST /v1/capabilities/mcp-connectors`.

4. **Plugin-chain orchestration**
   - Compose multiple skills/connectors into one higher-order workflow.
   - API: `POST /v1/capabilities/plugin-chains`.

5. **Image/video planning**
   - Generate plans for branded image/video creation based on references and social formats.
   - API: `POST /v1/capabilities/media-plan`.

6. **Scheduled automation recipes**
   - Define cron-like workflows that react to calendar or data conditions and produce drafts/artifacts.
   - API: `POST /v1/capabilities/automations`.

7. **Browser task automation planning**
   - Plan browser-based data entry/extraction flows for old software without APIs.
   - API: `POST /v1/capabilities/browser-task`.

8. **Mobile command queue**
   - Queue phone-originated app-building commands into the active workspace context.
   - API: `POST /v1/capabilities/mobile-command`.


9. **Design system blueprinting**
   - Convert brand/product direction into tokens, component inventories, accessibility checks, and implementation notes.
   - API: `POST /v1/capabilities/design-system`.

10. **Automatic agent blueprinting**
    - Convert objectives and task lists into specialist agents with tools, connectors, job templates, and guardrails.
    - API: `POST /v1/capabilities/agent-blueprint`.

11. **Reusable job templates**
    - Package recurring build/ops work into triggers, runbooks, expected outputs, approvals, scorecards, and event trails.
    - API: `POST /v1/capabilities/job-template`.

## Safety principles

- Browser and automation flows default to human approval.
- Connectors require least-privilege scopes.
- Plugins and skills remain declarative until signed/approved by policy plane.
- Generated media plans include brand and safety quality checks.
- Design, agent, and job-template capabilities stay declarative until policy approval binds them to live credentials or side effects.
