from ..probability import sampling

class Space():
    '''
    Defines the base space class, nothing more than a set
    with some additional structure. Used for outlining action
    spaces and state spaces.
    '''
    pass

class Discrete(Space):
    def __init__(self, states=[]):
        self.states = states

    def sample(self):
        return next(sampling.sample(self.states))

class Natural(Discrete):
    def __init__(self, n: int):
        super().__init__()
