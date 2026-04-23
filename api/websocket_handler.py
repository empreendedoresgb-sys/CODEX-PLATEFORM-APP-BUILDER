from __future__ import annotations

from fastapi import APIRouter, WebSocket

from orchestrator.repository import get_events

router = APIRouter()


@router.websocket("/v1/ws/events")
async def events_socket(ws: WebSocket) -> None:
    await ws.accept()
    run_id = ws.query_params.get("run_id")

    if not run_id:
        await ws.send_json({"status": "ok", "message": "APBUILDER.APP realtime events channel"})
        await ws.close()
        return

    try:
        events = [item.model_dump() for item in get_events(run_id)]
        await ws.send_json({"status": "ok", "run_id": run_id, "events": events})
    except ValueError as exc:
        await ws.send_json({"status": "failed", "error": str(exc)})
    finally:
        await ws.close()
