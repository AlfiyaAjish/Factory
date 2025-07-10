from celery.schedules import crontab
from scripts.utils.celery.celery import celery_app

celery_app.conf.beat_schedule = {
    "run-daily-report-chain": {
        "task": "run_daily_chain_task",
        "schedule": crontab(hour=23, minute=59),
    },
}


        # "schedule": crontab(minute="*")
        #"schedule": crontab(hour=23, minute=59)