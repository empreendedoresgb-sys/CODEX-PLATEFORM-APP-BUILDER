from fastapi import APIRouter, WebSocket

router = APIRouter()


@router.websocket("/v1/ws/events")
async def events_socket(ws: WebSocket) -> None:
    await ws.accept()
    await ws.send_text("APBUILDER.APP realtime events channel")
    await ws.close()
