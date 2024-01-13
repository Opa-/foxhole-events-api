import enum
import uuid
from datetime import datetime

from sqlalchemy import Column, UUID, Integer, Enum
from sqlmodel import SQLModel, Field


class Faction(str, enum.Enum):
    none = "NONE"
    wardens = "WARDENS"
    colonials = "COLONIALS"


class War(SQLModel):
    id: str = Column(UUID, primary_key=True, default=uuid.uuid4)
    number: int = Column(Integer)
    winner: str = Column(Enum(Faction))
    started_at: datetime
    ended_at: datetime
    resistance_started_at: datetime
    required_victory_towns: int = Column(Integer, default=32)


class Region(SQLModel):
    id: str = Field(default=None, primary_key=True)
    name: str
    # q,r,s coordinates as in https://www.redblobgames.com/grids/hexagons/#coordinates-cube
    q: int
    r: int
    s: int
