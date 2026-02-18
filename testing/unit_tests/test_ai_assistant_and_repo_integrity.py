import re
from pathlib import Path

from core.engine_controller import process


CONFLICT_LINE_RE = re.compile(r"^(<<<<<<<|=======|>>>>>>>)", re.MULTILINE)


def test_process_adds_assistant_review_metadata() -> None:
    out = process({"input": "Kriol KA na tira boka na binhu"})
    review = out["data"].get("assistant_review", {})
    assert review.get("status") == "reviewed"
    assert "timestamp" in review


def test_repository_has_no_merge_conflict_markers() -> None:
    roots = [
        Path("api"),
        Path("core"),
        Path("ai_assistant"),
        Path("validation"),
        Path("enforcement"),
        Path("testing"),
        Path("docs"),
        Path(".github"),
    ]
    offenders: list[str] = []

    for root in roots:
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix in {".png", ".jpg", ".jpeg", ".gif", ".ico", ".wav", ".mp3", ".webm"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if CONFLICT_LINE_RE.search(text):
                offenders.append(str(path))

    assert not offenders, f"Merge conflict markers found in files: {offenders}"
