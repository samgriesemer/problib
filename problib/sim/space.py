class Space():
    '''
    Defines the base space class, nothing more than a set
    with some additional structure. Used for outlining action
    spaces and state spaces.
    '''
    def __init__(self, states=[]):
        self.states = states

class Discrete(Space):
    def __init__(self, states=[]):
        self.states = states

class Natural(Discrete):
    def __init__(self, n: int):
        super().__init__()

s = Discrete(['a','b','c'])
n = discrete.Natural(5)