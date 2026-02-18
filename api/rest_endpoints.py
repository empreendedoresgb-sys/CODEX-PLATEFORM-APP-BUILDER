from datetime import UTC, datetime

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from backend.services.billing_service import create_invoice, list_invoices, validate_webhook_signature
from backend.services.file_service import export_file, import_file
from backend.services.qr_service import create_qr, get_qr_stats
from backend.services.transcription_service import analyze_transcription
from backend.services.voice_clone_service import start_training_job
from core.engine_controller import process
from monetization import get_tier
from multilingual.translation_router import route_translation
from voice.editing.processing import apply_processing
from voice.labs.mode_router import validate_mode_selection
from voice.labs.template_manager import list_templates
from voice.presets import PresetStore, VoicePreset
from voice.voice_cloning_4k import synthesize
from validation.phonetic_validation import run_phonetic_validation

app = FastAPI(title="KriolGB IA Voice API", version="v1")
preset_store = PresetStore()


class TextRequest(BaseModel):
    input: str
    mode: str = "kriol"
    ntopy4: bool = True
    validation: bool = True


class VoiceRequest(BaseModel):
    text: str
    voice_id: str
    phonetic_mode: str = "african"
    preserve_identity: bool = True
    emotional_mode: str | None = None
    character_mode: str | None = None
    tonal_variant: str | None = None
    pitch: float = Field(default=1.0, ge=0.5, le=2.0)
    tempo: float = Field(default=1.0, ge=0.5, le=2.0)
    energy: float = Field(default=1.0, ge=0.1, le=3.0)


class MultilingualRequest(BaseModel):
    text: str
    target_language: str
    maintain_voice_identity: bool = True


class ValidateRequest(BaseModel):
    text: str
    check_ntopy4: bool = True
    check_lexical: bool = True


class PresetRequest(BaseModel):
    preset_id: str
    voice_id: str
    emotional_mode: str | None = None
    character_mode: str | None = None
    tonal_variant: str | None = None


class FileImportRequest(BaseModel):
    filename: str


class FileExportRequest(BaseModel):
    resource_id: str
    output_format: str


class QrCreateRequest(BaseModel):
    target_type: str
    target_id: str
    expires_in_seconds: int = Field(default=3600, ge=60)


class TranscriptionRequest(BaseModel):
    content: str
    language_hint: str | None = None


class VoiceCloneRequest(BaseModel):
    user_id: str
    dataset_reference: str


class InvoiceCreateRequest(BaseModel):
    org_id: str
    amount_cents: int = Field(ge=1)
    currency: str = "USD"


@app.get("/v1/system/health")
def system_health() -> dict:
    return {
        "status": "ok",
        "service": "kriolgb-ia-voice",
        "version": "Ntopy-4",
        "timestamp": datetime.now(UTC).isoformat(),
    }


@app.get("/v1/voice/templates")
def voice_templates() -> dict:
    return {"status": "ok", "templates": list_templates()}


@app.get("/v1/monetization/tiers/{tier_name}")
def monetization_tier(tier_name: str) -> dict:
    return {"status": "ok", "tier": get_tier(tier_name)}


@app.post("/v1/voice/presets")
def save_preset(req: PresetRequest) -> dict:
    validate_mode_selection(req.emotional_mode, req.character_mode, req.tonal_variant)
    preset = VoicePreset(**req.model_dump())
    return {"status": "ok", "preset": preset_store.save(preset)}


@app.get("/v1/voice/presets")
def list_presets() -> dict:
    return {"status": "ok", "presets": preset_store.list_all()}


@app.post("/v1/generate/text")
def generate_text(req: TextRequest) -> dict:
    return process(req.model_dump())


@app.post("/v1/generate/voice")
def generate_voice(req: VoiceRequest) -> dict:
    run_phonetic_validation(req.phonetic_mode)
    validate_mode_selection(req.emotional_mode, req.character_mode, req.tonal_variant)
    processing = apply_processing(req.text, pitch=req.pitch, tempo=req.tempo, energy=req.energy)
    audio = synthesize(processing["text"], req.voice_id)
    return {"status": "ok", "data": {"audio": audio, "processing": processing}}


@app.post("/v1/generate/multilingual")
def generate_multilingual(req: MultilingualRequest) -> dict:
    translated = route_translation(req.text, req.target_language)
    return {"status": "ok", "data": {"text": translated}}


@app.post("/v1/validate")
def validate(req: ValidateRequest) -> dict:
    try:
        process({"input": req.text})
        return {"status": "ok", "compliance": 1.0, "errors": []}
    except ValueError as exc:
        return {
            "status": "failed",
            "compliance": 0.0,
            "errors": [str(exc)],
            "suggested_correction": "Adjust output to Ntopy-4 canonical operators and lexicon.",
        }


@app.post("/v1/files/import")
def files_import(req: FileImportRequest) -> dict:
    try:
        imported = import_file(req.filename)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "ok", "data": imported.__dict__}


@app.post("/v1/files/export")
def files_export(req: FileExportRequest) -> dict:
    try:
        exported = export_file(req.resource_id, req.output_format)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "ok", "data": exported}


@app.post("/v1/qr/create")
def qr_create(req: QrCreateRequest) -> dict:
    return {"status": "ok", "data": create_qr(req.target_type, req.target_id, req.expires_in_seconds)}


@app.get("/v1/qr/{token}/stats")
def qr_stats(token: str) -> dict:
    try:
        return {"status": "ok", "data": get_qr_stats(token)}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/v1/transcription/analyze")
def transcription_analyze(req: TranscriptionRequest) -> dict:
    try:
        result = analyze_transcription(req.content, req.language_hint)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "ok", "data": result}


@app.post("/v1/voice/clone/train")
def voice_clone_train(req: VoiceCloneRequest) -> dict:
    return {"status": "ok", "data": start_training_job(req.user_id, req.dataset_reference)}


@app.get("/v1/billing/invoices")
def billing_invoices_list(org_id: str | None = None) -> dict:
    return {"status": "ok", "data": list_invoices(org_id=org_id)}


@app.post("/v1/billing/invoices")
def billing_invoices_create(req: InvoiceCreateRequest) -> dict:
    return {"status": "ok", "data": create_invoice(req.org_id, req.amount_cents, req.currency)}


@app.post("/v1/billing/webhook/payment")
def billing_webhook_payment(payload: dict, x_signature: str | None = Header(default=None, alias="X-Signature")) -> dict:
    if not validate_webhook_signature(payload, x_signature):
        raise HTTPException(status_code=403, detail="Invalid webhook signature")
    return {"status": "ok", "received": True, "event": payload.get("event", "unknown")}
