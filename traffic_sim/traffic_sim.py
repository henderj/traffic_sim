from typing import List
from dataclasses import dataclass
import astar


@dataclass
class SimData:
    nav_network: List[dict]  # node tree or something
    entities: List[dict]  # array of entities (growable, active/inactive entities)
    tiles: List[List[int]]  # 2d array of tiles, will almost never change
    meta_data: dict  # some game properties (speed, size, etc.), will almost never change


# entities = [
#     {
#         "active": True,
#         "current_node_index": 0,
#         "next_node_index": 1,
#         "progress_to_next_node": 0.34,
#         "target_node": 0,
#         "path": [1, 2, 0],
#         "speed": 1,
#     }
# ]
# nav_network = [
#     {"pos": (3, 0), "neighbors": [2]},
#     {"pos": (0, 3), "neighbors": [2]},
#     {"pos": (3, 3), "neighbors": [0, 1, 3, 4]},
#     {"pos": (6, 3), "neighbors": [2]},
#     {"pos": (3, 6), "neighbors": [2]},
# ]


def findPath(start, end, nav_network: dict) -> List[int]:
    def neighbors(node):
        node["neighbors"]

    def distance(node1, node2):
        (x1, y1) = node1["pos"]
        (x2, y2) = node2["pos"]
        return abs(x1 - x2) + abs(y1 - y2)

    return astar.find_path(start, end, neighbors, False, distance, distance)


def updateEntities(data: SimData, deltaTime: int) -> dict:
    entities = data.entities
    for e_data in entities:
        if not e_data["active"]:
            continue
        path = e_data["path"]
        progress = e_data["progress_to_next_node"]
        current_node_index = e_data["current_node_index"]
        next_node_index = e_data["next_node_index"]
        target_node = e_data["target_node"]
        speed = e_data["speed"]

        if len(path) <= 0:
            nav = data.nav_network
            start = nav[0]
            end = nav[1]
            path = findPath(start, end, nav)

        if progress >= 1:
            current_node_index += 1
            next_node_index += 1
            progress = 0

        progress += speed * (deltaTime / 1000)

        e_data["path"] = path
        e_data["progress_to_next_node"] = progress
        e_data["current_node_index"] = current_node_index
        e_data["next_node_index"] = next_node_index
    return entities


class TrafficSim:
    @staticmethod
    def tick(data: SimData, delta_time: int) -> SimData:
        nav_network = data.nav_network
        entities = updateEntities(data, delta_time)
        tiles = data.tiles
        meta_data = data.meta_data

        return SimData(nav_network, entities, tiles, meta_data)
