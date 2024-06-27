from plaza.plaza_env import PlazaEnv

class Algorithm:
    def get_action(self, env: PlazaEnv):
        raise NotImplementedError("You must implement this function")
