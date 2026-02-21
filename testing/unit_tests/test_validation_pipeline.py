import pytest

from core.engine_controller import process


def test_process_accepts_text() -> None:
    out = process({"input": "Builder pipeline content"}, language_id="en")
    assert out["status"] == "ok"


def test_process_rejects_empty_text() -> None:
    with pytest.raises(ValueError):
        process({"input": "   "}, language_id="en")
