import hashlib
import hmac
import json
import os
from datetime import UTC, datetime
from uuid import uuid4

_invoices: list[dict] = []


def create_invoice(org_id: str, amount_cents: int, currency: str = "USD") -> dict:
    invoice = {
        "invoice_id": str(uuid4()),
        "org_id": org_id,
        "amount_cents": amount_cents,
        "currency": currency,
        "status": "issued",
        "created_at": datetime.now(UTC).isoformat(),
    }
    _invoices.append(invoice)
    return invoice


def list_invoices(org_id: str | None = None) -> list[dict]:
    if org_id:
        return [inv for inv in _invoices if inv["org_id"] == org_id]
    return list(_invoices)


def validate_webhook_signature(payload: dict, signature: str | None) -> bool:
    secret = os.getenv("PAYMENT_WEBHOOK_SECRET", "dev-secret")
    expected = hmac.new(secret.encode(), json.dumps(payload, sort_keys=True).encode(), hashlib.sha256).hexdigest()
    return bool(signature) and hmac.compare_digest(expected, signature)
