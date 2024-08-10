from plaza.algorithm import Algorithm

from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

import cv2

class PlazaAlgorithm(Algorithm):
    def __init__(self, maps, items, start, start_level, end, end_level):
        super().__init__(maps, items, start, start_level, end, end_level)

    def find_path(self):

        paths = []

        # Use A* algorithm for pathfinding
        grids = [Grid(matrix=m.map_image.map_data.tolist()) for m in self.maps]

        current_pos = self.start
        current_level = self.start_level

        # straight forward order with level order
        sorted_items = sorted(self.items, key=lambda item: item['pos']['level'])

        for item in sorted_items:
            if current_level != item['pos']['level']:
                target_level = item['pos']['level']
                target_portal = next((portal for portal in self.maps[current_level].portals if target_level in [d["level"] for d in portal['dests']]), None)

                start_node = grids[current_level].node(current_pos[0], current_pos[1])
                end_node = grids[current_level].node(target_portal["pos"]["x"], target_portal["pos"]["y"])
                finder = AStarFinder()
                path, _ = finder.find_path(start_node, end_node, grids[current_level])

                paths.extend([{
                    "action": "move",
                    "pos": (int(node.x), int(node.y))
                } for node in path])
                paths.append({
                    "action": "transfer",
                    "level": target_level
                })

                grids[current_level].cleanup()

                dest = next((dest for dest in target_portal["dests"] if target_level == dest["level"]), None)
                current_pos = [dest["pos"]["x"], dest["pos"]["y"]]
                current_level = target_level

            start_node = grids[current_level].node(current_pos[0], current_pos[1])
            end_node = grids[current_level].node(item["pos"]["x"], item["pos"]["y"])
            finder = AStarFinder()
            path, _ = finder.find_path(start_node, end_node, grids[current_level])

            paths.extend([{
                "action": "move",
                "pos": (int(node.x), int(node.y))
            } for node in path])
            paths.append({
                "action": "buy"
            })

            current_pos = [item["pos"]["x"], item["pos"]["y"]]
            grids[current_level].cleanup()

        if current_level != self.end_level:
            target_level = self.end_level
            target_portal = next((portal for portal in self.maps[current_level].portals if target_level in [d["level"] for d in portal['dests']]), None)

            start_node = grids[current_level].node(current_pos[0], current_pos[1])
            end_node = grids[current_level].node(target_portal["pos"]["x"], target_portal["pos"]["y"])
            finder = AStarFinder()
            path, _ = finder.find_path(start_node, end_node, grids[current_level])

            paths.extend([{
                "action": "move",
                "pos": (int(node.x), int(node.y))
            } for node in path])
            paths.append({
                "action": "transfer",
                "level": target_level
            })

            grids[current_level].cleanup()

            dest = next((dest for dest in target_portal["dests"] if target_level == dest["level"]), None)
            current_pos = [dest["pos"]["x"], dest["pos"]["y"]]
            current_level = target_level

        start_node = grids[current_level].node(current_pos[0], current_pos[1])
        end_node = grids[current_level].node(self.end[0], self.end[1])
        finder = AStarFinder()
        path, _ = finder.find_path(start_node, end_node, grids[current_level])

        paths.extend([{
            "action": "move",
            "pos": (int(node.x), int(node.y))
        } for node in path])

        return paths
