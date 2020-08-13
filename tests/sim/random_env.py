from problib.sim import env, space, entity

action_space = space.Discrete(['a','b','c'])
state_space = space.Discrete([1,2,3])
entity_space = space.Discrete([entity.Entity])

renv = env.RandomEnv(action_space, state_space, entity_space)


class Property(Entity):
    """Docstring for Property. """

    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

        
properties = [{'name': 'Boardwalk', 'cost': 1e6}]
mon = MonopolyEnv(properties, players=4)

mon.select('properties').data([
    {'name': 'Boardwalk', 'cost': 1e6},
]).enter()

