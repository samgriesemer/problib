class Agent():
    '''
    Base agent class for defining individuals that interact with
    and react to dynamic environments. Agent is responsible for
    maintaining an internal state that represents their interpretation
    of the world since their most recent observation, can store a history
    of such observations, defines an action mechanism (often based on the
    most recent state and reward), and a reward history.

    All functions are internally based. That is, except for the `act()` entry
    point, agent methods are expected to act on the internally managed variables
    like .state, .obs, .reward, etc. Anytime one of these functions is invoked,
    it can expect these internally kept values contain the most recent, relevant
    information. This is primarily due to the fact that all methods are invoked
    only by the `act()` method, which is responsible for accepting external
    information and updating internal values correctly before calling such methods.

    :action_space: is theoretically aware of available actions
    '''
    def __init__(self, state_space=None, action_space=None):
        # define relevant spaces, note state space is the 
        self.state_space  = state_space  
        self.action_space = action_space

        # internal model, stores internal agent state 
        self.model = {}

        # current raw state from env (reconsider use of state for env and more
        # internal agent vars)
        self.state = {}

        # internal history tracking variables
        self.state_history = []
        self.reward_history = []
        self.action_history = []

        # agent identifier
        self.id = None

    def observe(self, state, reward):
        '''
        Interpret incoming environment state. The structure of this state should
        either be coordinated with the environment or known by the agent. This
        method is left to agents so that the possibly varying individual agents'
        interpretations are abstracted away from the environment.

        Semantically this method serves as a sensory input processing stage,
        whereby the agent filters out information it's incapable of perceiving
        (or rather focuses only that information it knows how to process) due to
        imposed sensory restraints. For example, as a human the external environment
        produces a spectrum of light, from which we are only able to perceive certain
        frequencies.

        This method is by default called by the `auto()` method before any other
        agent updates are made (i.e. before `update()` and `act()` are called).

        Note that the agent is left to process the reward in this method as well. 
        This can be done however the inheriting class needs: it can be set as its
        own instance variable, stored as an attribute of the state, or disregarded
        entirely. We decided against explicitly setting a reward instance variable
        in the interest of modularity. Besides, the reward is not inherent to the
        agent itself; rather, it's a piece of information like the state that is
        communicated by the environment.
        '''
        pass

    def update(self):
        '''
        Perform internal model updates based on new state, reward, and any other
        information used by the agent's internal model (e.g. state/reward histories).
        This method is used primarily by model-based RL agents, explicitly defining
        the process by which the internal world model should be updated according
        to the newly available information.

        This method is called by the `auto()` method following the observation phase,
        at which point the agent has interpreted the new environment state and made it
        available for further processing. This method also precedes the action mechanism,
        allowing the agent to make necessary model changes before deciding how to act.
        '''
        pass

    def act(self):
        '''
        Generate action according to currently available internal information.
        This primarily includes the `state` and `model` variables, but can include
        any other explicitly defined instance variables. Unlike the other internal
        agent methods, this method is not static and returns the decided upon action.
        Note this action should created from or verified by the action space before
        being returned.

        This method is called by the `auto()` method following the observation and
        model update phases during the response to external stimulus. All available
        information has been processed and necessary model changes have been made,
        implying the agent should have everything it needs to make a final decision.
        '''
        pass

    def auto(self, state, reward):
        '''
        Define basic boilerplate for processing external stimulus and generating
        a following action. This is the primary endpoint for interacting with the
        agent, and should be used by external APIs such as the gym.
        '''
        # pass new information to observation process
        self.observe(state, reward)

        # update internal model (if defined)
        self.update()

        # generate action from available state/model
        action = self.act()

        # populate history tracking variables
        self.state_history.append(state)
        self.reward_history.append(reward)
        self.action_history.append(action)

        return action


class Example(Agent):
    def observe(self, state):
        self.state = state

    def update(self):
        self.model = self.state

    def act(self):
        return self.action_space.sample()

