import pygame
from pygame import draw
from random import randint


class DrawableInterface:
    def draw(self, screen: pygame.Surface):
        pass


class TickableInterface:
    def tick(self):
        pass


class Orb(DrawableInterface, TickableInterface):
    COLOR = (255, 255, 255)
    pos = (0, 0)
    size = 0

    def init(self, pos: tuple, size: int):
        self.pos = pos
        self.size = size

    def tick(self):
        dx = randint(-1, 1)
        dy = randint(-1, 1)
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)

    def draw(self, screen: pygame.Surface):
        screen_size = (screen.get_width(), screen.get_height())
        pos = self.pos
        size = self.size
        draw_pos = (pos[0] - size / 2, pos[1] - size / 2)
        pygame.draw.ellipse(screen, self.COLOR, [draw_pos[0], draw_pos[1], size, size])


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
        orb.init((self.WIDTH / 2, self.HEIGHT / 2), 10)
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
