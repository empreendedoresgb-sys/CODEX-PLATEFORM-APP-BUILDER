from linguistic.grammar_operator_validator import has_known_operator


def analyze_transcription(content: str, language_hint: str | None = None) -> dict:
    text = content.strip()
    if not text:
        raise ValueError("Transcription content is empty")

    lower = text.lower()
    is_kriol = any(marker in lower for marker in ["kriol", "n'ka", "ka ", " na "])
    operators = [token for token in text.upper().split() if token in {"KA", "NA", "TA", "STA", "PA", "N'KA"}]

    return {
        "language_detected": "KriolGB" if is_kriol else (language_hint or "unknown"),
        "confidence": 0.97 if is_kriol else 0.8,
        "operators_detected": operators,
        "oral_markers": ["pause_pattern"] if "..." in text or "—" in text else [],
        "cultural_keywords": [kw for kw in ["tabanka", "griot", "ditus"] if kw in lower],
        "semantic_intent": "cultural_narrative" if is_kriol else "general",
        "ntopy4_compliance": has_known_operator(text),
    }
