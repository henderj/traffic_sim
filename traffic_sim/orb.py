from interfaces.interfaces import DrawableInterface, TickableInterface, PoolInterface
import vector
from random import randint
from vector import VectorObject2D
import pygame
import pytweening as tween


class Orb(DrawableInterface, TickableInterface):
    COLOR = (255, 255, 255)
    TARGET_COLOR = (50, 168, 82)

    starting_pos = vector.obj(x=0, y=0)
    pos = vector.obj(x=0, y=0)
    size = vector.obj(x=10, y=10)
    target = vector.obj(x=200, y=200)
    progress = 0
    speed = 2

    target_threshold = 1

    pool: PoolInterface

    def init(self, pos: vector.VectorObject2D, size: int, pool: PoolInterface):
        self.starting_pos = pos
        self.pos = self.starting_pos
        self.progress = 0
        self.size = vector.obj(x=size, y=size)
        self.pool = pool

    def set_target(self, target: VectorObject2D = None):
        if target == None:
            target = vector.obj(x=randint(0, 700), y=randint(0, 500))
        self.target = target

    def is_at_target(self) -> bool:
        return self.progress >= self.speed

    def tick(self, dt: int):
        self.progress += dt / 1000.0
        if self.is_at_target():
            self.pool.despawn(self)
            return None
        tweened_progress = tween.easeInOutSine(self.progress / self.speed)
        diff = self.target - self.starting_pos
        self.pos = diff.scale(tweened_progress) + self.starting_pos

    def draw(self, screen: pygame.Surface):
        self.draw_circle(self.pos, self.size, self.COLOR, screen)
        self.draw_circle(self.target, self.size.scale(0.5), self.TARGET_COLOR, screen)

    def draw_circle(self, pos: VectorObject2D, size: VectorObject2D, color, screen):
        draw_pos = pos - (size / 2)
        pygame.draw.ellipse(screen, color, [draw_pos.x, draw_pos.y, size.x, size.y])
