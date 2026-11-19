from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.websocket_manager import manager

router = APIRouter()


@router.websocket("/ws/stocks")
async def stock_websocket(websocket: WebSocket):

    print("Có client yêu cầu kết nối WebSocket")

    await manager.connect(websocket)

    print("WebSocket client đã kết nối!")

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("WebSocket client đã ngắt kết nối!")
