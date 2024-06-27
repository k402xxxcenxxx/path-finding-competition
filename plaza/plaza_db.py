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
                },
                "required": ["x", "y"]
            }
        },
        "required": ["name", "pos"]
    }

    def __init__(self, filepath: str) -> None:
        json_data = None

        with open(filepath, "r") as f:
            json_data = json.load(f)
            validate(instance=json_data, schema=self.schema)

        self.points = [(d["pos"]["x"], d["pos"]["y"]) for d in json_data]
        self.attributes = json_data

        self.kdtree = KDTree(self.points)

    def gets(self, num: int = 1) -> list:
        return random.sample(self.attributes, k=num)

    def query(self, point: tuple, max_distance: float = 1.0) -> object:
        distance, idx = self.kdtree.query(point)
        if distance > max_distance:
            return None
        else:
            return self.attributes[idx]
