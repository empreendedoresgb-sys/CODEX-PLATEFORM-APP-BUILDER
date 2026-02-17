def run_phonetic_validation(phonetic_mode: str) -> None:
    if phonetic_mode != "african":
        raise ValueError("Phonetic mode must be 'african'")
