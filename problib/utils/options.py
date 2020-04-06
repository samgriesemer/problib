class Opt(dict):
    '''
    TODO: may want to be able to set values using standard dict API, so would have
    to redirect options set to the value dict

    TODO: could maybe throw specialized errors for patterns like require, but a key error
    will be thrown either way, which might be good enough

    Default pattern value is 'optional', as it seems to make the least assumptions
    about the nature of the parameter. When the base has some set values, but no pattern
    is given, we simply recover the default `update` behaviour of standard dicts. Here we
    iterate over the target keys, and if the key has no pattern, we set it directly to the
    base. This takes care of both keys that are in the base but we've left them to be taken
    care of optionally by default, and any other keys unknown to both the base and to
    patterns. The subset of the target keys without a pattern is the only group of unprocessed
    keys at that point in time.

    Note that dicts can use their `update` method on an Opt object, and of course vice versa.
    There is not point in using an Opt object if no pattern is specified, as all patterns
    not specified are assumed to be optional, which is exactly what regular dicts do.

    Why is "ignore" needed? If you don't want your defaults changed, why not just leave them
    out? Well this is a valid point, but in the case you are using the Opt object to set your
    class attributes, there are some you want to ensure _dont_ get set (which will overwrite
    your defaults you may have set outside the Opt object).

    Permission options include:
    - require: require provided dict specifies key, no base value needed
    - optional: key is optional in provided dict, will be used instad of any base values
    - merge: merge provided values with base values in expectable way
    - ignore: ignore provided values under this key in preference for base (if defined, doesn't need to be)
    '''
    def __init__(self, d):
        super().__init__(**d)

    def set_pattern(self, pattern):
        self.pattern = pattern

    def update(self, target):
        '''
        Main purpose of this class. Update base values with target values according to the
        permissions set.
        '''
        # execute update pattern
        for key, pattern in self.pattern.items():
            if pattern == 'require':
                self[key] = target[key]
            elif pattern == 'optional':
                self[key] = target.get(key, self.get(key, None))
            elif pattern == 'merge':
                self[key] = self.merge(self.get(key), target.get(key))

        # add key-value pairs that don't have a pattern, but may or may not already have
        # an entry in base. All keys with a pattern have already been processed (if they've
        # been ignored, and there wasn't an entry in base, then that key doesn't have a
        # representative in the base, but this is intentional
        for key, value in target.items():
            if self.pattern.get(key) is None:
                self[key] = value

    def merge(self, val1, val2):
        if val1 is None and val2 is None:
            raise Exception('no values provided to merge')

        if val1 is None: return val2
        if val2 is None: return val1

        if type(val1) != type(val2):
            raise Exception('mismatching types on merge')

        if type(val1) == dict:
            return {**val1, **val2}
        else:
            return val1 + val2

