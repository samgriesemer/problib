from problib.sim import *

class TrafficEnv(env.Env):
    def __init__(self, roads: graph.Graph):
        self.roads = roads

class Car(entity.Entity):
    pass

class TrafficLight(entity.Entity):
    pass

# usage
states = space.Discrete()
actions = space.Discrete([1,2,3,4])

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
traffic = TrafficEnv({
    'state_space': states
    'action_space': actions
    'entity_space': entities
    'roads': roadnet
})

