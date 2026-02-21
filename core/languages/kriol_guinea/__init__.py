from core.languages.kriol_guinea.grammar import validate_grammar
from core.languages.kriol_guinea.lexicon import validate_lexicon
from core.languages.kriol_guinea.localization import get_localization_hooks
from core.languages.kriol_guinea.orthography import normalize_orthography
from core.languages.kriol_guinea.phonetics import validate_phonetic_mode
from core.languages.kriol_guinea.prompt_conditioning import condition_prompt

LANGUAGE_ID = "kriol-guinea"
DISPLAY_NAME = "Kriol Guinea"
LANGUAGE_TYPE = "National Linguistic System"

__all__ = [
    "LANGUAGE_ID",
    "DISPLAY_NAME",
    "LANGUAGE_TYPE",
    "normalize_orthography",
    "validate_lexicon",
    "validate_grammar",
    "validate_phonetic_mode",
    "condition_prompt",
    "get_localization_hooks",
]
