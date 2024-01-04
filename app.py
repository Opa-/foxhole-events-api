from datetime import timedelta

from celery import Celery, Task
from flask import Flask
from flask_caching import Cache
from flask_openapi3 import OpenAPI

from stockpile.api import api_stockpile
from towns.api import api_towns

app = OpenAPI(__name__)
app.register_api(api_stockpile)
app.register_api(api_towns)


def celery_init_app(flask_app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(flask_app.name, task_cls=FlaskTask)
    celery_app.config_from_object(flask_app.config["CELERY"])
    celery_app.set_default()
    flask_app.extensions["celery"] = celery_app
    return celery_app


app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost",
        worker_concurrency=20,
        result_backend="redis://localhost",
        task_ignore_result=True,
        beat_schedule={
            "refresh-warapi-every-60-seconds": {
                "task": "warapi_refresh_war",
                "schedule": timedelta(seconds=60),
            },
            "warpiapi-every-3-seconds": {
                "task": "warapi_refresh_maps",
                "schedule": timedelta(seconds=3),
            },
        },
    ),
)
celery = celery_init_app(app)

app.config.from_mapping(
    {
        "CACHE_TYPE": "RedisCache",
        "CACHE_DEFAULT_TIMEOUT": 300,
        "CACHE_KEY_PREFIX": "warapi_cache_",
        "CACHE_REDIS_URL": "redis://localhost:6379/2",
    }
)
cache = Cache(app)


if __name__ == "__main__":
    app.run()
