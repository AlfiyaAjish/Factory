from scripts.constants.app_constants import AppConstants
import os
from celery import Celery
from dotenv import load_dotenv
from datetime import timedelta

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
    task_reject_on_worker_lost=True,
    worker_concurrency=AppConstants.WORKER_CONCURRENCY,
    task_default_retry_delay=AppConstants.TASK_DEFAULT_RETRY_DELAY,
    task_max_retries=AppConstants.TASK_MAX_RETRIES,
    result_expires=AppConstants.RESULT_EXPIRES,
    task_acks_late=AppConstants.TASK_ACKS_LATE,
    worker_max_tasks_per_child=AppConstants.WORKER_MAX_TASKS_PER_CHILD,
    result_compression=AppConstants.RESULT_COMPRESSION,
    include=["scripts.handler.celery.periodic_tasks"]
)
celery_app.config_from_object("scripts.handler.celery.celery_beat")