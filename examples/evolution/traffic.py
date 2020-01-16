from problib.sim import gym, env

class TrafficEnv(env.Env):
    def __init__(self, roads: graph.Graph):
        self.roads = roads