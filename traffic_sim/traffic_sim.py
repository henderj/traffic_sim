from typing import List
from dataclasses import dataclass


@dataclass
class SimData:
    nav_network: dict  # node tree or something
    entities: dict  # array of entities (growable, active/inactive entities)
    tiles: List[List[int]]  # 2d array of tiles, will almost never change
    meta_data: dict  # some game properties (speed, size, etc.), will almost never change


# entities = {
#     1: {
#         "active": True,
#         "current_node": 0,
#         "next_node": 1,
#         "progress_to_next_node": 0.34,
#         "target_node": 3,
#         "path": [1, 2, 0],
#         "speed": 1,
#     }
# }
# nav_network = {
#     0: {"pos": (3, 0), "neighbors": [2]},
#     1: {"pos": (0, 3), "neighbors": [2]},
#     2: {"pos": (3, 3), "neighbors": [0, 1, 3, 4]},
#     3: {"pos": (6, 3), "neighbors": [2]},
#     4: {"pos": (3, 6), "neighbors": [2]},
# }


class TrafficSim:
    @staticmethod
    def tick(data: SimData) -> SimData:
        nav_network = data.nav_network
        entities = data.entities
        tiles = data.tiles
        meta_data = data.meta_data
        return SimData(nav_network, entities, tiles, meta_data)
