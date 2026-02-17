from fastapi import FastAPI
from pydantic import BaseModel

from core.engine_controller import process
from multilingual.translation_router import route_translation
from voice.voice_cloning_4k import synthesize
from validation.phonetic_validation import run_phonetic_validation

app = FastAPI(title="KriolGB IA Voice API", version="v1")


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


class MultilingualRequest(BaseModel):
    text: str
    target_language: str
    maintain_voice_identity: bool = True


class ValidateRequest(BaseModel):
    text: str
    check_ntopy4: bool = True
    check_lexical: bool = True


@app.post("/v1/generate/text")
def generate_text(req: TextRequest) -> dict:
    return process(req.model_dump())


@app.post("/v1/generate/voice")
def generate_voice(req: VoiceRequest) -> dict:
    run_phonetic_validation(req.phonetic_mode)
    return {"status": "ok", "data": synthesize(req.text, req.voice_id)}


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
