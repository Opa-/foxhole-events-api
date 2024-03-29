from typing import Generator, Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from db.engine import engine


def get_db() -> Generator:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
