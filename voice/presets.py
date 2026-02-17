from dataclasses import dataclass, asdict


@dataclass
class VoicePreset:
    preset_id: str
    voice_id: str
    emotional_mode: str | None = None
    character_mode: str | None = None
    tonal_variant: str | None = None


class PresetStore:
    def __init__(self) -> None:
        self._presets: dict[str, VoicePreset] = {}

    def save(self, preset: VoicePreset) -> dict:
        self._presets[preset.preset_id] = preset
        return asdict(preset)

    def list_all(self) -> list[dict]:
        return [asdict(p) for p in self._presets.values()]
