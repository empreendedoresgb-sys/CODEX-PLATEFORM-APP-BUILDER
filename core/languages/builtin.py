from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GenericLanguageRuntime:
    language_id: str
    display_name: str
    language_type: str = "Global"

    def normalize(self, text: str) -> str:
        return " ".join(text.split())

    def validate_lexicon(self, text: str) -> bool:
        return bool(text.strip())

    def validate_grammar(self, text: str) -> bool:
        return bool(text.strip())

    def validate_phonetic_mode(self, phonetic_mode: str) -> None:
        return None

    def prompt_conditioning(self, prompt: str) -> str:
        return f"[{self.language_id}] {prompt}"

    def validate_text(self, text: str) -> None:
        if not text.strip():
            raise ValueError(f"Linguistic validation failed for {self.language_id}: empty content")
