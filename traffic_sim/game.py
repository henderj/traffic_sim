import pygame
from pygame import Color, Vector2
from pygame.sprite import Group
from pygame.surface import Surface
from pygame.time import Clock

from traffic_sim.traffic_sim import SimData, TrafficSim


class Game:
    SIZE = Vector2((360, 480))
    FPS = 30
    BACKGROUND_COLOR = Color(0, 0, 0)

    screen: Surface
    clock: Clock

    all_sprites: Group
    tile_sprites: Group

    data: SimData
    running: bool

    def run(self):
        pygame.init()
        self.data = self.getInitialData()
        self.setUp()
        self.gameLoop()
        pygame.quit()

    def setUp(self):
        self.screen = pygame.display.set_mode(size=self.SIZE)
        pygame.display.set_caption("Traffic Sim")
        self.clock = Clock()
        self.all_sprites = Group()
        self.tile_sprites = Group()
        self.running = True

    def gameLoop(self):
        while self.running:
            self.clock.tick(self.FPS)
            self.checkEvents()
            self.data = TrafficSim.tick(self.data)
            self.all_sprites.update(self.data)
            self.render()

    def render(self):
        self.screen.fill(self.BACKGROUND_COLOR)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    @staticmethod
    def getInitialData():
        data = SimData()
        return data


if __name__ == "__main__":
    GAME = Game()
    GAME.run()
