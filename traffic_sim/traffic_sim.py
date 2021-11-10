from direct.showbase.ShowBase import ShowBase


class Game(ShowBase):
    def __init__(self, fStartDirect=True, windowType=None):
        super().__init__(fStartDirect=fStartDirect, windowType=windowType)
        self.scene = self.loader.loadModel("models/environment")
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        self.tile = self.loader.loadModel("../assets/egg/city.egg")
        self.tile.reparentTo(self.render)
        self.tile.setScale(1, 1, 1)
        self.tile.setPos(0, 0, 0)


if __name__ == "__main__":
    global GAME
    GAME = Game()
    GAME.run()
