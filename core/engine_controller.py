from core.request_router import route_request
from core.response_formatter import format_response


def process(payload: dict) -> dict:
    """Entrypoint orchestration for text/voice/multilingual generation."""
    routed = route_request(payload)
    return format_response(routed)
