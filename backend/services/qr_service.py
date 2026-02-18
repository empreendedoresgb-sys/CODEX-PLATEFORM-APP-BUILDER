from datetime import UTC, datetime, timedelta
from uuid import uuid4

_qr_stats: dict[str, dict] = {}


def create_qr(target_type: str, target_id: str, expires_in_seconds: int = 3600) -> dict:
    token = uuid4().hex
    expires_at = datetime.now(UTC) + timedelta(seconds=expires_in_seconds)
    _qr_stats[token] = {
        "target_type": target_type,
        "target_id": target_id,
        "scans": 0,
        "last_scan_at": None,
        "expires_at": expires_at.isoformat(),
    }
    return {"token": token, "expires_at": expires_at.isoformat()}


def get_qr_stats(token: str) -> dict:
    if token not in _qr_stats:
        raise ValueError("QR token not found")
    data = _qr_stats[token]
    return {"token": token, **data}
