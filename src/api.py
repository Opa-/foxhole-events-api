from uuid import UUID

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import crud
import schemas
from db import SessionLocal

router = APIRouter(tags=["War"])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/wars/", response_model=schemas.War)
def create_war(war: schemas.War, db: Session = Depends(get_db)):
    try:
        return crud.create_war(db, war)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="War already exists")


@router.get("/wars/", response_model=list[schemas.War])
def read_wars(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    wars = crud.get_wars(db, skip=skip, limit=limit)
    return wars


@router.get("/wars/{war_id}", response_model=schemas.War)
def read_war(war_id: UUID, db: Session = Depends(get_db)):
    db_war = crud.get_war(db, war_id)
    if db_war is None:
        raise HTTPException(status_code=404, detail="War not found")
    return db_war
