from ..engine import physics

class Env():
    '''
    Base environment class outlining simple tick and draw methods. All
    environments to be used inside a Gym or interacting with Agent types
    should inherit this interface. Need to provide a state and action space
    for defining valid actions and return states.
    '''
    def __init__(self):
        # define internal tracking variables
        self.state = None
        self.engine = None

        # define spaces
        #self.state_space  = space.State()
        #self.action_space = space.Action()

    def tick(self, action):
        '''
        Execute given agent action and perform single environment tick. Can be
        dynamic (e.g. call on physics engine) or static. Agent actions are subject
        to internally defined constraints (i.e. agent desires may not be executed
        exactly as intended due realistic limitations). Resulting environment state
        is returned.
        '''
        return self.state

    def draw(self):
        '''
        Return view of internal environment state. This method is currently
        undefined as there is no standard view protocol. This may ultimately
        be removed considering visualization is left to client side Javascript
        objects. Could be used to render pixels for purely vision-based envs.
        '''
        pass

class SingleAgentEnv(Env):
    pass

class MultiAgentEnv(Env):
    pass

class Grid(Env):
    '''
    Naive implementation, simple velocity and position
    updates on body of defined point objects. Action space
    includes all real number within velocity ranges, and the state
    is the current set of physics entities and their 2D positions.
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

    def tick(self, actions):
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

