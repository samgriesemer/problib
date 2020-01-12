class Space():
    '''
    Defines the notion of a gym space. Nothing more than a set
    with some additional structure. Used for outlining action
    spaces and state spaces.
    '''
    def __init__(self, states=[]):
        self.states = states

class StateSpace(Space):
    pass

class ActionSpace(Space):
    def __init__(self):
        pass
