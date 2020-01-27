from problib.sim.gym import gym, env, agent, policy
import random
import copy

class Car():
    def __init__(self):
        self.state = [0]

    def drive(self, road):
        self.state.append(road)

class TrafficAgent(agent.Agent):
    def observe(self):
        # restrict agents knowledge to only their own state
        self.obs = self.state[self.id]

    def action(self):
        '''Decide on road to take'''
        #action = policy.ei(self.state_history)
        return random.choice(self.state)

class TrafficEnv(env.Env):
    def __init__(self, superhighway=None, f=25, d=100):
        self.f = f
        self.d = d
        self.cars = {}
        self.roads = {
            0: [1,2],
            1: [3],
            2: [3],
            3: []
        }
        self.costs = {
            0: [0, f],
            1: [f],
            2: [0],
            3: []
        }

        if superhighway is not None:
            self.roads[1].insert(0,2)
            self.costs[1].insert(0,0)

    def start(self):
        return self.roads[0]

    def register_car(self, agent):
        self.cars[agent.id] = Car()

    def tick(self, actions):
        # reset road costs
        costs = copy.deepcopy(self.costs)
        state = {}
        for aid, action in actions.items():
            car = self.cars[aid]
            car.drive(action)
            state[aid] = self.roads[action]

            # update costs
            if car.state[-1] == 1:
                costs[0][0] += 1/self.d
            elif car.state[-1] == 3:
                if car.state[-2] == 2:
                    costs[2][0] += 1/self.d

        self.state = state
        self.costs = costs
        return self.state, self.costs

class TrafficGym(gym.Gym):
    def tick(self):
        action = {}
        self.gen += 1

        for aid, agent in self.agents.items():
            action[aid] = agent.act(self.state, self.reward)
        self.state, self.reward = self.env.tick(action)

    def start(self):
        st = self.env.start()
        for aid, agent in self.agents.items():
            agent.state = st
            self.state[aid] = st

    def register_agent(self, agent):
        super().register_agent(agent)
        self.env.register_car(agent)
