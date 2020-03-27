class Entity:
    '''
    TODO: consider making this a numpy array based class for efficient updates
    Clear this out, should be abstract
    '''
    def __init__(self, px=0, py=0, vx=0, vy=0, ax=0, ay=0):
        # set position
        self.px = px
        self.py = py

        # set velocity
        self.vx = vx
        self.vy = vy

        # set acceleration
        self.ax = ax
        self.ay = ay

    @classmethod
    def random(cls, pxrng, pyrng, vxrng, vyrng, axrng=None, ayrng=None):
        '''
        Constructor overload, return randomly initialized
        point object within the specified position, velocty,
        and acceleration bounds
        '''
        px = random.uniform(*pxrng)
        py = random.uniform(*pyrng)
        vx = random.uniform(*vxrng)
        vy = random.uniform(*vyrng)
        ax = random.uniform(*axrng) if axrng else 0
        ay = random.uniform(*ayrng) if ayrng else 0

        return cls(px, py, vx, vy, ax, ay)

    def to_array(self):
        return np.array(list(self.__dict__.values()))

    def update(self):
        '''Update point physics'''
        # update position
        self.px += self.vx
        self.py += self.vy

        # update velocity
        self.vx += self.ax
        self.vy += self.ay

class Vector():
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

class State(Entity):
    def __init__(self, state=None):
        self.state = state

    def update(self, state):
        self.state = state

class Cell(Entity):
    def __init__(self, x, y, state={}):
        self.x = x
        self.y = y
        self.state = state

    def update(self, state):
        self.state = state
