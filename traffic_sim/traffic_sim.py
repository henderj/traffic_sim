from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.clock import Clock
from agent import Agent


class Game(Widget):
    agents: list[Agent] = []

    def awake(self) -> None:
        pass

    def start(self, dt: float) -> None:
        self.add_agent()

    def add_agent(self) -> None:
        agent = Agent()
        agent.initialize(self.center)
        self.agents.append(agent)
        self.add_widget(agent)

    def tick(self, dt: float) -> None:
        for a in self.agents:
            a.tick(dt)


class TrafficSimApp(App):
    def build(self):
        Builder.load_file("traffic_sim.kv")
        game = Game()
        game.awake()
        Clock.schedule_once(game.start)
        start_ticks = lambda dt: Clock.schedule_interval(game.tick, 1.0 / 60.0)
        Clock.schedule_once(start_ticks)
        return game


if __name__ == "__main__":
    TrafficSimApp().run()
