from core.languages.base import LanguageRegistration
from core.languages.registry import get_language


def select_language(language_id: str) -> LanguageRegistration:
    return get_language(language_id)
