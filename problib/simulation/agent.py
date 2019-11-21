class Agent():
    '''
    Base agent class for defining individuals that interact with
    and react to dynamic environments. Agent is responsible for
    maintaining an internal state that represents their interpretation
    of the world since their most recent observation. 

    :state_space: unaware of true state space
    :action_space: is theoretically aware of available actions
    :reward:

    '''
    def __init__(self, action_space):
        self.state = {}
        self.state_history = []
        self.reward = {}
        self.reward_history
        self.id = 0

    def act(self, obs):
        '''Process by which the agent reacts to an observation'''
        raise NotImplementedError
