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

    :state_space: unaware of true state space
    :action_space: is theoretically aware of available actions
    :reward:
    '''
    def __init__(self, action_space=[]):
        '''NOTE: determine how much agent should be dealing with this vs letting the gym handle it'''
        # make agent aware of action space
        self.action_space = action_space

        # internal model, stores "internal agent state" 
        self.model = {}

        # current raw state from env (reconsider use of state for env and more internal agent vars)
        self.state = {}

        # internal interpretation of current env state
        self.obs = {}

        # current received reward from env
        self.reward = {}

        # historical storage
        self.state_history = []
        self.reward_history = []

        # agent identifier
        self.id = 0

    def observe(self):
        '''
        Interal method to be called by `act()` for interpretting incoming state.
        Can be static and simple store the incoming state, or perform some sort
        of sensory analysis on the state as many agents must do in order to properly
        understand and parse the environmental state (i.e. apply any internal attention
        mechanisms). Sets the agent's `obs` variable to this processed/interpretted state.
        '''
        # by default, observe the entire raw state
        self.obs = self.state 

    def update(self):
        '''
        Perform internal model updates based on current/historical states, rewards,
        and actions. Called by `act()` after receiving a new state, reward pair, and
        prior to the next generated action.
        '''
        pass

    def action(self):
        '''
        Test addition to model. Goal is be separate from main act entry point and
        remain consistent with other methods acting on internal params. Also allows
        subclasses to override this method completely, without worrying about
        anything other than the internal state available.
        TODO: evaluate if this method should remain.
        '''
        return self.obs

    def act(self, state, reward):
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
        # update internal representation
        self.state = state
        self.reward = reward
        self.state_history.append(state)
        self.reward_history.append(reward)

        # interpret env state
        self.observe()

        # update internal model
        self.update()

        # generate and return action
        return self.action()

        '''
        implement some decision process and return an action
        '''
        #return self.action_space.sample() 
