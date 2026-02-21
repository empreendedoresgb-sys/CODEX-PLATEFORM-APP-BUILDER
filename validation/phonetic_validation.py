from core.languages.registry import get_runtime


def run_phonetic_validation(phonetic_mode: str, language_id: str = "en") -> None:
    runtime = get_runtime(language_id)
    runtime.validate_phonetic_mode(phonetic_mode)
