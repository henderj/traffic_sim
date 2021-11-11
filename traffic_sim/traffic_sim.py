class SimData:
    nav_network: None  # node tree or something
    entities: None  # array of entities (growable, active/inactive entities)
    tiles: None  # 2d array of tiles, will almost never change
    meta_data: None  # some game properties (speed, size, etc.), will almost never change


class TrafficSim:
    @staticmethod
    def tick(data: SimData) -> SimData:
        pass
