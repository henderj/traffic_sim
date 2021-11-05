from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.clock import Clock
from agent import Agent


class Game(Widget):
    agents: list[Agent] = []

    def set_up(self) -> None:
        self.add_agent()

    def add_agent(self) -> None:
        agent = Agent()
        self.agents.append(agent)
        self.add_widget(agent)

    def tick(self, dt: float) -> None:
        for a in self.agents:
            a.tick()


class TrafficSimApp(App):
    def build(self):
        Builder.load_file("traffic_sim.kv")
        game = Game()
        game.set_up()
        Clock.schedule_interval(game.tick, 1.0 / 60.0)
        return game


if __name__ == "__main__":
    TrafficSimApp().run()
