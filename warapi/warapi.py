# import numpy as np
# import requests
#
#
# def get_regions():
#     r = requests.get(
#         "https://war-service-live.foxholeservices.com/api/worldconquest/maps"
#     )
#     return r.json()
#
#
# def get_stockpiles_for_region(region):
#     static = requests.get(
#         f"https://war-service-live.foxholeservices.com/api/worldconquest/maps/{region}/static"
#     )
#     map_text_items = static.json()["mapTextItems"]
#     coordinates_major = np.array(
#         list((d["x"], d["y"]) for d in map_text_items if d["mapMarkerType"] == "Major")
#     )
#     dynamic = requests.get(
#         f"https://war-service-live.foxholeservices.com/api/worldconquest/maps/{region}/dynamic/public"
#     )
#     coordinates_stockpiles = list()
#     for map_item in dynamic.json()["mapItems"]:
#         if map_item["iconType"] in [33, 52]:
#             stock_location = np.array((map_item["x"], map_item["y"]))
#             distances = np.linalg.norm(coordinates_major - stock_location, axis=1)
#             min_index = np.argmin(distances)
#             coordinates_stockpiles.append(tuple(coordinates_major[min_index]))
#     return [
#         item["text"]
#         for item in map_text_items
#         if item["x"] in [x[0] for x in coordinates_stockpiles]
#         and item["y"] in [y[1] for y in coordinates_stockpiles]
#     ]
