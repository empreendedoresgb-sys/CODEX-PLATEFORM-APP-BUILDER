from linguistic.grammar_operator_validator import has_known_operator


CONFLICT_MARKERS = ("<<<<<<<", "=======", ">>>>>>>")


def detect(output: dict) -> bool:
    """Detect anomalies that should trigger assistant correction flow."""
    text = str(output.get("result", ""))
    if not text.strip():
        return True
    if any(marker in text for marker in CONFLICT_MARKERS):
        return True
    if not has_known_operator(text):
        return True
    return False
