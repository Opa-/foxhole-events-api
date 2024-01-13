from datetime import timedelta

import uvicorn
from celery import Celery
from fastapi import FastAPI
from redis import Redis

from api.v1.api import api_router
from core.config import settings

app = FastAPI(title="Foxhole Events API")
app.include_router(api_router, prefix=settings.API_V1_STR)

celery = Celery(
    __name__,
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)
cache = Redis(
    host=settings.CACHE_REDIS_HOST,
    port=settings.CACHE_REDIS_PORT,
    db=settings.CACHE_REDIS_DB,
    decode_responses=True,
)

celery.conf.update(
    task_serializer="json", result_serializer="json", accept_content=["json"]
)
celery.conf.beat_schedule = {
    "refresh-warapi-every-60-seconds": {
        "task": "warapi_refresh_war",
        "schedule": timedelta(seconds=60),
    },
    "warpiapi-every-3-seconds": {
        "task": "warapi_refresh_maps",
        "schedule": timedelta(seconds=10),
    },
}
celery.conf.timezone = "UTC"
celery.autodiscover_tasks(packages=["tasks"], force=True)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=settings.UVICORN_RELOAD)
