from .simulation.gym import gym, env, agent, policy

class Car():
    def __init__(self, aid):
        self.aid = aid
        self.state = [0]
    
    def drive(self, road):
        self.state.append(road)

class TrafficAgent(agent.Agent):
    def action(self):
        '''Decide on road to take'''
        action = policy.ei(self.state_history) 
        return action

class TrafficEnv(env.Env):
    def __init__(self, superhighway=None, f=25, d=100):
            self.state = {
                'roads': {
                    0: [1,2],
                    1: [3],
                    2: [3],
                    3: []
                },
                'costs': {
                    0: [0, f],
                    1: [f],
                    2: [0],
                    3: []
                }
            }
        if superhighway is not None:
            self.state['roads'][1].insert(0,2)
            self.state['costs'][1].insert(0,0)

    def tick(self, actions):
        states = {}
        costs = {}
        for aid, action in actions.items():
            states[aid] = self.state['roads'][action]
            if action == 1: costs[0][0] += 1/d
        return states

class TrafficGym(gym.Gym):
    def tick(self):
        action = {}
        self.gen += 1
    
        for aid, agent in self.agents.items():
            action[aid] = agent.act(self.state[aid], self.reward)
        self.state, self.reward = self.env.tick(action)
