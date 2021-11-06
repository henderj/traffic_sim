from interfaces.interfaces import DrawableInterface, TickableInterface, PoolInterface
import vector
from random import randint
from vector import VectorObject2D
import pygame


class Orb(DrawableInterface, TickableInterface):
    COLOR = (255, 255, 255)
    TARGET_COLOR = (50, 168, 82)

    pos = vector.obj(x=0, y=0)
    size = vector.obj(x=10, y=10)
    target = vector.obj(x=200, y=200)

    pool: PoolInterface

    def init(self, pos: vector.VectorObject2D, size: int, pool: PoolInterface):
        self.pos = pos
        self.size = vector.obj(x=size, y=size)
        self.pool = pool

    def set_target(self, target: VectorObject2D = None):
        if target == None:
            target = vector.obj(x=randint(0, 700), y=randint(0, 500))
        self.target = target

    def is_at_target(self) -> bool:
        return abs(self.pos.subtract(self.target)) < self.top_speed

    def tick(self):
        if self.is_at_target():
            self.pool.despawn(self)
            return None

    def draw(self, screen: pygame.Surface):
        self.draw_circle(self.pos, self.size, self.COLOR, screen)
        self.draw_circle(self.target, self.size.scale(0.5), self.TARGET_COLOR, screen)

    def draw_circle(self, pos: VectorObject2D, size: VectorObject2D, color, screen):
        draw_pos = pos - (size / 2)
        pygame.draw.ellipse(screen, color, [draw_pos.x, draw_pos.y, size.x, size.y])
