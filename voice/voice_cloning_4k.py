def synthesize(text: str, voice_id: str) -> dict:
    return {"voice_id": voice_id, "audio": f"synth:{text}"}
