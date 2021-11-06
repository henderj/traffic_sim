import pygame

from interfaces.interfaces import TickableInterface, DrawableInterface
import vector
from orb_pool import OrbPool


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
            clock.get_time()
            self.do_logic()
            self.do_draw(screen)
            # --- Limit to 60 frames per second
            clock.tick(60)

        pygame.quit()

    def add_objects(self):
        orb_pool = OrbPool()
        self.drawables.append(orb_pool)
        self.tickables.append(orb_pool)

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
