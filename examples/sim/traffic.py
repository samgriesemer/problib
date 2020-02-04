from problib.sim import *

class TrafficEnv(env.Env):
    def __init__(self, roads: graph.Graph):
        self.roads = roadsA


# usage
entities = {
    'car': Car,
    'traffic_light': TrafficLight
}

# define road network structure
roadnet = graph.UndirectedGraph({
    0: [1,2],
    1: [2,3]
})

# initialize new traffic env
traffic = TrafficEnv(roadnet)

env.make('Traffic
