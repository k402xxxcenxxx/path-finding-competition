from collections import Counter
import logging
from pprint import pformat

from plaza.plaza_algorithm import PlazaAlgorithm
from plaza.plaza_db import PlazaDB
from plaza.plaza_env import PlazaEnv

class Task:
    def __init__(self, map_filepath="simple.yaml", db_filepath="plaza_data.json", num_item=2):
        self.logger = logging.getLogger(__name__)

        # init env 
        self.logger.debug("init env")
        # env = PlazaEnv('plaza_world.yaml', save_ani=False, rm_fig_path=False, full=False)
        self.env = PlazaEnv(map_filepath)

        # init database
        self.logger.debug("init database")
        self.db = PlazaDB(db_filepath)

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
    
        self.algorithm = PlazaAlgorithm(self.db, self.target_list)
    
    def run(self, max_steps: int = 1000):
        for _ in range(max_steps):
            state = self.env.get_robot_state()
            logging.debug("Current state")
            logging.debug(state)

            action = self.algorithm.get_action(self.env)
            logging.debug(pformat(action))

            if action["type"] == "move":

                self.env.step([action["value"]])
                self.step_counter += 1

            elif action["type"] == "buy":

                pos = [state[0][0], state[1][0]]
                item = self.db.query(pos)

                if item is None:
                    logging.warning(f"No item is here to buy: {pos}")
                else:
                    self.item_list.append(item)

            else:
                logging.warning(f'Invalid action {action["type"]}')

            self.env.render(0.01, show_goal=False, show_trajectory=True)

            if self.judge():
                self.env.end(1)
                return True
        
        logging.warning(f"Max step {max_steps} exceed")
        self.env.end(1)
        return False
    
    def judge(self):

        current_set = Counter((obj["name"]) for obj in self.item_list)

        return current_set == self.target_set

    def get_result(self):
        result = {
            "item_list": self.item_list,
            "total_step": self.step_counter
        }
        return result