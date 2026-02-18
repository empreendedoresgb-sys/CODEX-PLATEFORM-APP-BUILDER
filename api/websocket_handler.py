from fastapi import APIRouter, WebSocket

router = APIRouter()


@router.websocket("/v1/ws/voice")
async def voice_socket(ws: WebSocket) -> None:
    await ws.accept()
    while True:
        text = await ws.receive_text()
        await ws.send_text(f"ack:{text}")
