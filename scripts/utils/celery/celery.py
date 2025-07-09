
import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    "smart_factory",
    broker=os.getenv("REDIS_BROKER"),
    backend=os.getenv("REDIS_BROKER")
)

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
    include=["scripts.handler.celery.periodic_tasks"]
)
celery_app.config_from_object("scripts.handler.celery.celery_beat")