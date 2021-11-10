import pygame


class Game:
    def run(self):
        pygame.init()
        pygame.quit()


if __name__ == "__main__":
    global GAME
    GAME = Game()
    GAME.run()
