from enforcement.foreign_injection_detector import has_foreign_injection


def enforce_drift_control(candidate: dict) -> dict:
    text = candidate.get("result", "")
    if has_foreign_injection(text):
        raise ValueError("Foreign lexical/structural injection detected")
    return candidate
