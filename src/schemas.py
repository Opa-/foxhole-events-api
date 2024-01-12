import enum
import uuid
from datetime import datetime

from pydantic import BaseModel


class FactionEnum(str, enum.Enum):
    none = "NONE"
    wardens = "WARDENS"
    colonials = "COLONIALS"


class War(BaseModel):
    id: uuid.UUID
    number: int = 1
    winner: FactionEnum
    started_at: datetime
    ended_at: datetime
    resistance_started_at: datetime
    required_victory_towns: int = 32

    class Config:
        use_enum_values = True
        from_attributes = True
