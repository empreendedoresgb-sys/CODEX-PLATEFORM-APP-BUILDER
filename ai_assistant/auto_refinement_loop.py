from ai_assistant.anomaly_detector import detect
from ai_assistant.correction_agent import correct


def refine_until_valid(output: dict, max_rounds: int = 2) -> dict:
    current = output
    for _ in range(max_rounds):
        if not detect(current):
            return current
        current = correct(current)
    return current
