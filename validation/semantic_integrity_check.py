def run_semantic_integrity_check(text: str) -> None:
    if not text.strip():
        raise ValueError("Semantic integrity failed: empty content")
