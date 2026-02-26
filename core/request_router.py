from enforcement.anti_drift_engine import enforce_drift_control
from validation.full_output_validator import validate_output


def route_request(payload: dict, language_id: str = "en") -> dict:
    """Route request through enforcement + validation layers."""
    candidate = {"result": payload.get("input") or payload.get("text", "")}
    stabilized = enforce_drift_control(candidate)
    validate_output(stabilized, language_id=language_id)
    return stabilized
