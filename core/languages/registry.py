from __future__ import annotations

from core.languages.base import LanguageRegistration
from core.languages import kriol_guinea

_SUPPORTED_LANGUAGES: dict[str, LanguageRegistration] = {
    "kriol-guinea": LanguageRegistration(
        language_id=kriol_guinea.LANGUAGE_ID,
        display_name=kriol_guinea.DISPLAY_NAME,
        language_type=kriol_guinea.LANGUAGE_TYPE,
    ),
    "en": LanguageRegistration(language_id="en", display_name="English", language_type="Global"),
    "fr": LanguageRegistration(language_id="fr", display_name="French", language_type="Global"),
    "pt": LanguageRegistration(language_id="pt", display_name="Portuguese", language_type="Global"),
}


def list_languages() -> list[dict[str, str]]:
    return [
        {
            "id": item.language_id,
            "display_name": item.display_name,
            "type": item.language_type,
        }
        for item in _SUPPORTED_LANGUAGES.values()
    ]


def get_language(language_id: str) -> LanguageRegistration:
    normalized = language_id.strip().lower()
    if normalized not in _SUPPORTED_LANGUAGES:
        available = ", ".join(sorted(_SUPPORTED_LANGUAGES))
        raise ValueError(f"Unsupported language '{language_id}'. Supported: {available}")
    return _SUPPORTED_LANGUAGES[normalized]
