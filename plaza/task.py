from collections import Counter
import logging
from pprint import pformat
import yaml
import os
import cv2
import numpy as np

from plaza.algorithm import Algorithm
from plaza.plaza_db import PlazaDB
from plaza.plaza_env import PlazaEnv

class Task:
    def __init__(self, config_filepath="simple.yaml", num_item=2):
        self.logger = logging.getLogger(__name__)

        self.config = {}
        self.load_config(config_filepath)

        # init env 
        self.logger.debug("init env")
        self.env = PlazaEnv(self.obstacle_map_path)

        # init database
        self.logger.debug("init database")
        self.db = PlazaDB(self.db_path)

        # init task
        self.logger.debug("init task")
        self.num_item = num_item
        self.target_list = self.db.gets(self.num_item)
        self.target_set = Counter((obj["name"]) for obj in self.target_list)

        self.logger.info("Target buying list")
        self.logger.info(pformat(self.target_list))

        # init current item list
        self.logger.debug("init robot")
        self.item_list = []
        self.step_counter = 0

        # render component
        self.path_color = (255, 0, 0) # Blue
        self.collision_color = (0, 0, 255) # Red
        self.buy_color = (0, 255, 0) # Green
        self.path_image = np.ones((self.env.map_height, self.env.map_width, 3), dtype=np.uint8) * 255
        self.collision_point = None

    def load_config(self, filepath):
        self.config_dir = os.path.dirname(filepath)

        with open(filepath, 'r') as file:
            self.config = yaml.safe_load(file)
        
        self.obstacle_map_path = os.path.join(self.config_dir, self.config["world"]["obstacle_map"])
        self.db_path = os.path.join(self.config_dir, self.config["world"]["item_list"])
        self.start = (self.config["world"]["start"][0], self.config["world"]["start"][1])
        self.end = (self.config["world"]["end"][0], self.config["world"]["end"][1])
    
    def init_algorithm(self, algorithm: Algorithm):
        self.algorithm = algorithm
    
    def run(self):
        self.path = self.algorithm.find_path()
    
    def judge(self):
        self.step_counter = 0
        self.collision_point = None
        self.item_list = []
        self.current_set = ()
        self.path_image = self.env.map_image_3channel.copy() * 0.5
        
        self._judge_valid_path()
        self._judge_buying_list()

    def dump_path_image(self, path):
        cv2.imwrite(path, self.path_image)

    def _bresenham(self, x0, y0, x1, y1):
        """Bresenham's Line Algorithm to find all points between (x0, y0) and (x1, y1)."""
        points = []
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            points.append((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

        return points

    def _judge_valid_path(self):
        points = [p["pos"] for p in self.path if p["action"] == "move"]
        points.insert(0, self.start)
        points.append(self.end)

        for i in range(len(points) - 1):
            x0, y0 = points[i]
            x1, y1 = points[i + 1]
            line_points = self._bresenham(x0, y0, x1, y1)
            for point in line_points:
                self.step_counter += 1
                if self.env.map_data[point[1]][point[0]] == 0:  # 0 represents an obstacle
                    self.collision_point = point
                    cv2.circle(self.path_image, (point[0], point[1]), 1, self.collision_color, -1)
                    return
                else:
                    self.path_image[point[1], point[0]] = self.path_color
        return

    def _judge_buying_list(self):
        current_pos = self.start

        for p in self.path:
            if p["action"] == "move":
                current_pos = p["pos"]
            elif p["action"] == "buy":
                item = self.db.query(current_pos)
                self.item_list.append(item)
                if item != None:
                    cv2.circle(self.path_image, current_pos, 3, self.buy_color, -1)
            else:
                self.logger.warning(f"Invalid action: {p['action']}")
                self.item_list = []
                self.current_set = ()
                return
        
        if self.item_list:
            self.current_set = Counter((obj["name"]) for obj in self.item_list if obj != None)
        else:
            self.current_set = ()

        return

    def get_result(self):
        result = {
            "is_valid": self.collision_point == None,
            "is_finish": self.current_set == self.target_set,
            "collision_point": self.collision_point,
            "item_list": self.item_list,
            "total_step": self.step_counter
        }
        return result
    
    def draw(self):
        points = [p["pos"] for p in self.path if p["action"] == "move"]
        points.insert(0, self.start)
        points.append(self.end)

        for i in range(len(points) - 1):
            x0, y0 = points[i]
            x1, y1 = points[i + 1]
            line_points = self._bresenham(x0, y0, x1, y1)
            for point in line_points:
                tmp = self.path_image.copy()
                cv2.circle(tmp, (point[0], point[1]), 3, self.collision_color, 1)
                cv2.imshow("Path demo", tmp)
                cv2.waitKey(33)
                if cv2.waitKey(33) == ord('q'):
                    return

        return
