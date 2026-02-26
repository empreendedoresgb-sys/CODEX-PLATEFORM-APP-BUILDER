import pytest

from core.engine_controller import process
from core.languages.base import LanguageRuntime
from core.languages.registry import get_language, list_languages, register_runtime
from multilingual.translation_router import route_translation


class _EsRuntime(LanguageRuntime):
    language_id = "es"
    display_name = "Spanish"
    language_type = "Global"

    def normalize(self, text: str) -> str:
        return text.strip()

    def validate_lexicon(self, text: str) -> bool:
        return bool(text.strip())

    def validate_grammar(self, text: str) -> bool:
        return bool(text.strip())

    def validate_phonetic_mode(self, phonetic_mode: str) -> None:
        return None

    def prompt_conditioning(self, prompt: str) -> str:
        return prompt

    def validate_text(self, text: str) -> None:
        if not text.strip():
            raise ValueError("empty content")


def test_global_languages_registered() -> None:
    ids = {item["id"] for item in list_languages()}
    assert {"en", "fr", "pt"}.issubset(ids)


def test_process_respects_language_selection() -> None:
    out = process({"input": "hello world"}, language_id="en")
    assert out["status"] == "ok"


def test_process_rejects_unknown_language() -> None:
    with pytest.raises(ValueError):
        process({"input": "hello world"}, language_id="es")


def test_multilingual_router_uses_registry_ids() -> None:
    out = route_translation("hello", "en", "fr")
    assert out.startswith("[en->fr]")


def test_multilingual_router_rejects_unknown_language() -> None:
    with pytest.raises(ValueError):
        route_translation("hello", "en", "es")


def test_runtime_registration_contract() -> None:
    register_runtime(_EsRuntime())
    ids = {item["id"] for item in list_languages()}
    assert "es" in ids


def test_kriol_available_only_when_external_package_installed() -> None:
    ids = {item["id"] for item in list_languages()}
    if "kriol-guinea" in ids:
        language = get_language("kriol-guinea")
        assert language.display_name
    else:
        with pytest.raises(ValueError):
            get_language("kriol-guinea")
