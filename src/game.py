import os
import pygame
from pygame import Color, Vector2
from pygame import sprite
from pygame.sprite import AbstractGroup, Group
from pygame.surface import Surface
from pygame.time import Clock

from traffic_sim.traffic_sim import SimData, TrafficSim, getInitialData
from traffic_sim.pathfinding import Point, PointGraph
from utils.spritesheet import SpriteSheet
import traffic_sim.mapgenerator as mapgenerator


class Tile(sprite.Sprite):
    def init(self, image: Surface, pos):
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

    @staticmethod
    def build(image: Surface, pos, group: AbstractGroup):
        tile = Tile(group)
        tile.init(image, pos)
        return tile


class Car(sprite.Sprite):
    def init(self, image: Surface, pos):
        self.image = image
        self.rect = self.image.get_rect(center=pos)

    def update(self, data: SimData) -> None:
        e = data.entities[0]
        pos = e.tilePos()
        pos = Point((pos.x * 64) + 32, (pos.y * 64) + 20)
        self.rect = self.image.get_rect(center=pos)

    @staticmethod
    def build(image: Surface, pos, group: AbstractGroup):
        car = Car(group)
        car.init(image, pos)
        return car

    def rot_center(self, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(self.image, angle)
        rot_rect = rot_image.get_rect(center=self.rect.center)
        self.image = rot_image
        self.rect = rot_rect

    def scale(self, factor):
        size = (int(self.rect.size[0] * factor), int(self.rect.size[1] * factor))
        scaled_img = pygame.transform.scale(
            self.image,
            size,
        )
        scaled_rect = scaled_img.get_rect(center=self.rect.center)
        self.image = scaled_img
        self.rect = scaled_rect


class Game:
    SIZE = Vector2((448, 448))
    FPS = 30
    BACKGROUND_COLOR = Color(0, 0, 0)

    screen: Surface
    clock: Clock

    all_sprites: Group = Group()
    tile_sprites: Group = Group()

    data: SimData
    running: bool

    def run(self):
        pygame.init()
        self.setUp()
        self.gameLoop()
        pygame.quit()

    def setUp(self):
        self.screen = pygame.display.set_mode(size=self.SIZE)
        pygame.display.set_caption("Traffic Sim")
        self.clock = Clock()
        self.data = self.getInitialData()
        self.setUpMap()
        self.all_sprites.add(self.tile_sprites)
        car1 = Car.build(
            pygame.image.load(
                os.path.join("assets/2d/racing/PNG/Cars", "car_blue_small_1.png")
            ).convert_alpha(),
            (32, (64 * 3) + 20),
            self.all_sprites,
        )
        car1.rot_center(-90)
        car1.scale(0.5)
        self.running = True

    def setUpMap(self):
        tileSize = 64
        sheet = SpriteSheet(
            os.path.join("assets/2d/roads/Tilesheet", "roadTextures_tilesheet.png")
        )

        def getTile(x, y):
            return sheet.image_at((x * tileSize, y * tileSize, tileSize, tileSize))

        loadedTiles = {}

        nodes = {
            (0, 1): [(1, 1)],
            (0, 4): [(3, 4)],
            (1, 0): [(1, 1), (4, 0)],
            (1, 1): [(0, 1), (1, 0), (1, 3), (3, 1)],
            (1, 3): [(1, 1), (3, 3)],
            (3, 1): [(1, 1), (3, 3)],
            (3, 3): [(1, 3), (3, 1), (3, 4), (4, 3)],
            (3, 4): [(3, 3), (0, 4)],
            (4, 0): [(1, 0), (4, 3)],
            (4, 3): [(3, 3), (4, 0)],
        }
        graph = PointGraph(nodes)
        tileMap = mapgenerator.generateFromGraph(graph, (7, 7))
        spriteids = tileMap.spriteIds
        for y, row in enumerate(spriteids):
            for x, spritepos in enumerate(row):
                (sx, sy) = spritepos
                img: Surface
                if spritepos in loadedTiles:
                    img = loadedTiles[spritepos]
                else:
                    img = getTile(sx, sy)
                    loadedTiles[spritepos] = img
                tilePos = (x * tileSize, y * tileSize)
                self.tile_sprites.add(Tile.build(img, tilePos, self.tile_sprites))

    def gameLoop(self):
        while self.running:
            deltaTime = self.clock.tick(self.FPS)
            self.checkEvents()
            self.data = TrafficSim.tick(self.data, deltaTime)
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
        return getInitialData()


if __name__ == "__main__":
    GAME = Game()
    GAME.run()
