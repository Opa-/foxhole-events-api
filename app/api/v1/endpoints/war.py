from uuid import UUID

from fastapi import HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError

import crud
from api.deps import SessionDep
from schemas.war import War, BaseWar

router = APIRouter(tags=["War"])


@router.post("/", response_model=War)
def create_war(db: SessionDep, war: War):
    try:
        return crud.create_war(db, war)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="War already exists")


@router.get("/", response_model=list[War])
def read_wars(db: SessionDep, skip: int = 0, limit: int = 100):
    wars = crud.get_wars(db, skip=skip, limit=limit)
    return wars


@router.get("/{war_id}", response_model=War)
def read_war(db: SessionDep, war_id: UUID):
    db_war = crud.get_war(db, war_id)
    if db_war is None:
        raise HTTPException(status_code=404, detail="War not found")
    return db_war


@router.put("/{war_id}", response_model=War)
def update_war(db: SessionDep, war_id: UUID, war: BaseWar):
    return crud.update_war(db, war_id, war)
