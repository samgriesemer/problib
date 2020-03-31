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

params = {
    'width': 5,
    'height': 5,
    'node_list': {
        (0,0): 'A',
        (1,0): 'A',
        (0,1): 'A',
    }
    'action_space': ['D','A'],
}

cellenv = env.Grid(**params)
cellgym = gym.Gym(cellenv)

cellgym.register_agent_class(LifeAutomata, 'life_automata')
cellgym.register_map('life_automata', 'default')
cellgym.register_agent(LifeAutomata(), params=(0,0,'A'))

# consider DEAP registry structure? adds flexibility, removes big init lists
#env.register('entity_space', [])

# EXPERIMENTAL
#def constraint(pstate, tstate):
    

