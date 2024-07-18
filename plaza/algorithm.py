from plaza.plaza_env import PlazaEnv

class Algorithm:
    def get_action(self, env: PlazaEnv):
        raise NotImplementedError("You must implement this function")

class Algorithm:
    def __init__(self, map_data, items, start, end):
        self.map_data = map_data
        self.items = items
        self.start = start
        self.end = end

    def find_path(self):
        raise NotImplementedError("You must implement this function")
