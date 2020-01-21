import string
import copy

from ..combinatorics.counting import Product

class Gym():
    '''
    Implements standard communication protocol between agents and environments,
    serving as a wrapper for agent-environment boilerplate and book-keeping (e.g.
    agent-entity registry and mapping, state/reward/action propogation, etc).
    Works with any environment and agent(s) inheriting the standard Env and Agent
    interfaces. Also an easy way to record the lifecycle of agents and ID them for
    analysis after simulation. Takes the more general assumption and operates with
    full multi-agent capability. Of course, single agent environments are a subset
    of multi-agent ones and can be created under the same protocol (base does not
    implement any agent<->env registry, just internal id assignment). However, the
    base will still record the single agent's id, pass actions as a list, etc.

    NOTE: Environment is abstracted away from the client. For example, no params
    are taken for the tick method, meaning the client doesnt have to worry about
    passing in env states, actions, rewards, etc; this exchange occurs internally.

    Note also that local representation of env state is not automatically queried
    after agent modifications are made. This is to prevent unnecessary computation
    in the case the client expects to make a series of agent updates and needs access
    to new state immediately (otherwise the changes will be propogated through at the
    next tick). TODO: this functationality should be important and known, that newly
    created agents have the ability to act before the next state i.e. at the next tick,
    and will other be missing a round if not taken care of. This shouldn't be a problem
    inside Gym, however, as the agent is immediately added to the internal registry
    and will be asked for an action at the next gym tick (although measures may be in
    place to filter out those agents not represented by the state, it's simply a matter
    of choice for the implementing gym).

    TODO: address agent constancy, even for agents that have been removed from
    active storage but may exist in the history. Imagine a dormant agent in some
    external sim that is never deleted, but re-enters the spotlight after some time.
    Should the gym be responsible for tracking this type of long-term agent, or just
    those that remain across ticks (i.e. acting under the assumption that agents
    are removed after they leave the spotlight)? Could be easily solved by making the
    agent_history a dictionary, but there is more a semantic question than anything.

    Also consider using built-in id() function to prevent external interaction with
    the agent .id variable. Can simple store an internal mapping between id()s and
    internally generated ids. Considering the id() will remain unique for the object
    lifetime, it works well the desired system behavior BUT there remains the issue
    that another agent could pick up that id() when the old one is deleted. So this
    is fine dealing with dormant agents that were never deleted and still have the
    same id() (and would be recognized by the system), but introduces the problem
    of external clashes. However, since the gym maintains an agent history these
    id()s will likely be preserved correctly, and the mapping will hold both ways.
    This doesn't necessarily make anything better for us now, but it could reduce
    the external modification required to set agent ids.

    Consider how agent actions sync up with environment ticks. Should the agent
    control the immediate next tick, or should it observe the state that will be
    used to update the next state before actions are applied (i.e. just difference
    in whether actions are applied before or after tick updates).

    Consider something like a `agent_state(agent)` method for grabbing state
    representation for given agent. Could reducde varying env/gym friction.
    '''
    def __init__(self, env, agents=[]):
        # set environment and record variables
        self.env = env
        self.state = {}
        self.reward = {}

        # active agent registry, dict by {aid:agent}
        self.agents = {}

        # create agent archive
        self.agent_history = []

        # create id generator
        chars = string.printable[:61]
        self.idgen = Product(chars, repeat=6).sample_without_replacement(-1)

        # additional variables
        self.gen = 0

        # register any initial agents
        self.update_agents(agents)

    def tick(self):
        action = {}
        self.gen += 1
        
        # hot fix for adaptive agent registry, remove in future
        self.state = copy.deepcopy(self.env.state)

        for aid, agent in self.agents.items():
            action[aid] = agent.act(self.state, self.reward)
        self.state, self.reward = self.env.tick(action)

    def start(self):
        self.state = self.env.state

    def run(self, gens=-1):
        self.start()
        while self.gen != gens:
            self.tick()
            yield {'gen'  : self.gen,
                   'state': self.state}

    def register_agent(self, agent):
        # check if agent already in gym
        if agent.id in self.agents: return

        # otherwise assign id and add to
        # active and historical agent sets
        aid = 'a'+''.join(next(self.idgen))
        agent.id = aid
        self.agents[aid] = agent
        self.agent_history.append((aid,agent))

    def remove_agent(self, agent):
        self.agents.pop(agent.id, None)

    def update_agents(self, agents):
        '''
        Takes a list of agents to sets gym to have only those agents. This
        process is slightly more nuanced than setting the .agents variable;
        we need to track and maintain the same agent and internal id if an
        existing agent is passed as part of list to set. This is to ensure
        ID constancy and unique ID<->agent mapping throughout the lifetime
        of the gym. Note that this identification is based on the signature
        of the agent instance itself; that is, the gym will treat a copy of
        an existing agent as something different than the original.
        '''
        temp = {}
        for agent in agents:
            self.register_agent(agent)
            temp[agent.id] = agent
        self.agents = temp

    def agent_state(self, agent):
        return self.state[agent.id]

    def refresh_state(self):
        pass


class PhysicsGym(Gym):
    '''
    Extend standard Gym interface by adding physics entity-agent
    management. Overrides agent registry methods with additional
    entity updates propogated back to the env.
    '''
    def __init__(self, env, agents=[]):
        # create internal agent-entity registry
        self.registry = {}

        # agent change tracker
        self.fresh_state = False
        
        # perform standard gym initialization
        super().__init__(env, agents)

    def tick(self):
        '''
        Addressing problem of newly added agents not being represented
        in currently held state. For now iterate over eid's directly
        as opposed to all gym agents, i.e. only agents recognized by
        environment
        '''
        action = {}
        self.gen += 1

        # refresh internal state to match agent-entity changes
        self.refresh_state()

        for aid, agent in self.agents.items():
            eid = self.registry[aid]

            # simple check for agent in current state
            if eid not in self.state: continue

            action[eid] = agent.act(self.state[eid], None)
        self.state, self.reward = self.env.tick(action)
        self.fresh_state = True

    def register_agent(self, agent):
        # check if agent already in gym
        if agent.id in self.agents: return

        super().register_agent(agent)
        
        # create entity for agent
        eid = self.env.random_entity()

        # store entity-agent pair in registry
        self.registry[agent.id] = eid
        self.fresh_state = False

    def remove_agent(self, agent):
        super().remove_agent(agent)
        self.env.remove_entity(self.registry[agent.id])
        self.registry.pop(agent.id)
        self.fresh_state = False

    def update_agents(self, agents):
        '''
        act explicitly for now, could implement "update" pattern
        through env and into engine
        UPDATE: turned into decent solution, no longer mega slow
        list lookup. Still consider above remark
        '''
        super().update_agents(agents)
        for aid, eid in self.registry.copy().items():
            if aid not in self.agents:
                self.env.remove_entity(eid)
                self.registry.pop(aid)
        self.fresh_state = False

    def refresh_state(self):
        if not self.fresh_state:
            self.state = self.env.state
            self.fresh_state = True

    def agent_state(self, agent):
        eid = self.registry[agent.id]
        return self.state[eid] 
