from problib.sim import *

class LifeAutomata(agent.Agent):
    def act(self):
        alive = 0
        for n in self.state['neighbors']:
            if n == 'A': alive += 1

        if self.state['self'] == 'A':
            if alive == 2 or alive == 3:
                return 'A'
            else: return 'D'
        else:
            if alive == 3:
                return 'A'
            else: return 'D'

def neighbors(packet, aid, eid):
    entity_index = packet['extra']['pos_index']
    entity = state['entities'][eid]
    pos = (entity.x, entity.y)
    state = {'self': packet['state'][eid].state}
    neighbor_list = []

    for i in range(-1,2):
        for j in range(-1,2):
            if i == 0 and j == 0: continue
            if entity_index[(pos[0]+i,pos[1]+j)]:
                nstate = entity_index[(pos[0]+i,pos[1]+j)].state
                neighbor_list.append[nstate]

    state['neighbors'] = neighbor_list
    packet['state'] = state
    return packet


cellenv = env.Grid({
    'width': 5,
    'height': 5,
    'node_list': {
        (0,0): 'A',
        (1,0): 'A',
        (0,1): 'A',
    }
    'action_space': ['D','A'],
})

cellgym = gym.Gym({
    'env': cellenv,
    'agent_map': {
        'life_automata': LifeAutomata
    },
    'default_map': {
        'life_automata': {
            'view': neighbors,
            'entity': 'cell'
    }
    'entity_agent_map': {
        'default': 'life_automata'
    }
})


# consider DEAP registry structure? adds flexibility, removes big init lists
env.register('entity_space', [])
env.register_entities({})
env.set_defaults({})


# EXPERIMENTAL
#def constraint(pstate, tstate):
    

