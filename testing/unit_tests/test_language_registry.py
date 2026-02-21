import pytest

from core.engine_controller import process
from core.languages.registry import get_language, list_languages
from multilingual.translation_router import route_translation


def test_kriol_guinea_registered() -> None:
    language = get_language("kriol-guinea")
    assert language.display_name == "Kriol Guinea"
    assert language.language_type == "National Linguistic System"


def test_languages_contains_global_and_kriol_guinea() -> None:
    ids = {item["id"] for item in list_languages()}
    assert {"kriol-guinea", "en", "fr", "pt"}.issubset(ids)


def test_process_respects_language_selection() -> None:
    out = process({"input": "Kriol KA na tira boka na binhu"}, language_id="kriol-guinea")
    assert out["status"] == "ok"


def test_process_rejects_unknown_language() -> None:
    with pytest.raises(ValueError):
        process({"input": "hello world"}, language_id="es")


def test_multilingual_router_uses_registry_ids() -> None:
    out = route_translation("hello", "kriol-guinea", "fr")
    assert out.startswith("[kriol-guinea->fr]")


def test_multilingual_router_rejects_unknown_language() -> None:
    with pytest.raises(ValueError):
        route_translation("hello", "kriol-guinea", "es")
