from fastapi import APIRouter

from api.v1.endpoints import war, region

api_router = APIRouter()
api_router.include_router(war.router, prefix="/wars", tags=["wars"])
api_router.include_router(region.router, prefix="/regions", tags=["regions"])
