from datetime import timedelta


class AppConstants:
    ALERT_TEMP_THRESHOLD = 80.0
    BASE_URL = "http://localhost:8009"

    WORKER_CONCURRENCY = 10
    TASK_DEFAULT_RETRY_DELAY = 10
    TASK_MAX_RETRIES = 3
    RESULT_EXPIRES = timedelta(hours=24)
    TASK_ACKS_LATE = True
    WORKER_MAX_TASKS_PER_CHILD = 100
    RESULT_COMPRESSION = 'gzip'
