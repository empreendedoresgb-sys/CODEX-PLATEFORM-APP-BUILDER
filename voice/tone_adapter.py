def adapt_tone(text: str, emotion: str | None = None) -> str:
    return text if not emotion else f"[{emotion}] {text}"
