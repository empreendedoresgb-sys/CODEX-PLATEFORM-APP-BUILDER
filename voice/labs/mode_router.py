from voice.labs.character_modes import CHARACTER_MODES
from voice.labs.cultural_variants import KRIOL_TONAL_VARIANTS
from voice.labs.emotional_modes import EMOTIONAL_MODES


def validate_mode_selection(emotional_mode: str | None, character_mode: str | None, tonal_variant: str | None) -> None:
    if emotional_mode and emotional_mode not in EMOTIONAL_MODES:
        raise ValueError(f"Unsupported emotional mode: {emotional_mode}")
    if character_mode and character_mode not in CHARACTER_MODES:
        raise ValueError(f"Unsupported character mode: {character_mode}")
    if tonal_variant and tonal_variant not in KRIOL_TONAL_VARIANTS:
        raise ValueError(f"Unsupported tonal variant: {tonal_variant}")
