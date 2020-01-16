from ..engine import physics
from ...algo import graph
from . import space

class Env():
    '''
    Base environment class outlining simple tick and draw methods. All
    environments to be used inside a Gym or interacting with Agent types
    should inherit this interface. Need to provide a state and action space
    for defining valid actions and return states.

    Environments encompass all of the components necessary for action execution.
    Environments should be independent of the agents interacting with it; it is not
    concerned with how the agents make decisions but only how to execute submitted
    actions against ingrained constraints. 
    '''
    def __init__(self, state_space=None, action_space=None, entity_space=None, engine=None):
        # define spaces
        self.state_space  = state_space
        self.action_space = action_space
        self.entity_space = entity_space
        self.engine = engine

        # define basic management variables
        self.state = {}
        self.entities = {}

    def tick(self, action):
        '''
        Execute given agent action and perform single environment tick. Can be
        dynamic (e.g. call on physics engine) or static. Agent actions are subject
        to internally defined constraints (i.e. agent desires may not be executed
        exactly as intended due to realistic limitations). Resulting environment state
        is returned
        '''
        return self.state, 0, False

    def draw(self):
        '''
        Return view of internal environment state. This method is currently
        undefined as there is no standard view protocol. This may ultimately
        be removed considering visualization is left to client side Javascript
        objects. Could be used to render pixels for purely vision-based envs.
        '''
        pass

    def create(self, type):
        '''
        Create an entity of the specified. Used to populate the environment with
        objects necessary to the simulation. This method is provided for working with
        environments that need to be dynamic and update the entities within while the
        simulation is running.

        :type: An entity from the entity space
        '''
        pass

class RandomEnv(Env):
    def tick(self, action):
        return self.state_space.sample(), 

class SingleAgentEnv(Env):
    pass

class MultiAgentEnv(Env):
    pass

class StaticContext(Env):
    '''
    Official environment for defining a static state. To be used as a simple Env
    object inheriting necessary interface when only some context is needed. Does
    nothing to the base class.
    '''
    pass

class Grid(Env):
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
        self.engine = physics.Engine(entities)

    @classmethod
    def random(cls, n, width, height, vxrng, vyrng, axrng, ayrng):
        '''
        Alternate constructor for random creation of entities
        NOTE: entities currently removed from constructor and
        dependent on agent registry
        '''
        entities = []
        for _ in range(n):
            e = physics.Entity.random((0, width), (0, height), vxrng, vyrng)
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
        entity = physics.Entity.random((0,self.width), (0,self.height), \
                                       self.vxrng, self.vyrng, self.axrng, self.ayrng)
        self.engine.add(entity)
        # return entity.id
        return id(entity)

    def remove_entity(self, eid):
        self.engine.remove(eid)

    def clip(self, val, rng):
        return min(max(val, rng[0]), rng[1])

class TrafficEnv(Env):
    '''
    Traffic environment for traffic simulations. Takes a (directed) Graph object representing
    road structure, moves agents along roads with each tick. That is, agents are "at"
    intersections between ticks, and during the tick the agent is moved along the direction to
    the next intersection.
    '''
    def __init__(self, roads: graph.Graph, cars: int, traffic_lights: int):
        self.roads = roads

        # create initial entities
        for _ in range(cars): self.create('car')
        for _ in range(traffic_lights): self.create('traffic_light')

    def tick(self, action):
        return self.state, None
        