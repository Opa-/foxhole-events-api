from flask_openapi3 import APIBlueprint

from stockpile.models import CreateStockpileBody

api_stockpile = APIBlueprint("stockpile", __name__, url_prefix="/api")


@api_stockpile.get("/stockpile")
def get_stockpile():
    return []


@api_stockpile.post("/stockpile")
def create_stockpile(body: CreateStockpileBody):
    return {"message": "success"}
