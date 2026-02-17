from linguistic.orthography_checker import normalize_orthography


def normalize(text: str) -> str:
    return normalize_orthography(text)
