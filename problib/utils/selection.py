class Collection():
    """Docstring for Collection."""

    def __init__(self, objs=[], data=[]):
        self.objs = objs
        self._data = data
        self.state = []

        self.state_map = {}
        self.data_map = {}

        self.key = lambda d,i: i

    def data(self, data, key=None):
        self._data = data

        if key is not None:
            self.key = key

        for i, d in enumerate(self._data):
            idx = self.key(d, i)
            self.data_map[idx] = d

        for i, o in enumerate(self.state):
            idx = self.key(o['dat'], i)
            self.state_map[idx] = o['obj']

    def enter(self):
        '''
        check keys across data to state dicts; those keys in the data dict not in the
        state dict are in the enter selection
        '''
        enter = []
        for k, v in self.data_map.items():
            if k not in self.state_map:
                enter.append(v)

        return Collection(data=enter)

    def merge(self):
        return self

    def update(self):
        '''
        check keys across data to state dicts; those keys in both the state dict and the
        data dict are in the update selection
        '''
        return self

    def exit(self):
        '''
        check keys across data to state dicts; those keys in the state dict not in the
        data dict are in the exit selection
        '''
        exit = []
        for k, v in self.state_map.items():
            if k not in self.data_map:
                exit.append(v)

        return Collection(objs=exit)

    def append(self, func):
        '''
        Takes a function and applies it to each
        '''
        for i, d in enumerate(self._data):
            obj = func(d,i)
            self.objs.append(obj)
            self.state.append({'dat': d, 'obj': obj})

#.select('group')
#.data([])
#.enter().append()
#.update()
#.exit().remove()

#groups = {
#    'group': Collection([1,2,3,4,5])
#}
#
#col = groups['group']
#col.data([1,2,3])
#col.enter()
#col.exit()
