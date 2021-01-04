from problib.sim import *

# left-right-center game sim
class LRC(env.Env):
    """Docstring for LRC. """

    def __init__(self, players, arms=3):
        """LRC game constructor

        :players: number of players in the game
        :arms: TODO

        """
        .__init__(self)

        self._players = players
        self._arms = arms
        

