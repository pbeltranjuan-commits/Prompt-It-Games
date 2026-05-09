from celery import Celery
from app.config import get_settings

settings = get_settings()
celery_app = Celery(
    "boardgames",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Madrid",
    enable_utc=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_default_retry_delay=60,
    task_max_retries=3
)
