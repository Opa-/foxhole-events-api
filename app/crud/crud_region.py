from typing import Type

from sqlalchemy.orm import Session

import models
from schemas.region import Region


def read_regions(db: Session) -> list[Type[models.Region]]:
    return db.query(models.Region).all()


def create_region(db: Session, region: Region) -> models.Region:
    db_region = models.Region(name=region.name, x=region.x, y=region.y)
    db.add(db_region)
    db.commit()
    return db_region
