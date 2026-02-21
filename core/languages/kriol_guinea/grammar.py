OPERATORS = {
    "KA", "NA", "TA", "STA", "PA", "SI", "SA", "SO", "SON", "SIN", "MA",
    "TAN", "N'", "N'KA", "KI", "KE", "EL", "LA", "BA", "NAN", "BU", "U",
    "BO", "KU", "I", "E", "DI"
}


def validate_grammar(text: str) -> bool:
    tokens = {token.strip(".,!?;:").upper() for token in text.split()}
    return bool(tokens & OPERATORS)
