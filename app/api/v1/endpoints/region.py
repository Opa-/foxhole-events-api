from fastapi import APIRouter

import crud
from api.deps import SessionDep
from schemas.region import Region

router = APIRouter()


@router.get("/", response_model=list[Region])
def read_regions(db: SessionDep):
    return crud.read_regions(db)


@router.post("/", response_model=Region)
def create_region(db: SessionDep, region: Region):
    return crud.create_region(db, region)
