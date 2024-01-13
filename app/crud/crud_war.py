from uuid import UUID

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import models
from schemas.war import War, BaseWar


def get_war(db: Session, war_id: UUID):
    return db.query(models.War).filter(models.War.id == war_id).first()


def get_wars(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.War).offset(skip).limit(limit).all()


def create_war(db: Session, war: War):
    db_war = models.War(
        id=war.id,
        number=war.number,
        winner=war.winner,
        started_at=war.started_at,
        ended_at=war.ended_at,
        resistance_started_at=war.resistance_started_at,
        required_victory_towns=war.required_victory_towns,
    )
    db.add(db_war)
    db.commit()
    return db_war


def update_war(db: Session, war_id, war: BaseWar):
    db_war = db.query(models.War).filter(models.War.id == war_id)
    if not db_war.first():
        raise HTTPException(status_code=404, detail="War not found")
    db_war = db_war.first()
    obj_data = jsonable_encoder(db_war)
    update_data = war.model_dump(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_war, field, update_data[field])
    db.add(db_war)
    db.commit()
    db.refresh(db_war)
    return db_war
