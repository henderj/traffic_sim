from interfaces.interfaces import DrawableInterface, TickableInterface, PoolInterface
import vector
from random import randint
from vector import VectorObject2D
import pygame
from helper_methods import normalize


class Orb(DrawableInterface, TickableInterface):
    COLOR = (255, 255, 255)
    TARGET_COLOR = (50, 168, 82)

    pos = vector.obj(x=0, y=0)
    velocity = vector.obj(x=0, y=0)
    mass = 1
    top_speed = 10
    net_force = vector.obj(x=0, y=0)

    size = vector.obj(x=10, y=10)
    target = vector.obj(x=200, y=200)
    min_speed = 0.1
    max_force = 1
    drag = 0.1

    pool: PoolInterface

    def init(self, pos: vector.VectorObject2D, size: int, pool: PoolInterface):
        self.pos = pos
        self.size = vector.obj(x=size, y=size)
        self.pool = pool
        zero = vector.obj(x=0, y=0)
        self.velocity = zero
        self.net_force = zero

    def set_target(self, target: VectorObject2D = None):
        if target == None:
            target = vector.obj(x=randint(0, 700), y=randint(0, 500))
        self.target = target

    def is_at_target(self) -> bool:
        return abs(self.pos.subtract(self.target)) < self.top_speed

    def add_force(self, force: VectorObject2D):
        self.net_force = self.net_force + force

    def apply_forces(self):
        acc = self.net_force.scale(self.mass)
        self.velocity = self.velocity.add(acc)
        if abs(self.velocity) > self.top_speed:
            self.velocity = normalize(self.velocity).scale(self.top_speed)
        self.pos = self.pos.add(self.velocity)

    def tick(self):
        if self.is_at_target():
            self.pool.despawn(self)
            return None
        self.net_force = vector.obj(x=0, y=0)
        diff = self.target - self.pos
        dist = abs(diff)
        G = 30
        force_mag = G * self.mass / (dist * dist)
        force = normalize(diff).scale(force_mag)
        if abs(force) < self.min_speed:
            force = normalize(force).scale(self.min_speed)
        drag = self.velocity.scale(-(G * self.mass / (dist * dist)))
        self.add_force(force)
        self.add_force(drag)
        self.apply_forces()

    def draw(self, screen: pygame.Surface):
        self.draw_circle(self.pos, self.size, self.COLOR, screen)
        self.draw_circle(self.target, self.size.scale(0.5), self.TARGET_COLOR, screen)

    def draw_circle(self, pos: VectorObject2D, size: VectorObject2D, color, screen):
        draw_pos = pos - (size / 2)
        pygame.draw.ellipse(screen, color, [draw_pos.x, draw_pos.y, size.x, size.y])
