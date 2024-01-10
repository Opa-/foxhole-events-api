from datetime import timedelta

import uvicorn
from celery import Celery
from fastapi import FastAPI
from redis import Redis

from settings import settings

app = FastAPI()
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


@app.get("/")
def home():
    return {"Hello": "World"}


# def celery_init_app(flask_app: Flask) -> Celery:
#     class FlaskTask(Task):
#         def __call__(self, *args: object, **kwargs: object) -> object:
#             with flask_app.app_context():
#                 return self.run(*args, **kwargs)
#
#     celery_app = Celery(flask_app.name, task_cls=FlaskTask)
#     celery_app.config_from_object(flask_app.config["CELERY"])
#     celery_app.set_default()
#     flask_app.extensions["celery"] = celery_app
#     return celery_app
#
#
# app.config.from_mapping(
#     CELERY=dict(
#         broker_url="redis://localhost",
#         worker_concurrency=20,
#         result_backend="redis://localhost",
#         task_ignore_result=True,
#         beat_schedule={
#             "refresh-warapi-every-60-seconds": {
#                 "task": "warapi_refresh_war",
#                 "schedule": timedelta(seconds=60),
#             },
#             # "warpiapi-every-3-seconds": {
#             #     "task": "warapi_refresh_maps",
#             #     "schedule": timedelta(seconds=3),
#             # },
#         },
#     ),
# )
# celery = celery_init_app(app)
#
# app.config.from_mapping(
#     {
#         "CACHE_TYPE": "RedisCache",
#         "CACHE_DEFAULT_TIMEOUT": 300,
#         "CACHE_KEY_PREFIX": "warapi_cache_",
#         "CACHE_REDIS_URL": "redis://localhost:6379/2",
#     }
# )
# cache = Cache(app)


if __name__ == "__main__":
    uvicorn.run("app:app")
