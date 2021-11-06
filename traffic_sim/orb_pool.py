import pygame
from interfaces.interfaces import DrawableInterface, TickableInterface, PoolInterface
import vector
from orb import Orb
from pygame import Surface


class OrbPool(DrawableInterface, TickableInterface, PoolInterface[Orb]):
    active_orbs: list[Orb] = []
    pool: list[Orb] = []
    starting_pos = vector.obj(x=500, y=250)
    spawn_rate = 500
    last_spawn_tick = 0

    def spawn(self) -> Orb:
        if len(self.pool) <= 0:
            self.grow_pool(5)
        orb = self.pool.pop()
        orb.init(self.starting_pos, 10, self)
        orb.set_target()
        self.active_orbs.append(orb)
        return orb

    def despawn(self, obj: Orb):
        self.active_orbs.remove(obj)
        self.pool.append(obj)

    def grow_pool(self, amount):
        for _ in range(amount):
            self.pool.append(Orb())

    def tick(self):
        current_tick = pygame.time.get_ticks()
        if current_tick - self.last_spawn_tick >= self.spawn_rate:
            self.last_spawn_tick = current_tick
            self.spawn()
        for o in self.active_orbs:
            o.tick()

    def draw(self, screen: Surface):
        for o in self.active_orbs:
            o.draw(screen)
