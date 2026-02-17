BLOCKED_MARKERS = {"dialect", "pidgin reinterpretation"}


def has_foreign_injection(text: str) -> bool:
    lower = text.lower()
    return any(marker in lower for marker in BLOCKED_MARKERS)
