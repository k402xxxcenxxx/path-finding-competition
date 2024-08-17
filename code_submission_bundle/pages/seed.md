# Seed:

```python
# plaza_algorithm.py
from plaza.algorithm import Algorithm

from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from plaza.path import BuyAction, MoveAction, TranferAction, Action

class PlazaAlgorithm(Algorithm):
    def __init__(self, maps, items, start, start_level, end, end_level):
        super().__init__(maps, items, start, start_level, end, end_level)

    def find_path(self) -> list[Action]:

        paths = []

        # Use A* algorithm for pathfinding
        grids = [Grid(matrix=m.map_image.map_data.tolist()) for m in self.maps]

        current_pos = self.start
        current_level = self.start_level

        # straight forward order with level order
        sorted_items = sorted(self.items, key=lambda item: item['pos']['level'])

        for item in sorted_items:
            if current_level != item['pos']['level']:
                # Find path to portal and move then transfer
                target_level = item['pos']['level']
                target_portal = next((portal for portal in self.maps[current_level].portals if target_level in [d["level"] for d in portal['dests']]), None)

                if target_portal == None:
                    print(f"There is no portal to level: {target_level} in the current level: {current_level}")
                    print("It's too complicated, I give up")
                    return paths

                start_node = grids[current_level].node(current_pos[0], current_pos[1])
                end_node = grids[current_level].node(target_portal["pos"]["x"], target_portal["pos"]["y"])
                finder = AStarFinder()
                path, _ = finder.find_path(start_node, end_node, grids[current_level])

                paths.extend([MoveAction((int(node.x), int(node.y))) for node in path])
                paths.append(TranferAction(target_level))

                grids[current_level].cleanup()

                dest = next((dest for dest in target_portal["dests"] if target_level == dest["level"]), None)

                if dest == None:
                    print(f"There is no dests for level: {target_level} in the portal: {target_portal}")
                    print("Something wrong, I give up")
                    return paths

                current_pos = [dest["pos"]["x"], dest["pos"]["y"]]
                current_level = target_level

            # Find path to item and move then buy
            start_node = grids[current_level].node(current_pos[0], current_pos[1])
            end_node = grids[current_level].node(item["pos"]["x"], item["pos"]["y"])
            finder = AStarFinder()
            path, _ = finder.find_path(start_node, end_node, grids[current_level])

            paths.extend([MoveAction((int(node.x), int(node.y))) for node in path])
            paths.append(BuyAction())

            current_pos = [item["pos"]["x"], item["pos"]["y"]]
            grids[current_level].cleanup()

        if current_level != self.end_level:
            # Find path to portal and move then transfer
            target_level = self.end_level
            target_portal = next((portal for portal in self.maps[current_level].portals if target_level in [d["level"] for d in portal['dests']]), None)

            if target_portal == None:
                print(f"There is no portal to level: {target_level} in the current level: {current_level}")
                print("It's too complicated, I give up")
                return paths

            start_node = grids[current_level].node(current_pos[0], current_pos[1])
            end_node = grids[current_level].node(target_portal["pos"]["x"], target_portal["pos"]["y"])
            finder = AStarFinder()
            path, _ = finder.find_path(start_node, end_node, grids[current_level])

            paths.extend([MoveAction((int(node.x), int(node.y))) for node in path])
            paths.append(TranferAction(target_level))

            grids[current_level].cleanup()

            dest = next((dest for dest in target_portal["dests"] if target_level == dest["level"]), None)
            if dest == None:
                    print(f"There is no dests for level: {target_level} in the portal: {target_portal}")
                    print("Something wrong, I give up")
                    return paths

            current_pos = [dest["pos"]["x"], dest["pos"]["y"]]
            current_level = target_level

        # Find path to end position
        start_node = grids[current_level].node(current_pos[0], current_pos[1])
        end_node = grids[current_level].node(self.end[0], self.end[1])
        finder = AStarFinder()
        path, _ = finder.find_path(start_node, end_node, grids[current_level])

        paths.extend([MoveAction((int(node.x), int(node.y))) for node in path])

        return paths

```