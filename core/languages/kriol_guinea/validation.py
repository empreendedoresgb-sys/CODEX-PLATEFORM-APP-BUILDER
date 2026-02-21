from core.languages.kriol_guinea.grammar import validate_grammar
from core.languages.kriol_guinea.lexicon import validate_lexicon


def validate_text(text: str) -> None:
    if not validate_lexicon(text):
        raise ValueError("Lexical validation failed for kriol-guinea")
    if not validate_grammar(text):
        raise ValueError("Grammar validation failed for kriol-guinea")
