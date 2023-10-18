from pydantic import BaseModel, Field


class CreateStockpileBody(BaseModel):
    discord_server_id: int = Field(
        42, description="The discord server of the stockpile"
    )
    region: str = Field(None, description="The region of the stockpile")
    town: str = Field(None, description="The town of the stockpile")
    name: str = Field(None, description="The name of the stockpile")
    code: str = Field(
        "123456", min_length=6, max_length=6, description="The code of the stockpile"
    )
