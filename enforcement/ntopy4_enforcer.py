from core.languages.kriol_guinea.grammar import validate_grammar


def enforce_ntopy4(text: str) -> None:
    if not validate_grammar(text):
        raise ValueError("Ntopy-4 operator compliance failed")
