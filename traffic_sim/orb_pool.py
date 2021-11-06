import pygame
from interfaces.interfaces import DrawableInterface, TickableInterface, PoolInterface
from orb import Orb
from pygame import Surface, Vector2
from typing import List


class OrbPool(DrawableInterface, TickableInterface, PoolInterface[Orb]):
    active_orbs: List[Orb] = []
    pool: List[Orb] = []
    starting_pos = Vector2(x=500, y=250)
    spawn_rate = 500
    last_spawn_tick = 0

    def spawn(self) -> Orb:
        if len(self.pool) <= 0:
            self.grow_pool(5)
        orb = self.pool.pop()
        orb.init(self.starting_pos, 10, self)
        orb.set_target(Vector2(x=200, y=250))
        self.active_orbs.append(orb)
        return orb

    def despawn(self, obj: Orb):
        self.active_orbs.remove(obj)
        self.pool.append(obj)

    def grow_pool(self, amount):
        for _ in range(amount):
            self.pool.append(Orb())

    def tick(self, dt):
        current_tick = pygame.time.get_ticks()
        if (
            # len(self.active_orbs) <= 0
            current_tick - self.last_spawn_tick
            >= self.spawn_rate
        ):
            self.last_spawn_tick = current_tick
            self.spawn()
        for o in self.active_orbs:
            o.tick(dt)

    def draw(self, screen: Surface):
        for o in self.active_orbs:
            o.draw(screen)
