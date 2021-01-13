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


#### existing billiards setup ####
bounds = [
    InfiniteWall((0, 0), (length, 0)),  # bottom side
    InfiniteWall((length, 0), (length, width)),  # right side
    InfiniteWall((length, width), (0, width)),  # top side
    InfiniteWall((0, width), (0, 0))  # left side
]
bld = billiards.Billiard(obstacles=bounds)

# add non-cue balls
for i in range(4):
    for j in range(i + 1):
        x = 0.75 * length + radius * sqrt(3) * i
        y = width / 2 + radius * (2 * j - i)
        bld.add_ball((x, y), (0, 0), radius)
        
# add cue ball (random position and velocity)
bld.add_ball((params[0], params[1]), (velx, vely), radius)


#### ideal billiards setup ####
class BilliardBall(Entity):
    def __init__(pos, vel, radius):
        self.pos = pos
        self.vel = vel
        self.radius = radius

class Billiard(Env):
    def __init__(self, bounds):
        self.bounds = bounds

        super.__init__(
            entity_space=BilliardBall,
            action_space=
        )

bld = Billiard(bounds)
bld.add(BilliardBall(x, y, vx, vy), 'cue')

balls = []
for i in range(4):
    for j in range(i + 1):
        x = 0.75 * length + radius * sqrt(3) * i
        y = width / 2 + radius * (2 * j - i)
        balls.append(BilliardBall((x, y), (0, 0), radius))

bld.add(balls, '8ball')

## new structure ##
### env comp ###
class BilliardBall(Entity):
    def __init__(pos, vel, radius):
        self.pos = pos
        self.vel = vel
        self.radius = radius

class Billiard(Env):
    def __init__(self, bounds):
        self.bounds = bounds

        super.__init__(
            entity_space=BilliardBall,
            action_space=
        )

        {
            'billiard_ball': {
                'type': BilliardBall,
                'action_space': space.Discrete(4),
                'params': lambda _: x
            }

        }

### client usage ###
bounds = [
    InfiniteWall((0, 0), (length, 0)),  # bottom side
    InfiniteWall((length, 0), (length, width)),  # right side
    InfiniteWall((length, width), (0, width)),  # top side
    InfiniteWall((0, width), (0, 0))  # left side
]

bld = Billiard(bounds=bounds)
bld.add('billiard_ball', (x, y, vx, vy), 'cue')

for i in range(4):
    for j in range(i + 1):
        x = 0.75 * length + radius * sqrt(3) * i
        y = width / 2 + radius * (2 * j - i)
        bld.add(BilliardBall((x, y), (0, 0), radius))
