from celery import shared_task

from towns import warapi


@shared_task(ignore_result=False)
def init_database_towns():
    stockpiles = []
    for region in warapi.get_regions():
        stockpiles += warapi.get_stockpiles_for_region(region)
    return stockpiles
