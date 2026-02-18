from ai_assistant.auto_refinement_loop import refine_until_valid
from ai_assistant.internal_review_agent import review
from core.request_router import route_request
from core.response_formatter import format_response


def process(payload: dict) -> dict:
    """Entrypoint orchestration for text/voice/multilingual generation."""
    routed = route_request(payload)
    refined = refine_until_valid(routed)
    reviewed = review(refined)
    return format_response(reviewed)
