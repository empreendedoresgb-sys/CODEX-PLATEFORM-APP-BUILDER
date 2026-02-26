from core.languages.selector import select_language


def route_translation(text: str, source_language_id: str, target_language_id: str) -> str:
    source = select_language(source_language_id)
    target = select_language(target_language_id)
    return f"[{source.language_id}->{target.language_id}] {text}"
