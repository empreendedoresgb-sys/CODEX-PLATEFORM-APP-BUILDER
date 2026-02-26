def run(prompt: str) -> list[str]:
    issues: list[str] = []
    if len(prompt.strip()) < 10:
        issues.append("Prompt too short for safe orchestration")
    return issues
