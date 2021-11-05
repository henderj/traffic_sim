from kivy.uix.widget import Widget


class Agent(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def tick(self, dt: float) -> None:
        pass
