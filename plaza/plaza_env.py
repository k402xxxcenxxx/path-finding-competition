from ir_sim.env import EnvBase
from ir_sim.global_param import env_param, world_param
import numpy as np

# Overwrite the collision behavior
def step(self, velocity=None, **kwargs):
    if self.static or self.stop_flag:

        self._velocity = np.zeros_like(velocity)

        return self._state  

    else: 
        
        self.pre_process()

        behavior_vel = self.gen_behavior_vel(velocity, )

        origin_state = self._state
        origin_velocity = self._velocity
        origin_geometry = self._geometry
        
        new_state = self._kinematics(behavior_vel, **self.kinematics_dict, **kwargs)
        next_state = self.mid_process(new_state)

        self._state = next_state
        self._velocity = behavior_vel

        self._geometry = self.geometry_transform(self._init_geometry, self._state)

        self.sensor_step()
        self.post_process()
        self.check_status()
        
        if world_param.collision_mode == 'reactive' and self.collision_flag is True:
            # rollback
            env_param.logger.warning( self.role + "{} roll back state".format(self.id))
            self._state = origin_state
            self._velocity = origin_velocity
            self._geometry = origin_geometry
            self.collision_flag = False

        self.trajectory.append(self._state.copy())
            
        return next_state

class PlazaEnv(EnvBase):
    def __init__(self, world_name=None, display=True, disable_all_plot=False, save_ani=False, full=False, log=True, log_file='ir_sim.log', log_level='INFO', **kwargs):
        super().__init__(world_name, display, disable_all_plot, save_ani, full, log, log_file, log_level, **kwargs)

        # Overwrite the step function
        for o in self.objects:
            funcType = type(o.step)
            o.step = funcType(step, o)

