from dataclasses import dataclass


@dataclass(frozen=True)
class BehaviorProfile:
    template_name: str
    behavior_category: str
    description: str
    supported_voices: list[str]


BEHAVIOR_PROFILES: list[BehaviorProfile] = [
    BehaviorProfile("storytelling_mode", "creative", "Narrative-driven cadence with controlled pauses.", ["guine_male_01", "guine_female_01"]),
    BehaviorProfile("poetic_romantic_mode", "emotional", "Soft contour and warm harmonic profile.", ["guine_female_01"]),
    BehaviorProfile("political_speech_mode", "leadership", "Clear projection and authority pacing.", ["guine_male_01", "guine_male_02"]),
    BehaviorProfile("podcast_mode", "media", "Balanced EQ and smooth transitions for long-form audio.", ["guine_male_01", "guine_female_01", "guine_female_02"]),
    BehaviorProfile("rapper_mode", "entertainment", "Rhythmic emphasis and beat-aligned punch.", ["guine_male_02", "guine_female_02"]),
]
