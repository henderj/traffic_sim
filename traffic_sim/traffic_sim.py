from math import radians
import pygame
from pygame import draw, Surface
from random import randint

from vector._backends.object_ import VectorObject2D
from interfaces.interfaces import TickableInterface, DrawableInterface
import vector
import numpy as np


def normalize(v: vector.VectorObject) -> vector.VectorObject:
    normalized_v = v / np.sqrt(np.sum(v ** 2))
    return normalized_v


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

    def init(
        self,
        pos: vector.VectorObject2D,
        size: int,
        target: vector.VectorObject2D = None,
    ):
        self.pos = pos
        self.size = vector.obj(x=size, y=size)
        if target != None:
            self.target = target

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
            self.set_target()
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


class OrbPool(DrawableInterface, TickableInterface):
    orbs: list[Orb] = []

    def tick(self):
        for o in self.orbs:
            o.tick()

    def draw(self, screen: Surface):
        for o in self.orbs:
            o.draw(screen)


class Game:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    WIDTH = 700
    HEIGHT = 500

    carryOn = False

    drawables: list[DrawableInterface] = []
    tickables: list[TickableInterface] = []

    def run(self):
        pygame.init()
        size = (self.WIDTH, self.HEIGHT)
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("stuff")
        self.carryOn = True
        clock = pygame.time.Clock()
        self.add_objects()
        while self.carryOn:
            for event in pygame.event.get():  # User did something
                self.check_for_quit(event)

            self.do_logic()
            self.do_draw(screen)
            # --- Limit to 60 frames per second
            clock.tick(60)

        pygame.quit()

    def add_objects(self):
        orb = Orb()
        orb.init(vector.obj(x=self.WIDTH / 2, y=self.HEIGHT / 2), 10)
        self.drawables.append(orb)
        self.tickables.append(orb)

    def check_for_quit(self, event):
        if event.type == pygame.QUIT:  # If user clicked close
            self.carryOn = False  # Flag that we are done so we exit this loop

    def do_logic(self):
        for t in self.tickables:
            t.tick()

    def do_draw(self, screen: pygame.Surface):
        screen.fill(self.BLACK)
        # pygame.draw.rect(screen, RED, [55, 200, 100, 70], 0)
        # pygame.draw.line(screen, GREEN, [0, 0], [100, 100], 5)
        # pygame.draw.ellipse(
        #     screen, self.WHITE, [size[0] / 2 - 5, size[1] / 2 - 5, 10, 10]
        # )
        for d in self.drawables:
            d.draw(screen)
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()


if __name__ == "__main__":
    Game().run()
