from pygame import Surface
from typing import TypeVar, Generic


class DrawableInterface:
    def draw(self, screen: Surface):
        pass


class TickableInterface:
    def tick(self, dt: int):
        pass


T = TypeVar("T")


class PoolInterface(Generic[T]):
    def spawn(self) -> T:
        pass

    def despawn(self, obj: T):
        pass
