from linguistic.lexical_validator import validate_lexicon


def run_linguistic_validation(text: str) -> None:
    if not validate_lexicon(text):
        raise ValueError("Lexical validation failed")
