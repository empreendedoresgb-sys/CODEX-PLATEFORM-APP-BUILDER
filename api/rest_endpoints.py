from fastapi import FastAPI
from pydantic import BaseModel, Field

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
