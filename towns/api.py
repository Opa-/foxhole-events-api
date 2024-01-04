from celery.result import AsyncResult
from flask_openapi3 import APIBlueprint

from towns.models import CeleryTaskResultPath
from warapi.tasks import init_database_towns

api_towns = APIBlueprint("towns", __name__, url_prefix="/api")


@api_towns.get("/towns")
def get_towns():
    return []


@api_towns.post("/towns/init")
def create_towns():
    result = init_database_towns.delay()
    return {"result_id": result.id}


@api_towns.get("/towns/init/<task_id>")
def get_init_towns_result(path: CeleryTaskResultPath):
    result = AsyncResult(path.task_id)
    return {
        "ready": result.ready(),
        "successful": result.successful(),
        "value": result.result if result.ready() else None,
    }
