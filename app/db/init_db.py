import os.path

import yaml
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Region


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    path = os.path.join(os.path.dirname(__file__), "fixtures", "regions.yaml")
    with open(path, "r") as f:
        regions_raw = yaml.safe_load(f.read())
        regions = [
            Region(id=r["id"], name=r["name"], q=r["q"], r=r["r"], s=r["s"])
            for r in regions_raw["regions"]
        ]
        try:
            session.bulk_save_objects(regions)
            session.commit()
        except IntegrityError:
            session.rollback()
            # Create or update one by one
            for region in regions:
                region_db = session.get(Region, region.id)
                if region_db:
                    for key, value in region.model_dump(exclude_unset=True).items():
                        setattr(region_db, key, value)
                session.add(region_db)
                session.commit()
