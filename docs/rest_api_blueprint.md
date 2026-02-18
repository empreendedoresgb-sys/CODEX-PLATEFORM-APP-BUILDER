# REST API Blueprint (Full Expansion)

This blueprint maps all major modules to API-first contracts.

## Domains
- Generation: text, voice, multilingual
- Validation: Ntopy-4, lexical, semantic
- Voice Labs: templates, presets, clone training
- File IO: import/export
- QR: creation, analytics
- Transcription: multimodal with Kriol priority
- Billing: invoices, webhooks
- System: health

## Canonical Validation Loop
`generate -> validate -> correct -> revalidate -> approve`

## Source of truth
- Machine-readable contract: `api/contracts/rest_api_blueprint.json`
- Existing runtime endpoints: `api/rest_endpoints.py`
