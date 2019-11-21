from . import physics

class Gym():
  '''Base gym class, outlines simple tick and game loop methods'''
  def __init__(self):
    self.state = None

  def tick(self):
    '''Execute single gym tick'''
    pass

  def draw(self):
    '''Draw objects'''
    pass

  def loop(self, ticks):
    '''Return gym loop, generator over specified numer of ticks'''
    for _ in range(ticks):
      yield tick()

class MultiAgentGym(Gym):
  pass

class Grid(Gym):
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

    # create internal agent-entity registry
    self.registry = {}

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

  def register_agent(self, agent):
    # create entity for agent
    entity = self.random_entity()
    self.engine.add(entity)

    # store entity-agent pair in registry
    self.registry[id(agent)] = id(entity)

  def remove_agent(self, aid):
    self.engine.remove(self.registry[aid])
    self.registry.pop(aid)

  def random_entity(self):
    return physics.Entity.random((0,self.width), (0,self.height), \
                          self.vxrng, self.vyrng, self.axrng, self.ayrng)

  def clip(self, val, rng):
    return min(max(val, rng[0]), rng[1])

  @property
  def state(self):
    return {aid: self.engine.entities[eid].__dict__ for aid, eid in self.registry.items()}

  def start(self):
    return self.state

  def tick(self, actions):
    '''
    Handles action requests to engine entities, returns resulting
    state. Note for multi-agent systems, `action` is a list of actions
    to be performed by each agent at the current step

    :actions: list of actions in form {'action':<str>, 'aid':<int>, value:{'x':<int>, 'y':<int>}}
    ::known actions:: ['setv']
    '''
    # update entities and agents
    for action in actions:
      eid       = self.registry[action['aid']]
      entity    = self.engine.entities[eid]
      entity.vx = self.clip(action['val']['vx'], self.vxrng)
      entity.vy = self.clip(action['val']['vy'], self.vyrng)
      entity.ax = self.clip(action['val']['ax'], self.axrng)
      entity.ay = self.clip(action['val']['ay'], self.ayrng)

    # call physics tick
    self.engine.tick()
    return self.state

