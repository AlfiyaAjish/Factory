import subprocess
import sys


def start_celery_beat():
    print("Starting Celery Beat...")
    subprocess.Popen([
        sys.executable, "-m", "celery",
        "-A", "scripts.handler.celery.periodic_tasks",
        "beat",
        "--loglevel=info"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
