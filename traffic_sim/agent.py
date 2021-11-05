from kivy.uix.widget import Widget
from kivy.vector import Vector
from random import randint


class Agent(Widget):
    def initialize(self, pos: Vector) -> None:
        self.pos = pos

    def tick(self, dt: float) -> None:
        self.random_walk()
        # pass

    def random_walk(self) -> None:
        self.pos = Vector(*self.pos) + Vector(1, 0).rotate(randint(0, 359))
