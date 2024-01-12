import enum
import uuid

from sqlalchemy import Column, UUID, Integer, Enum, DateTime

from db import Base


class Faction(str, enum.Enum):
    none = "NONE"
    wardens = "WARDENS"
    colonials = "COLONIALS"


class War(Base):
    __tablename__ = "wars"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    number = Column(Integer, unique=True)
    winner = Column(Enum(Faction))
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    resistance_started_at = Column(DateTime, nullable=True)
    required_victory_towns = Column(Integer, default=32)
