MODIFICATION_KEYWORD = "Ntopy-4Develop"


def is_modification_allowed(payload: dict) -> bool:
    return payload.get("modification_key") == MODIFICATION_KEYWORD
