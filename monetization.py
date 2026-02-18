TIERS = {
    "free": {
        "daily_requests": 10,
        "voice_library_size": 20,
        "features": ["basic_voice_output", "limited_templates", "basic_text_to_voice"],
    },
    "pro": {
        "daily_requests": 1000,
        "voice_library_size": 100,
        "features": ["editing_tools", "all_behavior_templates", "audio_export", "usage_analytics"],
    },
    "enterprise": {
        "daily_requests": -1,
        "voice_library_size": 400,
        "features": ["custom_cloning", "dedicated_templates", "api_access", "on_prem_option", "sla_support"],
    },
}


def get_tier(name: str) -> dict:
    key = name.lower()
    if key not in TIERS:
        raise ValueError(f"Unknown tier: {name}")
    return TIERS[key]
