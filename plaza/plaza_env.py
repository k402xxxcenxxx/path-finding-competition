import cv2
from scipy.spatial import KDTree

class MapImage():
    def __init__(self, filepath):
        self.filepath = filepath
        self.map_image = None
        self.map_images_3channel = None
        self.binary_map = None
        self.map_data = None
        self.height = -1
        self.width = -1

        self._read_map()

    def _read_map(self):
        self.map_image = cv2.imread(self.filepath, cv2.IMREAD_GRAYSCALE)
        _, binary_map = cv2.threshold(self.map_image, 128, 255, cv2.THRESH_BINARY)
        self.map_images_3channel = cv2.cvtColor(self.map_image, cv2.COLOR_GRAY2BGR)
        self.map_data = (binary_map // 255).astype(int)  # Convert to binary map
        self.height, self.width = self.map_data.shape

class Portal():
    def __init__(self, x, y, destinations):
        self.x , self.y = x, y
        self.destinations = []

class Map():
    def __init__(self, filepath, portals):
        self.map_image = MapImage(filepath)
        self.portals = portals
        self.portal_points = [(p["pos"]["x"], p["pos"]["y"]) for p in portals]
        self.kdtrees = KDTree(self.portal_points)

    def query(self, point: tuple, max_distance: float) -> dict | None:
        distance, idx = self.kdtrees.query(point)
        if distance > max_distance:
            return None
        else:
            return self.portals[idx]

class PlazaEnv():
    def __init__(self, maps):
        self.maps = [Map(m["filepath"], m["portals"]) for m in maps]

    def transfer(self, point: tuple, level: int, dest_level: int, max_distance: float = 3.0) -> dict | None:
        portal = self.maps[level].query(point, max_distance)
        if portal is None:
            return None
        else:
            for p in portal["dests"]:
                if p["level"] == dest_level:
                    return p
            return None
