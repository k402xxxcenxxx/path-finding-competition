from plaza.algorithm import Algorithm

from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

class PlazaAlgorithm(Algorithm):
    def __init__(self, map_data, items, start, end):
        super().__init__(map_data, items, start, end)

    def find_path(self):

        paths = []

        # Use A* algorithm for pathfinding
        grid = Grid(matrix=self.map_data.tolist())
    
        current_pos = self.start

        # straight forward order
        for item in self.items:
            
            start_node = grid.node(current_pos[0], current_pos[1])
            end_node = grid.node(item["pos"]["x"], item["pos"]["y"])
            finder = AStarFinder()
            path, _ = finder.find_path(start_node, end_node, grid)

            paths.extend([{
                "action": "move",
                "pos": (int(node.x), int(node.y))
            } for node in path])
            paths.append({
                "action": "buy"
            })

            current_pos = [item["pos"]["x"], item["pos"]["y"]]
            grid.cleanup()

        start_node = grid.node(current_pos[0], current_pos[1])
        end_node = grid.node(self.end[0], self.end[1])
        finder = AStarFinder()
        path, _ = finder.find_path(start_node, end_node, grid)

        paths.extend([{
            "action": "move",
            "pos": (int(node.x), int(node.y))
        } for node in path])

        return paths
