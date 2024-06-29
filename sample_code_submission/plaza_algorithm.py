from ir_sim.lib.behaviorlib import DiffDash
from ir_sim.util.util import relative_position
import numpy as np
from plaza.algorithm import Algorithm
from plaza.plaza_env import PlazaEnv
from plaza.plaza_db import PlazaDB

# Simplest algorithm
class PlazaAlgorithm(Algorithm):
    def __init__(self, db: PlazaDB, target_list: list) -> None:
        self.db = db
        self.target_list = target_list
        self.current_list = []


    def get_action(self, env: PlazaEnv):
        
        print("HAHAHA")
        target = self.target_list[len(self.current_list)]
        target_state = [[target["pos"]["x"]], [target["pos"]["y"]], [0], [0]]

        robot_state = env.get_robot_state()

        distance, _ = relative_position(robot_state, target_state) 

        if distance < 1:
            self.current_list.append(target)
            return {
                "type": "buy",
                "value": []
            }
        else:
            movement = DiffDash(robot_state, target_state, np.array([[1], [1]]))
            return {
                "type": "move",
                "value": movement
            }
