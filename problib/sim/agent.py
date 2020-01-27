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
    :reward:
    '''
    def __init__(self, action_space=None):
        '''NOTE: determine how much agent should be dealing with this vs letting the gym handle it'''
        # make agent aware of action space
        self.action_space = action_space

        # internal model, stores "internal agent state" 
        self.model = {}

        # current raw state from env (reconsider use of state for env and more internal agent vars)
        self.state = {}

        # current received reward from env
        self.reward = None

        # agent identifier
        self.id = None

    def observe(self, state):
        '''
        Interpret incoming global environment state. Serves as sensory input processing stage,
        which can be necessary in order for agents to properly understand and parse the exteneral
        environment signal.
        
        This method is by default called by the `act()` method before executing the policy action
        on the current agent state. This method is left to agents so that the logic behind individual
        agents' interpretations is abstracted away from the environment.
        '''
        pass

    def update(self):
        '''
        Perform internal model updates based on new states, rewards, and any other information used by
        the agent's internal model. This method is used primarily by model-based RL agents, explicitly
        defining the process by which the internal world model should be updated according to the new
        information. 

        This method is called by `act()` after receiving a new (state, reward) pair
        to allow the model to incorporate newly available information before its policy is queried.
        '''
        pass

    def act(self):
        '''
        Main entry point for state/reward processing and internal model updates.
        This is where the agent is presented with new external information from the
        environment (state), along with any observed rewards from past actions. 
        This method is responsible for setting internal state and reward variables
        and maintaining historical storage. Once internal variables are updated,
        `observe()` is called to interpret the state and `update()` is invoked to
        update the agent's internal model given the new information. A decision
        process is then invoked using avaiable information to return a selected
        action from the known action space.
        '''
        pass

    def auto(self, state, reward):
        # populate history tracking variables
        self.state_history.append(state)
        self.reward_history.append(reward)

        self.reward = reward
        self.state = self.observe(state)
        self.model = self.update()
        return self.act()


class Example(Agent):
    def observe(self, state):
        self.state = state

    def update(self):
        self.model = self.state

    def act(self);
        return self.action_space.sample()
