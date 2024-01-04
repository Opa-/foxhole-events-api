import logging

from celery import shared_task, signals, group
from warapi_client.api.maps_api import MapsApi
from warapi_client.api.war_api import WarApi
from warapi_client.rest import ApiException

from warapi import warapi


@shared_task(ignore_result=False)
def init_database_towns():
    stockpiles = []
    for region in warapi.get_regions():
        stockpiles += warapi.get_stockpiles_for_region(region)
    return stockpiles


@shared_task(name="warapi_refresh_war")
def warapi_refresh_war():
    api = WarApi()
    war = api.get_war()
    return war


@shared_task(name="warapi_refresh_map_war_report")
def warapi_refresh_map_war_report(map_name: str):
    from app import cache

    if_none_match = cache.get(f"etag_war_report_{map_name}") or ""
    api = MapsApi()
    try:
        war_report, http_status, http_info = api.get_war_report_with_http_info(
            map_name, if_none_match=if_none_match
        )
        logging.log(logging.INFO, f"{map_name} {http_status}, {http_info}")
        if "ETag" in http_info.keys():
            cache.set(f"etag_war_report_{map_name}", http_info["ETag"])
        return war_report
    except ApiException as e:
        if e.status == 304:
            return
        raise


@shared_task(name="warapi_refresh_map_static")
def warapi_refresh_map_static(map_name: str):
    from app import cache

    if_none_match = cache.get(f"etag_map_static_{map_name}") or ""
    api = MapsApi()
    try:
        map_static, http_status, http_info = api.get_map_static_with_http_info(
            map_name, if_none_match=if_none_match
        )
        logging.log(logging.INFO, f"{map_name} {http_status}, {http_info}")
        if "ETag" in http_info.keys():
            cache.set(f"etag_map_static_{map_name}", http_info["ETag"])
        return map_static
    except ApiException as e:
        if e.status == 304:
            return
        raise


@shared_task(name="warapi_refresh_map_dynamic")
def warapi_refresh_map_dynamic(map_name: str):
    from app import cache

    if_none_match = cache.get(f"etag_map_dynamic_{map_name}") or ""
    api = MapsApi()
    try:
        map_dynamic, http_status, http_info = api.get_map_dynamic_with_http_info(
            map_name, if_none_match=if_none_match
        )
        logging.log(logging.INFO, f"{map_name} {http_status}, {http_info}")
        if "ETag" in http_info.keys():
            cache.set(f"etag_map_dynamic_{map_name}", http_info["ETag"])
        return map_dynamic
    except ApiException as e:
        if e.status == 304:
            return
        raise


@shared_task(name="warapi_refresh_map")
def warapi_refresh_map(map_name: str):
    job = group(
        [
            warapi_refresh_map_war_report.s(map_name),
            warapi_refresh_map_static.s(map_name),
            warapi_refresh_map_dynamic.s(map_name),
        ]
    )
    job.apply_async()


@shared_task(name="warapi_refresh_maps")
def warapi_refresh_maps():
    from app import cache

    maps = cache.get("maps")
    tasks = []
    for map_name in maps:
        logging.log(logging.INFO, f"{map_name}")
        tasks.append(warapi_refresh_map.s(map_name))
    job = group(tasks)
    result = job.apply_async()
    return result.successful()


@signals.worker_ready.connect
def warapi_init_maps(sender, **kwargs):
    from app import cache

    api = MapsApi()
    maps = api.get_maps()
    logging.log(logging.INFO, f'Fethed maps: {", ".join(maps)}')
    cache.set("maps", maps)
