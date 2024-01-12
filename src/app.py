from datetime import timedelta

import uvicorn
from celery import Celery
from fastapi import FastAPI
from redis import Redis

import api
import models
from db import engine
from settings import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Foxhole Events API")
app.include_router(api.router)

celery = Celery(
    __name__,
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)
cache = Redis(
    host=settings.cache_redis_host,
    port=settings.cache_redis_port,
    db=settings.cache_redis_db,
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
    uvicorn.run("app:app", reload=True)
