from .simulation.gym import gym, env, agent

class TrafficAgent(agent.Agent):
    def action(self):
        '''Decide on road to take'''
        action = ei(self.state_history) 
        return action

class BraessEnv(env.Env):
    def __init__(self, superhighway=False):
        self.superhighway = superhighway
        if superhighway:
            self.state = {
                0: [1,2],
                1: [3],
                2: [3],
                3: []
            }
        else:
            self.state = {
                0: [1,2],
                1: [2,3],
                2: [3],
                3: []
            }

    def tick(self, actions):
        states = {}
        for aid, action in actions.items():
            states[aid] = self.state[action]
        return states

class BraessGym(gym.Gym):
    def tick(self):
        action = {}
        self.gen += 1
    
        for aid, agent in self.agents.items():
            action[aid] = agent.act(self.state[aid], self.reward)
        self.state, self.reward = self.env.tick(action)
