from typing import Optional

from pydantic import BaseModel


class Region(BaseModel):
    name: str
    x: Optional[int] = None
    y: Optional[int] = None
