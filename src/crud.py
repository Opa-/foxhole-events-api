from uuid import UUID

from sqlalchemy.orm import Session

import models
import schemas


def get_war(db: Session, war_id: UUID):
    return db.query(models.War).filter(models.War.id == war_id).first()


def get_wars(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.War).offset(skip).limit(limit).all()


def create_war(db: Session, war: schemas.War):
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
    # db.refresh(db_war)
    return db_war


def update_war(db: Session, war_id, war: schemas.War):
    db_war = db.query(models.War).filter(models.War.id == war_id)
    if not db_war.first():
        raise HttNotFoundError
    db_war
