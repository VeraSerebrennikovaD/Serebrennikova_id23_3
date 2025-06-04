from pathlib import Path
from urllib.parse import quote_plus

from celery import Celery
from redislite import Redis

_DB_PATH = Path(__file__).resolve().parent.parent.parent / ".celery_redis.db"

redis_server = Redis(str(_DB_PATH))

socket_path = quote_plus(redis_server.socket_file)

redis_url = f"redis+socket:///{socket_path}?db=0"

celery_app = Celery(
    "app",
    broker=redis_url,
    backend=redis_url,
    include=["app.celery.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,
)
