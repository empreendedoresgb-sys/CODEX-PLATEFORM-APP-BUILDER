def run(prompt: str) -> list[str]:
    issues: list[str] = []
    if len(prompt.strip()) < 3:
        issues.append("Prompt too short")
    return issues
