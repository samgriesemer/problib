from problib.sim import *

class MonopolyEnv(env.Env):
    '''
    **General Monopoly Environment**

    local static structure: 
        - board size: number of property spaces
        - player range: range of number of players

    local param. structure:
        - properties: list of monopoly properties, including name and cost

    global static structure:
        - entity_map: Player, agent subclass for players (the only front for
          decision processes)
        - action_space: 
    '''

    def __init__(self, options):
        opts = Opt({
            'board_size': 16,
            'player_range': [2, 8],
            'entity_map': {
                'player': Player
            },
            'action_space':

        opts.set_pattern({
            'board_size': '',
            'player_range': '',
            'entity_map': '',
            'action_space': ''
        })

        opts.update(options)

        super().__init__(opts)

            entity_map={
            'player': Player
        },)

class MonopolyEnv(env.Env):
    def __init__(self, properties):
        self.properties = properties

        # defaults
        self.board_size = 16
        self.player_range = [2, 8]

        super.__init__(
            action_space = space.Discrete([2,8]),
            entity_map = {
                'player': Player
            }
        )


class StandardMonopoly(MonopolyEnv):
    '''
    Standard Monopoly Environment

    Inherits general MonopolyEnv, moves `properties` to local static structure by
    fixing the standard property set.
    '''

class Player(entity.Entity):
    """Docstring for Property. """

    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

        
properties = [{'name': 'Boardwalk', 'cost': 1e6}]
mon = MonopolyEnv(properties, players=4)

mon.select('properties').data([
    {'name': 'Boardwalk', 'cost': 1e6},
]).enter()

#######

class MonopolyEnv(env.Env):
    def __init__(
        self,
        board_size=16,
        player_range=[2,8]
    ):
        self.board_size = board_size
        self.player_range = player_range


        super().__init__(
            action_space={},
            entity_map={
                'player': Player
            },
        )

