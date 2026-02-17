import pytest

from core.engine_controller import process


def test_process_accepts_canonical_text() -> None:
    out = process({"input": "Kriol KA na tira boka na binhu"})
    assert out["status"] == "ok"


def test_process_rejects_missing_operator() -> None:
    with pytest.raises(ValueError):
        process({"input": "kriol tira boka binhu"})
