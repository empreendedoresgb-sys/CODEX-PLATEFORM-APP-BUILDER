from voice.labs.behavior_profiles import BEHAVIOR_PROFILES


def list_templates() -> list[dict]:
    return [
        {
            "template_name": p.template_name,
            "behavior_category": p.behavior_category,
            "supported_voices": p.supported_voices,
            "description": p.description,
        }
        for p in BEHAVIOR_PROFILES
    ]
