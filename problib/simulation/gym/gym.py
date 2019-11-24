import string

from ...combinatorics.counting import Product

class Gym():
    '''
    Implements standard communication protocol between agents and environments,
    serving as a wrapper for agent-environment boilerplate and book-keeping (e.g.
    agent-entity registry and mapping, state/reward/action propogation, etc).
    Works with any environment and agent(s) inheriting the standard Env and Agent
    interfaces. Also an easy way to record the lifecycle of agents and ID them for
    analysis after simulation. Takes the more general assumption and operates with
    full multi-agent capability. Of course, single agent environments are a subset
    of mulit-agent ones and can be created under the same protocol (base does not
    implement any agent<->env registry, just internal id assignment). However, the
    base will still record the single agent's id, pass actions as a list, etc.

    NOTE: Environment is abstracted away from the client. For example, no params
    are taken for the tick method, meaning the client doesnt have to worry about
    passing in env states, actions, rewards, etc; this exchange occurs internally.

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
        self.idgen = Product(chars, repeat=4).sample_without_replacement()

        # register any initial agents
        self.update_agents(agents)

    def tick(self):
        action = {}
        for aid, agent in self.agents.items():
            action[aid] = agent.act(self.state, self.reward)
        self.state, self.reward = self.env.tick(action)

    def run(self, gens=-1):
        gen = 0
        self.state = self.env.start()
        while gen != gens:
            self.tick()
            yield {'gen':gen}
            gen += 1

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

class PhysicsGym(Gym):
    '''
    Extend standard Gym interface by adding physics entity-agent
    management. Overrides agent registry methods with additional
    entity updates propogated back to the env.
    '''
    def __init__(self, env, agents=[]):
        # create internal agent-entity registry
        self.registry = {}
        
        # perform standard gym initialization
        super().__init__(env, agents)

    def register_agent(self, agent):
        super().register_agent(agent)
        
        # create entity for agent
        eid = self.env.random_entity()

        # store entity-agent pair in registry
        self.registry[agent.id] = eid

    def remove_agent(self, agent):
        super().remove_agent(agent)
        self.env.remove_entity(self.registry[aid])
        self.registry.pop(aid)

    def update_agents(self, agents):
        '''
        act explicitly for now, could implement "update" pattern
        through env and into engine
        '''
        super().update_agents(agents)
        for aid in self.registry.keys():
            if aid not in agents:
                self.env.remove_entity(self.registry[aid])
                self.registry.pop(aid)
