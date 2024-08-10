from plaza.plaza_env import Map

class Algorithm:
    def __init__(self, maps: list[Map], items, start, start_level, end, end_level):
        self.maps = maps
        self.items = items
        self.start = start
        self.start_level = start_level
        self.end = end
        self.end_level = end_level

    def find_path(self):
        raise NotImplementedError("You must implement this function")
