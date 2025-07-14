from scripts.constants.app_constants import AppConstants
import os
from celery import Celery
from dotenv import load_dotenv
from datetime import timedelta
import ssl

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
    timezone='Asia/Kolkata',
    include=["scripts.handler.celery.periodic_tasks"]
)
celery_app.config_from_object("scripts.handler.celery.celery_beat")

celery_app.conf.broker_use_ssl = {
    'ssl_cert_reqs': ssl.CERT_NONE
}


celery_app.conf.redis_backend_use_ssl = {
    'ssl_cert_reqs': ssl.CERT_NONE
}