from fastapi import FastAPI
from pydantic import BaseModel

from core.engine_controller import process
from core.languages.registry import list_languages
from multilingual.translation_router import route_translation

app = FastAPI(title="APBUILDER.APP API", version="v1")


class TextRequest(BaseModel):
    input: str
    language_id: str = "en"


class MultilingualRequest(BaseModel):
    text: str
    source_language_id: str = "en"
    target_language_id: str = "fr"


class ValidateRequest(BaseModel):
    text: str
    language_id: str = "en"


@app.get("/v1/languages")
def languages() -> dict:
    return {"status": "ok", "languages": list_languages()}


@app.post("/v1/generate/text")
def generate_text(req: TextRequest) -> dict:
    return process(req.model_dump(), language_id=req.language_id)


@app.post("/v1/generate/multilingual")
def generate_multilingual(req: MultilingualRequest) -> dict:
    translated = route_translation(req.text, req.source_language_id, req.target_language_id)
    return {"status": "ok", "data": {"text": translated}}


@app.post("/v1/validate")
def validate(req: ValidateRequest) -> dict:
    try:
        process({"input": req.text}, language_id=req.language_id)
        return {"status": "ok", "compliance": 1.0, "errors": []}
    except ValueError as exc:
        return {
            "status": "failed",
            "compliance": 0.0,
            "errors": [str(exc)],
            "suggested_correction": "Adjust output to selected language rules.",
        }
