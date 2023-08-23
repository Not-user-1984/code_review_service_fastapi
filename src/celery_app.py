from celery import Celery
from config import Settings

calary = Celery(
    "tasks",
    broker=Settings.CELERY_BROKER_URL,
    backend=Settings.CELERY_RESULT_BACKEND,
    include=["src.tasks"]
)
