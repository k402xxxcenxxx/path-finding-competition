import json
import random
from jsonschema import validate
from scipy.spatial import KDTree

class PlazaDB:
    schema = {
        "type": "array",
        "properties": {
            "name": {"type": "string"},
            "pos": {
                "type": "object",
                "properties": {
                    "x": {"type": "number"},
                    "y": {"type": "number"},
                    "level": {"type": "number"},
                },
                "required": ["x", "y", "level"]
            },
            "attributes": {
                "type": "object",
                "properties": {
                    "storage_temperature": {"type": "number"},
                    "weight": {"type": "number"},
                    "packaging_volume": {"type": "string"},
                    "fragile": {"type": "boolean"},
                },
                "required": [
                    "storage_temperature",
                    "weight",
                    "packaging_volume",
                    "fragile"
                ]
            }
        },
        "required": ["name", "pos", "attributes"]
    }

    def __init__(self, filepath: str) -> None:
        self.db = None

        with open(filepath, "r") as f:
            self.db = json.load(f)
            validate(instance=self.db, schema=self.schema)

        self.points = []
        self.attributes = []
        for d in self.db:
            while len(self.points) <= d["pos"]["level"]:
                self.points.append([])
                self.attributes.append([])
            self.points[d["pos"]["level"]].append((d["pos"]["x"], d["pos"]["y"]))
            self.attributes[d["pos"]["level"]].append(d)

        self.kdtrees = [KDTree(p) for p in self.points]

    def gets(self, num: int = 1) -> list:
        return random.sample(self.db, k=num)

    def query(self, point: tuple, level: int, max_distance: float = 3.0) -> object:
        distance, idx = self.kdtrees[level].query(point)
        if distance > max_distance:
            return None
        else:
            return self.attributes[level][idx]
