from pydantic import BaseModel, Field


class CeleryTaskResultPath(BaseModel):
    task_id: str = Field(..., description="The id of the celery task")
