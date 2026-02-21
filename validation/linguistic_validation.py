from core.languages.kriol_guinea.validation import validate_text
from core.languages.registry import get_language


def run_linguistic_validation(text: str, language_id: str = "kriol-guinea") -> None:
    language = get_language(language_id)
    if language.language_id == "kriol-guinea":
        validate_text(text)
        return
    if not text.strip():
        raise ValueError(f"Linguistic validation failed for {language.language_id}: empty content")
