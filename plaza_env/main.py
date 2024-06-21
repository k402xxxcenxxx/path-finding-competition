from plaza_env import PlazaEnv
env = PlazaEnv('plaza_world.yaml', save_ani=False, rm_fig_path=False, full=False)

for i in range(1000):

    env.step()
    env.render(0.05, show_goal=False, show_trajectory=True)
    
    if env.done():
        break

env.end(10)