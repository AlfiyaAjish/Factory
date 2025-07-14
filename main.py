from fastapi import FastAPI
from scripts.utils.mqtt.mqtt_subscriber import start_subscriber

from scripts.utils.websocket.websocket_manager import redis_alert_listener


import asyncio
from scripts.handler.celery import trigger_report_tasks
# from scripts.service.service import router
from scripts.service import service,auth
from scripts.service.websocket import router as websocket_router

app = FastAPI()


app.include_router(auth.router,tags=["user"])
app.include_router(service.router,tags=["machine"])
app.include_router(trigger_report_tasks.router, prefix="/tasks",tags=["celery"])
app.include_router(websocket_router, prefix="/ws")



redis_task = None

@app.on_event("startup")
async def startup_event():
    # global redis_task
    loop = asyncio.get_running_loop()

    print(" FastAPI Startup: Starting MQTT client...")
    start_subscriber(loop)


    print("Starting Redis Alert Listener...")
    redis_task = asyncio.create_task(redis_alert_listener())

@app.on_event("shutdown")
async def shutdown_event():
    global redis_task
    if redis_task:
        redis_task.cancel()
        try:
            await redis_task
        except asyncio.CancelledError:
            print("Redis Alert Listener gracefully cancelled.")
