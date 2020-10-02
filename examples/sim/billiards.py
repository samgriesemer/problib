from problib.sim import *

# base class definition
class Billiards(env.Env):
    def __init__(self, boundary):
        super().__init__(
            action_space={},
            entity_space={}
        )

        self.table = boundary

# relevant entities
class BilliardBall(entity.composite.Ball):
    pass

class PoolStick(entity.Entity):
    pass

# custom registry patterns
def std_8ball(func):
    pass

### CONCRETE ###
bld = Billiards([])

# ENTITY REGISTRY #
bld.append(std_8ball(lambda x: BilliardBall(*x)))
## OR ##
# here group is left out for implicit `BilliardBall` group
bld.pattern(std_8ball).enter(lambda x: BilliardBall(*x))
## OR ##
balls = std_8ball(lambda x: BilliardBall(*x))
bld.add_entities(balls, 'balls')

# INDEX REGISTRY #
# basic position index
bld.select('BilliardBall').add_index(lambda x,y: (x,y))
## OR ##
bld.add_index(lambda x,y: (x,y), 'BilliardBall')

# TOTAL REGISTRY #
bld.add({
    'balls': {
        'entities': [
            BilliardBall(0,0),
            BilliardBall(1,1),
            ...
        ],
        'indexes': [
            lambda x: x,
            ...
        ],
    },
    ...
})

# create gym
poolgym = gym.Gym(bld)
