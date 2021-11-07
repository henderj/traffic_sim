import pygame
from pygame import time
from typing import List
from orb_pool import OrbPool


class Game:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    WIDTH = 700
    HEIGHT = 500

    carryOn = False
    last_tick = 0

    sprites: List[pygame.sprite.Sprite] = []

    def run(self):
        pygame.init()
        size = (self.WIDTH, self.HEIGHT)
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("stuff")
        self.carryOn = True
        clock = pygame.time.Clock()
        self.add_objects()
        while self.carryOn:
            for event in pygame.event.get():
                self.check_for_quit(event)
            dt = self.get_delta_time()
            self.do_logic(dt)
            self.do_draw(screen)
            clock.tick(60)

        pygame.quit()

    def get_delta_time(self):
        current_tick = time.get_ticks()
        delta_time = current_tick - self.last_tick
        self.last_tick = current_tick
        return delta_time

    def add_objects(self):
        orb_pool = OrbPool()
        self.sprites.append(orb_pool)

    def add_sprite(self, sprite):
        self.sprites.append(sprite)

    def remove_sprite(self, sprite):
        self.sprites.remove(sprite)

    def check_for_quit(self, event):
        if event.type == pygame.QUIT:  # If user clicked close
            self.carryOn = False  # Flag that we are done so we exit this loop

    def do_logic(self, dt: int):
        for s in self.sprites:
            s.update(dt)

    def do_draw(self, screen: pygame.Surface):
        screen.fill(self.BLACK)
        for s in self.sprites:
            screen.blit(s.surf, s.rect)
        pygame.display.flip()


if __name__ == "__main__":
    global GAME
    GAME = Game()
    GAME.run()
