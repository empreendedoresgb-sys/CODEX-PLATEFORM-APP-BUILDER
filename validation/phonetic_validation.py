from core.languages.kriol_guinea.phonetics import validate_phonetic_mode as validate_kriol_guinea_mode
from core.languages.registry import get_language


def run_phonetic_validation(phonetic_mode: str, language_id: str = "kriol-guinea") -> None:
    language = get_language(language_id)
    if language.language_id == "kriol-guinea":
        validate_kriol_guinea_mode(phonetic_mode)
