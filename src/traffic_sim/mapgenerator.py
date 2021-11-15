from typing import List, Iterator, Tuple
from .pathfinding import Point, PointGraph
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
sand = (1, 2)
ud = (0, 0)
lr = (0, 1)
udlr = (9, 0)
d = (8, 2)
u = (9, 2)
r = (8, 3)
l = (9, 3)
dr = (1, 0)
dl = (2, 0)
ur = (1, 1)
ul = (2, 1)
udr = (4, 2)
udl = (5, 2)
ulr = (4, 3)
dlr = (5, 3)

bitmask = [sand, u, l, ul, r, ur, lr, ulr, d, ud, dl, udl, dr, udr, dlr, udlr]


def northCheck(point: Point, graph: PointGraph):
    if point in graph.edges:
        neighbors = graph.neighbors(point)
        for n in neighbors:
            (x, y) = n
            if x == point.x and y < point.y:
                return True
        return False

    for node in graph.edges:
        (x, y) = node
        if x == point.x and y < point.y and southCheck(node, graph):
            for n in graph.neighbors(node):
                (nx, ny) = n
                if nx == point.x and ny > point.y:
                    return True
    return False


def eastCheck(point: Point, graph: PointGraph):
    if point in graph.edges:
        neighbors = graph.neighbors(point)
        for n in neighbors:
            (x, y) = n
            if x > point.x and y == point.y:
                return True
        return False

    for node in graph.edges:
        (x, y) = node
        if x > point.x and y == point.y and westCheck(node, graph):
            for n in graph.neighbors(node):
                (nx, ny) = n
                if nx < point.x and ny == point.y:
                    return True
    return False


def southCheck(point: Point, graph: PointGraph):
    if point in graph.edges:
        neighbors = graph.neighbors(point)
        for n in neighbors:
            (x, y) = n
            if x == point.x and y > point.y:
                return True
        return False

    for node in graph.edges:
        (x, y) = node
        if x == point.x and y > point.y and northCheck(node, graph):
            for n in graph.neighbors(node):
                (nx, ny) = n
                if nx == point.x and ny < point.y:
                    return True
    return False


def westCheck(point: Point, graph: PointGraph):
    if point in graph.edges:
        neighbors = graph.neighbors(point)
        for n in neighbors:
            (x, y) = n
            if x < point.x and y == point.y:
                return True
        return False

    for node in graph.edges:
        (x, y) = node
        if x < point.x and y == point.y and eastCheck(node, graph):
            for n in graph.neighbors(node):
                (nx, ny) = n
                if nx > point.x and ny == point.y:
                    return True
    return False


def getBitmaskValue(point: Point, graph: PointGraph):
    return (
        1 * northCheck(point, graph)
        + 2 * westCheck(point, graph)
        + 4 * eastCheck(point, graph)
        + 8 * southCheck(point, graph)
    )


def generateFromGraph(graph: PointGraph):
    pass


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
                sprites_row.append(udlr)
                continue
            if neighbors.right == 1 and neighbors.left == 1:
                sprites_row.append(lr)
                continue
            if neighbors.up == 1 and neighbors.down == 1:
                sprites_row.append(ud)
                continue
            if neighbors.up == 1 and neighbors.right == 1:
                sprites_row.append(ur)
                continue
            if neighbors.up == 1 and neighbors.left == 1:
                sprites_row.append(ul)
                continue
            if neighbors.down == 1 and neighbors.right == 1:
                sprites_row.append(dr)
                continue
            if neighbors.down == 1 and neighbors.left == 1:
                sprites_row.append(dl)
                continue
            if neighbors.down == 1:
                sprites_row.append(d)
                continue
            if neighbors.up == 1:
                sprites_row.append(u)
                continue
            if neighbors.right == 1:
                sprites_row.append(r)
                continue
            if neighbors.left == 1:
                sprites_row.append(l)
                continue
    return sprites_row
