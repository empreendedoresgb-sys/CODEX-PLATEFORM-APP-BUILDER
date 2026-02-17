CANONICAL_TERMS = {"kriol", "ntopy-4", "tira", "boka", "binhu"}


def validate_lexicon(text: str) -> bool:
    lower = text.lower()
    return any(term in lower for term in CANONICAL_TERMS)
