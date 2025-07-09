# from fastapi import WebSocket
# from bson import ObjectId
#
# clients = []
#
# async def connect_client(ws: WebSocket):
#     await ws.accept()
#     clients.append(ws)
#
# def disconnect_client(ws: WebSocket):
#     if ws in clients:
#         clients.remove(ws)
#
# async def alert_clients(alert: dict):
#     print(" Broadcasting alert to WebSocket clients...")
#
#     if "_id" in alert and isinstance(alert["_id"], ObjectId):
#         alert["_id"] = str(alert["_id"])
#
#     disconnected = []
#     for ws in clients:
#         try:
#             await ws.send_json(alert)
#         except Exception as e:
#             print(f" Failed to send alert to a client: {e}")
#             disconnected.append(ws)
#
#     for ws in disconnected:
#         disconnect_client(ws)
#
#
#


import asyncio
import redis.asyncio as redis
import json
import os
from bson import ObjectId

clients = []
redis_listener_task = None  # <-- Task holder

REDIS_BROKER = os.getenv("REDIS_BROKER")
ALERT_CHANNEL = os.getenv("ALERT_CHANNEL", "alert_notifications")

async def connect_client(ws):
    await ws.accept()
    clients.append(ws)

def disconnect_client(ws):
    if ws in clients:
        clients.remove(ws)

async def alert_clients(alert: dict):
    if "_id" in alert and isinstance(alert["_id"], ObjectId):
        alert["_id"] = str(alert["_id"])

    print("Broadcasting alert to WebSocket clients:", alert)

    for ws in clients[:]:  # Copy to avoid iteration issues
        try:
            await ws.send_json(alert)
        except Exception as e:
            print(f"Client disconnected or failed: {e}")
            disconnect_client(ws)


async def redis_alert_listener():
    print(f"Redis subscriber started for channel: {ALERT_CHANNEL}")
    r = redis.from_url(REDIS_BROKER, decode_responses=True)
    pubsub = r.pubsub()
    await pubsub.subscribe(ALERT_CHANNEL)

    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                alert = json.loads(message["data"])
                await alert_clients(alert)
    except asyncio.CancelledError:
        print(" Redis subscriber task cancelled")
        await pubsub.unsubscribe(ALERT_CHANNEL)
        await pubsub.close()
    except Exception as e:
        print(f" Redis listener error: {e}")
