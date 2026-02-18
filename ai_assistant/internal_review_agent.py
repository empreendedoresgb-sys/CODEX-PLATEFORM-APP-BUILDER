from datetime import UTC, datetime


def review(output: dict) -> dict:
    reviewed = dict(output)
    reviewed["assistant_review"] = {
        "status": "reviewed",
        "timestamp": datetime.now(UTC).isoformat(),
    }
    return reviewed
