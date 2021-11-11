import os
import pygame
from pygame import Color, Vector2
from pygame import sprite
from pygame import surface
from pygame.sprite import AbstractGroup, Group
from pygame.surface import Surface
from pygame.time import Clock
from typing import Any

from traffic_sim.traffic_sim import SimData, TrafficSim


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
        e_data = data.entities[0]
        pos = data.nav_network[e_data["current_node_index"]]["pos"]
        pos = ((pos[0] * 64) + 32, (pos[1] * 64) + 20)
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


class SpriteSheet:
    # This class handles sprite sheets
    # This was taken from www.scriptefun.com/transcript-2-using
    # sprite-sheets-and-drawing-the-background
    # I've added some code to fail if the file wasn't found..
    # Note: When calling images_at the rect is the format:
    # (x, y, x + offset, y + offset)

    # Additional notes
    # - Further adaptations from https://www.pygame.org/wiki/Spritesheet
    # - Cleaned up overall formatting.
    # - Updated from Python 2 -> Python 3.
    def __init__(self, filename):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)

    def image_at(self, rectangle, colorkey=None):
        """Load a specific image from a specific rectangle."""
        # Loads image from x, y, x+offset, y+offset.
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey=None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey=None):
        """Load a whole strip of images, and return them as a list."""
        tups = [
            (rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
            for x in range(image_count)
        ]
        return self.images_at(tups, colorkey)

    def load_grid_images(
        self, num_rows, num_cols, x_margin=0, x_padding=0, y_margin=0, y_padding=0
    ):
        """Load a grid of images.
        x_margin is space between top of sheet and top of first row.
        x_padding is space between rows.
        Assumes symmetrical padding on left and right.
        Same reasoning for y.
        Calls self.images_at() to get list of images.
        """
        sheet_rect = self.sheet.get_rect()
        sheet_width, sheet_height = sheet_rect.size

        # To calculate the size of each sprite, subtract the two margins,
        #   and the padding between each row, then divide by num_cols.
        # Same reasoning for y.
        x_sprite_size = (
            sheet_width - 2 * x_margin - (num_cols - 1) * x_padding
        ) / num_cols
        y_sprite_size = (
            sheet_height - 2 * y_margin - (num_rows - 1) * y_padding
        ) / num_rows

        sprite_rects = []
        for row_num in range(num_rows):
            for col_num in range(num_cols):
                # Position of sprite rect is margin + one sprite size
                #   and one padding size for each row. Same for y.
                x = x_margin + col_num * (x_sprite_size + x_padding)
                y = y_margin + row_num * (y_sprite_size + y_padding)
                sprite_rect = (x, y, x_sprite_size, y_sprite_size)
                sprite_rects.append(sprite_rect)

        grid_images = self.images_at(sprite_rects)
        print(f"Loaded {len(grid_images)} grid images.")

        return grid_images


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
    last_tick: int = 0

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

        tileGrass = getTile(0, 2)
        tileVerticle = getTile(0, 0)
        tileIntersect = getTile(9, 0)
        tileHorizontal = getTile(0, 1)
        tileWater1 = getTile(3, 4)
        tileWater2 = getTile(4, 4)
        tileWater3 = getTile(3, 5)
        tileWater4 = getTile(4, 5)
        tileMap = [
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [2, 2, 2, 3, 2, 2, 2],
            [0, 0, 0, 1, 0, 4, 5],
            [0, 0, 0, 1, 0, 6, 7],
            [0, 0, 0, 1, 0, 0, 0],
        ]
        tileSize = tileGrass.get_size()
        tileDict = {
            0: tileGrass,
            1: tileVerticle,
            2: tileHorizontal,
            3: tileIntersect,
            4: tileWater1,
            5: tileWater2,
            6: tileWater3,
            7: tileWater4,
        }
        for y in range(len(tileMap)):
            for x in range(len(tileMap[y])):
                img = tileDict.get(tileMap[y][x])
                pos = (x * tileSize[0], y * tileSize[1])
                self.tile_sprites.add(Tile.build(img, pos, self.tile_sprites))

    def gameLoop(self):
        while self.running:
            self.clock.tick(self.FPS)
            deltaTime = self.clock.get_time() - self.last_tick
            self.last_tick = self.clock.get_time()
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
        entities = [
            {
                "active": True,
                "current_node_index": 0,
                "next_node_index": 1,
                "progress_to_next_node": 0.34,
                "target_node": 0,
                "path": [1, 2, 0],
                "speed": 1,
            }
        ]
        nav_network = [
            {"pos": (3, 0), "neighbors": [2]},
            {"pos": (0, 3), "neighbors": [2]},
            {"pos": (3, 3), "neighbors": [0, 1, 3, 4]},
            {"pos": (6, 3), "neighbors": [2]},
            {"pos": (3, 6), "neighbors": [2]},
        ]
        data = SimData(nav_network, entities, [], {})
        return data


if __name__ == "__main__":
    GAME = Game()
    GAME.run()
