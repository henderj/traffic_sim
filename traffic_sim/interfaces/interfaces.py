from pygame import Surface
from typing import TypeVar, Generic


T = TypeVar("T")


class PoolInterface(Generic[T]):
    def spawn(self) -> T:
        pass

    def despawn(self, obj: T):
        pass
