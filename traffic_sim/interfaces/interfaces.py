from pygame import Surface


class DrawableInterface:
    def draw(self, screen: Surface):
        pass


class TickableInterface:
    def tick(self):
        pass
