def correct(output: dict) -> dict:
    """Minimal safe correction: normalize whitespace and annotate remediation."""
    text = str(output.get("result", ""))
    normalized = " ".join(text.replace("\n", " ").split())
    corrected = dict(output)
    corrected["result"] = normalized
    corrected["assistant_correction_applied"] = True
    return corrected
