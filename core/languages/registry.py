from __future__ import annotations

from core.languages.base import LanguageRegistration, LanguageRuntime
from core.languages.builtin import GenericLanguageRuntime

_RUNTIME_REGISTRY: dict[str, LanguageRuntime] = {
    "en": GenericLanguageRuntime(language_id="en", display_name="English"),
    "fr": GenericLanguageRuntime(language_id="fr", display_name="French"),
    "pt": GenericLanguageRuntime(language_id="pt", display_name="Portuguese"),
}

try:
    from kriol_guinea_language_core.runtime import KriolGuineaRuntime

    _RUNTIME_REGISTRY["kriol-guinea"] = KriolGuineaRuntime()
except ModuleNotFoundError:
    # External dependency not installed in this environment.
    pass


def list_languages() -> list[dict[str, str]]:
    return [
        {
            "id": runtime.language_id,
            "display_name": runtime.display_name,
            "type": runtime.language_type,
        }
        for runtime in _RUNTIME_REGISTRY.values()
    ]


def get_language(language_id: str) -> LanguageRegistration:
    runtime = get_runtime(language_id)
    return LanguageRegistration(
        language_id=runtime.language_id,
        display_name=runtime.display_name,
        language_type=runtime.language_type,
    )


def get_runtime(language_id: str) -> LanguageRuntime:
    normalized = language_id.strip().lower()
    if normalized not in _RUNTIME_REGISTRY:
        available = ", ".join(sorted(_RUNTIME_REGISTRY))
        raise ValueError(f"Unsupported language '{language_id}'. Supported: {available}")
    return _RUNTIME_REGISTRY[normalized]
