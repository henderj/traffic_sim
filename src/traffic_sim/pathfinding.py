from collections import namedtuple
from typing import Iterator, List, Protocol, TypeVar, Dict
import math, astar

Location = TypeVar("Location")
Point = namedtuple("Point", ["x", "y"])


class Graph(Protocol):
    def neighbors(self, id: Location) -> List[Location]:
        pass


class PointGraph:
    def __init__(self, edges: Dict[Point, List[Point]] = {}) -> None:
        self.edges: Dict[Point, List[Point]] = {}
        for e in edges:
            neighbors = []
            for n in edges[e]:
                neighbors.append(Point(*n))
            point = Point(*e)
            self.edges[point] = neighbors

    def neighbors(self, pos: Point) -> List[Point]:
        return self.edges[pos]

    def dist(self, pos1: Point, pos2: Point) -> float:
        (x1, y1) = pos1
        (x2, y2) = pos2
        return abs(x1 - x2) + abs(y1 - y2)

    def addPoint(self, point: Point, neighbors: List[Point]):
        newEdge = {point: neighbors}
        newEdges = {**self.edges, **newEdge}
        return PointGraph(newEdges)


def findPath(start: Point, end: Point, graph: PointGraph) -> List[int]:
    return list(
        astar.find_path(
            start=start,
            goal=end,
            neighbors_fnct=graph.neighbors,
            heuristic_cost_estimate_fnct=graph.dist,
            distance_between_fnct=graph.dist,
        )
    )


def findClosestPosInGraph(pos: Point, graph: PointGraph) -> Point:
    """TODO: sort dict keys and return optional number of closest points"""
    closest = Point(math.inf, math.inf)
    closestDist = math.inf
    for edge in graph.edges:
        dist = graph.dist(pos, edge)
        if dist < closestDist:
            closest = edge
            closestDist = dist
    return closest


def findEntityPath(pos: Point, end: Point, graph: PointGraph) -> List[int]:
    if pos in graph.edges:
        return findPath(pos, end, graph)

    closest = findClosestPosInGraph(pos, graph)
    return findPath(pos, end, graph.addPoint(pos, [closest]))
