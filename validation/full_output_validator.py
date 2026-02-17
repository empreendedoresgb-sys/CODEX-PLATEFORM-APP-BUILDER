from validation.linguistic_validation import run_linguistic_validation
from validation.ntopy4_compliance_check import run_ntopy4_check
from validation.semantic_integrity_check import run_semantic_integrity_check


def validate_output(candidate: dict) -> None:
    text = candidate.get("result", "")
    run_linguistic_validation(text)
    run_ntopy4_check(text)
    run_semantic_integrity_check(text)
