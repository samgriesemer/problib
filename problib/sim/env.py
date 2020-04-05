import string

from . import entity
from ..combinatorics.counting import Product

class Env():
    '''
    Base environment class outlining simple tick, draw, and create methods. All
    environments to be used inside a Gym or interacting with Agent types
    should inherit this interface. Need to provide a state and action space
    for defining valid actions and return states.

    Environments encompass all of the components necessary for action execution.
    Environments should be independent of the agents interacting with it; it is not
    concerned with how the agents make decisions but only how to execute submitted
    actions against ingrained constraints.

    This environment module is designed with multi agent systems in mind. Environments
    don't have to be crafted with specific elements and logic built-in. The implementation
    intends to be general enough to allow for factory object registration; this is often
    important when creating or changing an agents representation in the simulation at run time
    or dynamically before hand. This is where the library differs from existing implementations
    like OpenAI's gym library; it uses a more general and flexible approach.
    '''
    def __init__(self, options):
        # base env variables, expect inheriting env to modify these according
        # their own defaults. Since these get set whether the client specifies them
        # or not (that's where `options` is coming from, the inheriting env knows
        # they will at least be set to a null value Note that this null value needs
        # to still be a valid object of each of these respective types, perhaps a space.
        # Even when empty, the "null" object still needs to be able to be used without
        # throwing errors all over the place because it's not a "expected null format", if
        # you will.
        self.action_space = {}
        if 'action_space' in options:
            self.action_space = options['action_space']

        self.entity_space = {}
        if 'entity_space' in options:
            self.entity_space = options['entity_space']

        self.index_space = {}
        if 'index_space' in options:
            self.index_space = options['index_space']

        # full environment state, describes every piece of information that would be needed to
        # recreate the same state in a different instance
        self.state = {}

        # canonical entity dict mapping from entity id (string) to entity instances
        self.entities = {}

        self.indexes = {}

        # entity groups, determine if part of indexes or deserve distinction
        self.groups = {'default': [], 'all': []}

        # create id generator
        chars = string.printable[:61]
        self.idgen = Product(chars, repeat=3).sample_without_replacement(-1)

    def tick(self, action, sandbox=False):
        '''
        Execute given agent(s) action(s) and perform single environment tick. Can be
        dynamic (e.g. call on physics engine) or static. Agent actions are subject
        to internally defined constraints (i.e. agent desires may not be executed
        exactly as intended due to realistic limitations). Returns a tuple containing the
        new environment state, the reward, and whether or not the env has reached termination.

        This method implements what is commonly referred to as the "successor/transition function".
        It is a function that maps input from the state space (current state), action space X entity space
        (submitted agent actions) to the state space (next state)

        NEW: sandbox execution mode, to accommodate rollouts and internal agent planning simulations
        '''
        return self.state, 0, False

    def create(self, entity_name, opts={}):
        '''
        Create an entity of the specified type, use the given params. Used to populate
        the environment with objects necessary to the simulation. This method is provided
        for working with environments that need to be dynamic and update the entities within
        while the simulation is running.

        :type: An entity from the entity space
        '''
        if entity_name not in self.entity_space:
            raise Exception('Entity not recognized by environment')

        options = {
            'params': {},
            'count': 1,
            'groups': []
        }
        
        options.update(opts)
        entity_class = self.entity_space[entity_name]

        for _ in range(options['count']):
            entity = entity_class(**options['params'])
            eid = entity_name+''.join(next(self.idgen))
            self.entities[eid] = entity
            entity.id = eid

            self.groups['all'].append(entity)
            for group in options['groups']:
                if group not in self.groups:
                    self.groups[group] = []
                self.groups[group].append(entity)

            for index, func in self.index_space[entity_name]:
                index[func(entity)] = entity

        return entity

class Static(Env):
    '''
    Environment for defining a static state. To be used as a simple environment object
    inheriting necessary interface when some static context is needed for agent reference.
    Adds nothing to the base class.
    '''
    pass

class RandomState(Env):
    '''
    Simple random state environment. Takes given state, action, and entity spaces and simply samples
    random states at each tick. This env is independent of any assigned agents.
    '''
    def tick(self, action=None):
        return self.state_space.sample(), 0, False

class Grid(Env):
    def __init__(self, options):
        # initialize base
        super().__init__(options)
        
        #### STRUCTURE ####
        ### LOCAL STRUCTURE ###
        ## SET LOCAL DEFAULT BASE STRUCTURE

        ## SET LOCAL PARAMETRIZED BASE STRUCTURE
        # required parametric structure
        self.width = options['width']
        self.height = options['height']

        # optional parametric structure
        self.node_list = options.get('node_list')

        ### GLOBAL STRUCTURE ####
        ## SET GLOBAL DEFAULT BASE STRUCTURE 
        # base entities
        self.entity_space.update({
            'cell': entity.Cell
        })
        
        # no default for action_space, deferred entirely to base
        # and thus must be user defined
        
        ## SET GLOBAL PARAMETRIZED BASE STRUCTURE
        # (this is handled by the base env!)

        ### INDEXES ###
        # create base entity indexes (for now no direct parametric support)
        self.index_space.update({
            'pos': lambda x: return (x.i, x.j)
        })
        
        ### ENTITY CREATION ###
        # default internal entities (all external directed through create())
        for i in range(self.width):
            for j in range(self.height):
                cell_state = self.action_space[0]
                if (i,j) in self.node_list:
                    cell_state = self.node_list[(i,j)]

                self.create('cell', {
                    'params': {'x':i, 'y':j, 'state':cell_state},
                    'groups': ['default']
                })

    def tick(self, actions):
        for eid, action in actions.items():
            self.entities[eid].update(action)
            self.state['entities'] = [vars(e) for e in self.entities.values()]
        return self.packet

    @property
    def packet(self):
        return {
            'state': {
                'entities' = [vars(e) for e in self.entities.values()]
            },
            'reward': None,
            'done': False,
            'extra': {
                'indexes': self.
            }
        }

class Box(Env):
    '''
    Naive implementation, simple velocity and position
    updates on body of defined point objects. Action space
    includes all real number within velocity ranges, and the state
    is the current set of physics entities and their 2D positions.

    For now, the state (method) property is not resitricted and is
    encouraged to update state after entity creation/removal has occurred.
    No other entity state's are affected, so no standard implementation
    should expect any side effects. Ultimately this may need reconsideration,
    but it has backing as explained in the docs.
    '''
    def __init__(self, width, height, vxrng, vyrng, axrng=[0,0], ayrng=[0,0], entities=[]):
        # set initial entities (to be formalized later)
        self.width = width
        self.height = height
        self.vxrng = vxrng
        self.vyrng = vyrng
        self.axrng = axrng
        self.ayrng = ayrng

        # create underlying physics engine
        self.engine = Engine(entities)

    @classmethod
    def random(cls, n, width, height, vxrng, vyrng, axrng, ayrng):
        '''
        Alternate constructor for random creation of entities
        NOTE: entities currently removed from constructor and
        dependent on agent registry
        '''
        entities = []
        for _ in range(n):
            e = Entity.random((0, width), (0, height), vxrng, vyrng)
            entities.append(e)
        return cls(entities, width, height, vxrng, vyrng)

    @property
    def state(self):
        return self.engine.entity_arrays()

    def start(self):
        return self.state, self.state

    def tick(self, actions={}):
        '''
        Handles action requests to engine entities, returns resulting
        state. Note for multi-agent systems, `action` is a list of actions
        to be performed by each agent at the current step

        :actions: list of actions in form {'action':<str>, 'aid':<int>, value:{'x':<int>, 'y':<int>}}
        :actions: numpy array of four needed values
        ::known actions:: ['setv']
        '''
        # update entities and agents
        for eid, action in actions.items():
            entity    = self.engine.entities[eid]
            entity.vx = self.clip(action[0], self.vxrng)
            entity.vy = self.clip(action[1], self.vyrng)
            entity.ax = self.clip(action[2], self.axrng)
            entity.ay = self.clip(action[3], self.ayrng)

        # call physics tick
        self.engine.tick()
        return self.state, self.state

    def run(self, gens=-1):
        yield {'state':self.start()[0]}
        gen = 0
        while gen != gens:
            yield {'gen':gen, 'state':self.tick()[0]}
            gen += 1

    def random_entity(self):
        '''return entity ID so we know how pass actions back to the env'''
        entity = Entity.random((0,self.width), (0,self.height), \
                                       self.vxrng, self.vyrng, self.axrng, self.ayrng)
        self.engine.add(entity)
        # return entity.id
        return id(entity)

    def remove_entity(self, eid):
        self.engine.remove(eid)

    def clip(self, val, rng):
        return min(max(val, rng[0]), rng[1])

# class TrafficEnv(Env):
#     '''
#     Traffic environment for traffic simulations. Takes a (directed) Graph object representing
#     road structure, moves agents along roads with each tick. That is, agents are "at"
#     intersections between ticks, and during the tick the agent is moved along the direction to
#     the next intersection.
#     '''
#     def __init__(self, roads: graph.Graph, cars: int, traffic_lights: int):
#         self.roads = roads

#         # create initial entities
#         for _ in range(cars): self.create('car')
#         for _ in range(traffic_lights): self.create('traffic_light')

#     def tick(self, action):
#         return self.state, None
