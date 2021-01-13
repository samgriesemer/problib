'''
Entire problib setup pipeline
'''

# 1. IMPORTS

# 2. ENTITY DEFS

# 3. ENV SETUP

## (OPTIONAL) ENGINE SPEC
### GLOBAL PARAMETRIC STRUCTURE
### GLOBAL DEFAULT STRUCTURE
### LOCAL PARAMETRIC STRUCTURE
### LOCAL DEFAULT STRUCTURE

## ENGINE INITIALIZATION
### STATE SPACE
### ACTION SPACE
### ENTITY SPACE

### Fixed structure
### Entities and groups
### Indexes

# 4. GYM SETUP

class A(Entity):
	pass

class B(Entity):
	pass

class a(A):
	pass

class Example(Env):
    def __init__(self, param1, ..., paramN, **kwargs):
        self.param1 = param1
        ...
        self.paramN = paramN

        super.__init__(
            spec={
                'A': {
                    'type': A,
                    'action_space': space.Discrete(A)
                },
                'B': {
                    'type': B,
                    'action_space': space.Discrete(B)
                },
                'Bsub': {
                    'type': B,
                    'action_space': space.Discrete(B),
                    'params': ['b']
                }
            }
        )
        # OR #
        super.__init__(
            spec={
                'A':  (A, space.Discrete(A)),
                'B':  (B, space.Discrete(B)),
                'Bs': (B, space.Discrete(B), ['b']),
                '<group>': (<type>, <action_space>, <param_func>)
            }
        )


class APolicy(Policy):
	pass

class BPolicy(Policy):
	pass

ex = Example(p1, ..., pN, pmap={
    'A': (APolicy, ),
    'B': (BPolicy, view, []),
    'group': (BPolicy, view)
}, index={
    'idx': (idx, ['A', 'group'])
})

ex.add('A', pararms={...})
ex.add('B', ..., group='group')
