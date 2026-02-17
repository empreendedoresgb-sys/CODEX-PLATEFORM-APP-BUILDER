def apply_processing(text: str, pitch: float = 1.0, tempo: float = 1.0, energy: float = 1.0) -> dict:
    return {
        "text": text,
        "pitch": round(pitch, 3),
        "tempo": round(tempo, 3),
        "energy": round(energy, 3),
        "equalizer": {"low": 0, "mid": 0, "high": 0},
    }
