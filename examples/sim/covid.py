from problib.sim import *

class Cell(agent.Agent):
    def act(self):
        for n in self.state['neighbors']:
            # do something with n

params = {
    'width': 5,
    'height': 5,
    'action_space': ['R','G','B']
}

cellenv = env.Grid(**params)
cellgym = gym.Gym(cellenv)

cellgym.register(
