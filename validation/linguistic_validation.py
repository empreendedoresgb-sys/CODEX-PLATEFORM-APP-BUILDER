from core.languages.registry import get_runtime


def run_linguistic_validation(text: str, language_id: str = "en") -> None:
    runtime = get_runtime(language_id)
    runtime.validate_text(text)
