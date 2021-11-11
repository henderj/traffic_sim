from typing import NamedTuple
import pygame


class GameData:
    nav_network: None  # node tree or something
    entities: None  # array of entities (growable, active/inactive entities)
    tiles: None  # 2d array of tiles, will almost never change
    meta_data: None  # some game properties (speed, size, etc.), will almost never change


class Game:
    def run(self):
        pygame.init()
        pygame.quit()


if __name__ == "__main__":
    GAME = Game()
    GAME.run()
