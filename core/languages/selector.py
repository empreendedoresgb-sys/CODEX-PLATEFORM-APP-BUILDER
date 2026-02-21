from core.languages.base import LanguageRuntime
from core.languages.registry import get_runtime


def select_language(language_id: str) -> LanguageRuntime:
    return get_runtime(language_id)
