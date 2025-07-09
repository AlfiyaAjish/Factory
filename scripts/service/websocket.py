# from fastapi import APIRouter, WebSocket
# from scripts.utils.websocket_manager import connect_client, disconnect_client
# import asyncio
#
# router = APIRouter()
#
# @router.websocket("/alerts")
# async def websocket_endpoint(ws: WebSocket):
#     await connect_client(ws)
#     try:
#         print(" WebSocket client connected")
#         while True:
#             await asyncio.sleep(1)  # keep the connection alive
#     except Exception as e:
#         print(f" WebSocket error: {e}")
#     finally:
#         disconnect_client(ws)
#         print(" WebSocket client disconnected")
#


# routers/alerts_websocket.py

from fastapi import APIRouter, WebSocket
from scripts.utils.websocket.websocket_manager import connect_client, disconnect_client
import asyncio

router = APIRouter()

@router.websocket("/alerts")
async def websocket_endpoint(ws: WebSocket):
    await connect_client(ws)
    try:
        print(" WebSocket client connected")
        while True:
            await asyncio.sleep(1)  # keep connection alive
    except Exception as e:
        print(f" WebSocket error: {e}")
    finally:
        disconnect_client(ws)
        print(" WebSocket client disconnected")
