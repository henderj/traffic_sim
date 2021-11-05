from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder


class Agent(Widget):
    pass


class Game(Widget):
    pass


class TrafficSimApp(App):
    def build(self):
        Builder.load_file("traffic_sim.kv")
        game = Game()
        return game


if __name__ == "__main__":
    TrafficSimApp().run()
