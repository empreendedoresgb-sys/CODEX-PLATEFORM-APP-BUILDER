from core.request_router import route_request
from core.response_formatter import format_response


def process(payload: dict, language_id: str = "kriol-guinea") -> dict:
    """Entrypoint orchestration for text/voice/multilingual generation."""
    routed = route_request(payload, language_id=language_id)
    return format_response(routed)
