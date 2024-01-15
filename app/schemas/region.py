from pydantic import BaseModel


class Region(BaseModel):
    id: str
    name: str
    q: int
    r: int
    s: int
