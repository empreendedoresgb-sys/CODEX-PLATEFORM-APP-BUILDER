import pytest

from core.engine_controller import process
from core.languages.registry import get_language, list_languages
from multilingual.translation_router import route_translation


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


def test_kriol_available_only_when_external_package_installed() -> None:
    ids = {item["id"] for item in list_languages()}
    if "kriol-guinea" in ids:
        language = get_language("kriol-guinea")
        assert language.display_name
    else:
        with pytest.raises(ValueError):
            get_language("kriol-guinea")
