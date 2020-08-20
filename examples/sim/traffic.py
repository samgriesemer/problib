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
    'state_space': states,
    'action_space': actions,
    'entity_space': entities,
    'roads': roadnet
})

#########

# possible entity/agent creation
entities = [Car(1), Car(2), Car(3)]
agents = [Agent1(), Agent2(), Agent3()]

# possible entity/agent registry
traffic.add(entities, agents, 'main')
traffic.select('main').add(entities, agents)

# possibly index registry
traffic.register_index('main', lambda e: (e.x, e.y))

# internal group structure
groups = {
    'group_name': {
        'entities': [
            ...
        ],
        'indexes': [
            ...
        ]
    }, ...
}

# given some pre-registered entities, we have the agent registry
def create_agents(e, i):
    return Driver(e.frame)

traffic.add(create_agents, 'default')

# can split off and just believe agents will get registered; not like anyone needs to
# force it! especially if we're making the clear distinction b/t agent and entity, and
# the gym is technically optional
traffic.add(entities, 'group_name')



# nice for big groups
traffic.add(bunny_entities, 'bunnies')
traffic.add(fox_entities, 'foxes')

