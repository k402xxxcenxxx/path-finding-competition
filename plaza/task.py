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
from plaza.path import ActionType

class Task:
    def __init__(self, config_filepath="simple.yaml", num_item=2):
        self.logger = logging.getLogger(__name__)

        self.config = {}
        self.load_config(config_filepath)

        # init env
        self.logger.debug("init env")
        self.env = PlazaEnv(self.maps)

        # init database
        self.logger.debug("init database")
        self.db = PlazaDB(self.db_path)

        # init task
        self.logger.debug("init task")
        self.num_item = num_item
        self.target_list = self.db.gets(self.num_item)
        self.target_set = Counter((obj["name"]) for obj in self.target_list)
        self.is_valid = False

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
        self.path_image = None
        self.path_image_y_offsets = []
        self.collision_point = None

    def load_config(self, filepath):
        self.config_dir = os.path.dirname(filepath)

        with open(filepath, 'r') as file:
            self.config = yaml.safe_load(file)

        self.maps = self.config["plaza"]["maps"]
        for m in self.maps:
            m["filepath"] = os.path.join(self.config_dir, m["image"])
        self.db_path = os.path.join(self.config_dir, self.config["plaza"]["item_list"])
        self.start = (self.config["plaza"]["start"]["pos"]["x"], self.config["plaza"]["start"]["pos"]["y"])
        self.end = (self.config["plaza"]["end"]["pos"]["x"], self.config["plaza"]["end"]["pos"]["y"])
        self.start_level = self.config["plaza"]["start"]["level"]
        self.end_level = self.config["plaza"]["end"]["level"]

    def init_algorithm(self, algorithm: Algorithm):
        self.algorithm = algorithm

    def run(self):
        self.path = self.algorithm.find_path()

    def judge(self):
        self.step_counter = 0
        self.collision_point = None
        self.item_list = []
        self.current_set = ()
        self._init_path_image()

        self._judge_valid_path()

    def _init_path_image(self):
        self.path_image = np.ones((sum([m.map_image.height for m in self.env.maps]), max([m.map_image.width for m in self.env.maps]), 3), dtype=np.uint8) * 255
        self.path_image_y_offsets = [0]
        idx = 0
        for m in self.env.maps:
            map_img = m.map_image
            y_offset = self.path_image_y_offsets[idx]
            height, width = map_img.height, map_img.width
            self.path_image[y_offset:y_offset + height, :width] = map_img.map_images_3channel * 0.5
            y_offset += height
            self.path_image_y_offsets.append(y_offset)
            idx += 1

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

    def _is_valid_line(self, p1: tuple, p2: tuple, level: int):
        x0, y0 = p1
        x1, y1 = p2
        line_points = self._bresenham(x0, y0, x1, y1)
        for point in line_points:
            self.step_counter += 1
            if self.env.maps[level].map_image.map_data[point[1]][point[0]] == 0:  # 0 represents an obstacle
                self.collision_point = point
                cv2.circle(self.path_image, (self.path_image_y_offsets[level] + point[0], point[1]), 1, self.collision_color, -1)
                return False
            else:
                self.path_image[self.path_image_y_offsets[level] + point[1], point[0]] = self.path_color
        return True

    def _judge_valid_path(self):
        current_level = self.start_level
        current_pos = self.start

        for p in self.path:
            if p.type == ActionType.TRANSFER:
                dest_level = p.level
                portal = self.env.transfer( current_pos, current_level, dest_level)

                if portal == None:
                    self.logger.warning(f"Invalid transfer action: level: {current_level}, pos: {current_pos}, dest_level: {dest_level}")
                else:
                    current_pos = (portal["pos"]["x"], portal["pos"]["y"])
                    current_level = dest_level

            elif p.type == ActionType.MOVE:
                if not self._is_valid_line(current_pos, p.pos, current_level):
                    self.is_valid = False
                    return
                else:
                    current_pos = p.pos

            elif p.type == ActionType.BUY:
                item = self.db.query(current_pos, current_level)
                if item == None:
                    self.logger.warning(f"Invalid buy action: level: {current_level}, pos: {current_pos}")
                else:
                    self.item_list.append(item)
                    buy_draw_point = (current_pos[0], self.path_image_y_offsets[current_level] + current_pos[1])
                    cv2.circle(self.path_image, buy_draw_point, 3, self.buy_color, -1)
            else:
                self.logger.warning(f"Invalid action: {p}")
                self.is_valid = False
                self.item_list = []
                self.current_set = ()
                return

        if self.item_list:
            self.current_set = Counter((obj["name"]) for obj in self.item_list if obj != None)
        else:
            self.current_set = ()

        if current_level != self.end_level:
            self.is_valid = False
        else:
            self.is_valid = self._is_valid_line(current_pos, self.end, current_level)

    def get_result(self):
        result = {
            "is_valid": self.is_valid,
            "is_finish": self.current_set == self.target_set,
            "collision_point": self.collision_point,
            "item_list": self.item_list,
            "total_step": self.step_counter
        }
        return result

    def draw(self):
        current_level = self.start_level
        current_pos = self.start

        for p in self.path:
            if p.type == ActionType.TRANSFER:
                dest_level = p.level
                portal = self.env.transfer(current_pos, current_level, dest_level)

                current_pos = (portal["pos"]["x"], portal["pos"]["y"])
                current_level = dest_level

            elif p.type == ActionType.MOVE:
                x0, y0 = current_pos
                x1, y1 = p.pos
                line_points = self._bresenham(x0, y0, x1, y1)
                for point in line_points:
                    tmp = self.path_image.copy()
                    cv2.circle(tmp, (point[0], self.path_image_y_offsets[current_level] + point[1]), 3, self.collision_color, 1)
                    cv2.imshow("Path demo", tmp)
                    cv2.waitKey(33)
                    if cv2.waitKey(33) == ord('q'):
                        return
                current_pos = p.pos
            elif p.type == ActionType.BUY:
                item = self.db.query(current_pos, current_level)
                if item != None:
                    tmp = self.path_image.copy()
                    buy_draw_point = (current_pos[0], self.path_image_y_offsets[current_level] + current_pos[1])
                    cv2.circle(tmp, buy_draw_point, 3, self.buy_color, -1)
                    cv2.imshow("Path demo", tmp)
                    cv2.waitKey(33)
                    if cv2.waitKey(33) == ord('q'):
                        return
