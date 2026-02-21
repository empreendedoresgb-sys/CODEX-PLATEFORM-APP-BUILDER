def validate_phonetic_mode(phonetic_mode: str) -> None:
    if phonetic_mode != "african":
        raise ValueError("Phonetic mode must be 'african' for kriol-guinea")
