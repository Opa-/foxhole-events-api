from celery import Celery, Task
from flask import Flask
from flask_openapi3 import OpenAPI

from stockpile.api import api_stockpile
from towns.api import api_towns

app = OpenAPI(__name__)
app.register_api(api_stockpile)
app.register_api(api_towns)


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost",
        result_backend="redis://localhost",
        task_ignore_result=True,
    ),
)
celery_app = celery_init_app(app)

if __name__ == "__main__":
    app.run()
