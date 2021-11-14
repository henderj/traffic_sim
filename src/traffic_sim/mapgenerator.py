from typing import List, Iterator, Tuple
from .pathfinding import Point
from dataclasses import dataclass

sampleIds = [
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
]


@dataclass
class Neighbors:
    up: int
    down: int
    right: int
    left: int


class TileGraph:
    def __init__(self, width: int, height: int, ids: List[List[int]]) -> None:
        self.width = width
        self.height = height
        self.ids = ids

    def in_bounds(self, pos: Point) -> bool:
        (x, y) = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def neighbors(self, pos: Point) -> Iterator[Point]:
        (x, y) = pos
        neighbors = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]  # E W N S
        results = filter(self.in_bounds, neighbors)
        return results

    def neighborObject(self, pos: Point) -> Neighbors:
        (x, y) = pos
        up = 0
        down = 0
        right = 0
        left = 0
        if self.in_bounds((x + 1, y)):
            right = self.getId((x + 1, y))
        if self.in_bounds((x - 1, y)):
            left = self.getId((x - 1, y))
        if self.in_bounds((x, y - 1)):
            up = self.getId((x, y - 1))
        if self.in_bounds((x, y + 1)):
            down = self.getId((x, y + 1))
        return Neighbors(up, down, right, left)

    def getId(self, pos: Point) -> int:
        (x, y) = pos
        return self.ids[y][x]


class TileMap:
    def __init__(self, spriteIds: List[List[Tuple]]) -> None:
        self.spriteIds = spriteIds


def getGraphFrom2DList(list2D: List[List[int]]) -> TileGraph:
    graph = TileGraph(len(list2D[0]), len(list2D))
    return graph


def pointToListId(ids: List[List[int]], pos: Point) -> int:
    return ids[pos.y][pos.x]


grass = (0, 2)
down = (0, 0)
right = (0, 1)
cross = (9, 0)
uend = (8, 2)
dend = (9, 2)
lend = (8, 3)
rend = (9, 3)
urturn = (1, 0)
ulturn = (2, 0)
drturn = (1, 1)
dlturn = (2, 1)


def generate(ids: List[List[int]]):
    width = len(ids[0])
    height = len(ids)
    graph = TileGraph(width, height, ids)
    spriteIds = []
    for y, row in enumerate(ids):
        spriterow = get_row_spriteids(graph, y, row)
        spriteIds.append(spriterow)
    return TileMap(spriteIds)


def get_row_spriteids(graph: TileGraph, y: int, ids_row: List[int]):
    sprites_row = []
    for x, id in enumerate(ids_row):
        point = Point(x, y)
        if id == 0:
            sprites_row.append(grass)
            continue
        if id == 1:
            neighbors = graph.neighborObject(point)
            if (
                neighbors.up == 1
                and neighbors.down == 1
                and neighbors.right == 1
                and neighbors.left == 1
            ):
                sprites_row.append(cross)
                continue
            if neighbors.right == 1 and neighbors.left == 1:
                sprites_row.append(right)
                continue
            if neighbors.up == 1 and neighbors.down == 1:
                sprites_row.append(down)
                continue
            if neighbors.up == 1 and neighbors.right == 1:
                sprites_row.append(drturn)
                continue
            if neighbors.up == 1 and neighbors.left == 1:
                sprites_row.append(dlturn)
                continue
            if neighbors.down == 1 and neighbors.right == 1:
                sprites_row.append(urturn)
                continue
            if neighbors.down == 1 and neighbors.left == 1:
                sprites_row.append(ulturn)
                continue
            if neighbors.down == 1:
                sprites_row.append(uend)
                continue
            if neighbors.up == 1:
                sprites_row.append(dend)
                continue
            if neighbors.right == 1:
                sprites_row.append(lend)
                continue
            if neighbors.left == 1:
                sprites_row.append(rend)
                continue
    return sprites_row
