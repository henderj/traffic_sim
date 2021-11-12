from dataclasses import dataclass
from typing import Dict, List
from .pathfinding import findEntityPath, Point, PointGraph

import math
import astar


class Entity:
    active: bool
    path: List[Point]
    current_path_index: int
    progress_to_next_node: int
    target_node: Point
    speed: float
    pos: Point

    def __init__(
        self,
        speed=1,
        active=False,
        pos: Point = Point(0, 0),
        path: List[Point] = [],
        current_path_index=0,
        progress_to_next_node=0,
        target_node=None,
    ) -> None:
        self.speed = speed
        self.active = active
        self.pos = pos
        self.path = path
        self.current_path_index = current_path_index
        self.progress_to_next_node = progress_to_next_node
        self.target_node = target_node

    def hasPath(self):
        return len(self.path) > 0

    def tilePos(self):
        return Point(math.floor(self.pos.x), math.floor(self.pos.y))

    def nextPathPos(self):
        return self.path[self.current_path_index]

    def update(self, findPath, deltaTime: int):
        if not self.active:
            return

        if not self.hasPath():
            start = self.tilePos()
            end = Point(3, 0)
            self.path = findPath(start, end)

        if self.progress_to_next_node >= 1:
            self.current_path_index += 1
            self.progress_to_next_node = 0

        if self.current_path_index >= len(self.path):
            self.path = []
            self.current_path_index = 0
            return

        self.pos = self.path[self.current_path_index]

        self.progress_to_next_node += self.speed * (deltaTime / 1000)


@dataclass
class SimData:
    nav_network: PointGraph  # node tree or something
    entities: List[Entity]  # array of entities (growable, active/inactive entities)
    tiles: List[List[int]]  # 2d array of tiles, will almost never change
    meta_data: dict  # some game properties (speed, size, etc.), will almost never change


def getInitialData():
    entities: List[Entity] = []
    entities.append(Entity(pos=Point(0, 3), active=True))

    nav_network = PointGraph()
    nav_network.edges = {
        Point(3, 0): [Point(3, 3)],
        Point(0, 3): [Point(3, 3)],
        Point(3, 3): [Point(3, 0), Point(0, 3), Point(6, 3), Point(3, 6)],
        Point(6, 3): [Point(3, 3)],
        Point(3, 6): [Point(3, 3)],
    }
    return SimData(nav_network, entities, [], {})


def updateEntities(data: SimData, deltaTime: int):
    for e in data.entities:
        e.update(lambda pos, end: findEntityPath(pos, end, data.nav_network), deltaTime)
    return data.entities


class TrafficSim:
    @staticmethod
    def tick(data: SimData, delta_time: int) -> SimData:
        data.entities = updateEntities(data, delta_time)
        return data
