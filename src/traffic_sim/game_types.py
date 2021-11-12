from typing import TypeVar, Protocol, List
from collections import namedtuple

Location = TypeVar("Location")


class Graph(Protocol):
    def neighbors(self, id: Location) -> List[Location]:
        pass


Point = namedtuple("Point", ["x", "y"])
