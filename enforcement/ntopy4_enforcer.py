from linguistic.grammar_operator_validator import has_known_operator


def enforce_ntopy4(text: str) -> None:
    if not has_known_operator(text):
        raise ValueError("Ntopy-4 operator compliance failed")
