from core.request_router import route_request
from core.response_formatter import format_response


def process(payload: dict, language_id: str = "en") -> dict:
    """Entrypoint orchestration for platform text/multilingual generation."""
    routed = route_request(payload, language_id=language_id)
    return format_response(routed)
