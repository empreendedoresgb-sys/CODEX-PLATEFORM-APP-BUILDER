from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class LanguageRuntime(Protocol):
    language_id: str
    display_name: str
    language_type: str

    def normalize(self, text: str) -> str: ...

    def validate_lexicon(self, text: str) -> bool: ...

    def validate_grammar(self, text: str) -> bool: ...

    def validate_phonetic_mode(self, phonetic_mode: str) -> None: ...

    def prompt_conditioning(self, prompt: str) -> str: ...


@dataclass(frozen=True)
class LanguageRegistration:
    language_id: str
    display_name: str
    language_type: str
