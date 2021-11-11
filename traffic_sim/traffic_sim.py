class SimData:
    nav_network: None  # node tree or something
    entities: None  # array of entities (growable, active/inactive entities)
    tiles: None  # 2d array of tiles, will almost never change
    meta_data: None  # some game properties (speed, size, etc.), will almost never change


class TrafficSim:
    @staticmethod
    def tick(data: SimData) -> SimData:
        return data
        newData = SimData()
        newData.nav_network = data.nav_network
        newData.entities = data.entities
        newData.tiles = data.tiles
        newData.meta_data = data.meta_data
        return newData
