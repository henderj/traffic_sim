from dataclasses import dataclass
from typing import Dict, List
from .game_types import Point

import math
import astar


class SimpleGraph:
    def __init__(self, edges: Dict[Point, List[Point]] = {}) -> None:
        self.edges = edges

    def neighbors(self, pos: Point) -> List[Point]:
        return self.edges[pos]

    def dist(self, pos1: Point, pos2: Point) -> float:
        (x1, y1) = pos1
        (x2, y2) = pos2
        return abs(x1 - x2) + abs(y1 - y2)


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
    nav_network: SimpleGraph  # node tree or something
    entities: List[Entity]  # array of entities (growable, active/inactive entities)
    tiles: List[List[int]]  # 2d array of tiles, will almost never change
    meta_data: dict  # some game properties (speed, size, etc.), will almost never change


def getInitialData():
    entities: List[Entity] = []
    entities.append(Entity(pos=Point(0, 3), active=True))

    nav_network = SimpleGraph()
    nav_network.edges = {
        Point(3, 0): [Point(3, 3)],
        Point(0, 3): [Point(3, 3)],
        Point(3, 3): [Point(3, 0), Point(0, 3), Point(6, 3), Point(3, 6)],
        Point(6, 3): [Point(3, 3)],
        Point(3, 6): [Point(3, 3)],
    }
    return SimData(nav_network, entities, [], {})


def findPath(start: Point, end: Point, nav_network: SimpleGraph) -> List[int]:
    return list(
        astar.find_path(
            start=start,
            goal=end,
            neighbors_fnct=nav_network.neighbors,
            heuristic_cost_estimate_fnct=nav_network.dist,
            distance_between_fnct=nav_network.dist,
        )
    )


def findEntityPath(pos: Point, end: Point, graph: SimpleGraph) -> List[int]:
    if pos in graph.edges:
        return findPath(pos, end, graph)

    closest = Point(math.inf, math.inf)
    closestDist = math.inf
    for edge in graph.edges:
        dist = graph.dist(pos, edge)
        if dist < closestDist:
            closest = edge
            closestDist = dist
    tempGraph = SimpleGraph(graph.edges)
    tempGraph.edges[pos] = [closest]
    return findPath(pos, end, tempGraph)


def updateEntities(data: SimData, deltaTime: int):
    def findPathCallback(pos, end):
        return findEntityPath(pos, end, data.nav_network)

    for e in data.entities:
        e.update(findPathCallback, deltaTime)
    return data.entities


class TrafficSim:
    @staticmethod
    def tick(data: SimData, delta_time: int) -> SimData:
        data.entities = updateEntities(data, delta_time)

        return data
