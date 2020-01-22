from problib.sim import *


class TrafficEnv(env.Env):
    def __init__(self, roads: graph.Graph):
        self.roads = roads