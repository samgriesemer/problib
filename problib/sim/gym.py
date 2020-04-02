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
    representation for given agent. Could reduce varying env/gym friction.

    Gym options allow for 
    - env: env object to wrap 
    - entity_agent_map: entity type to agent classes mostly for deciding
    how to wire up entities created by default
    - agent_entitiy_map: opposite of above
    - agents: initial set of agents, follows map rules if they apply, can
    be a dict mapping to entities
    - views: dict of agent type to view function
    '''
    def __init__(self, options):
        # set environment and record variables
        self.env = options['env']
        self.packet = {}

        # active agent registry, dict by {aid:agent}
        self.agents = {}

        # create internal agent-entity registry
        self.registry = {}

        # create views registry for agents {aid:view}
        self.views = options.get('views')

        # association maps, one for each index
        self.agent_entity_map = options.get('agent_entity_map')
        self.entity_agent_map = options.get('entity_agent_map')

        # create agent archive
        self.agent_history = []

        # create id generator
        chars = string.printable[:61]
        self.idgen = Product(chars, repeat=6).sample_without_replacement(-1)

        self.gen = 0

    def tick(self):
        action = {}
        self.gen += 1
        
        for aid, agent in self.agents.items():
            eid = self.registry.get(aid)
            state = self.packet['state']

            # simple check for agent in current state
            if eid not in state['entities']: continue
            entity = state['entities'][eid]

            # render agent view
            if type(entity) in self.views:
                subpacket = self.views[type(entity)](self.packet, aid, eid)

            action[eid] = agent.auto(subpacket)
        self.packet = self.env.tick(action)

    def start(self):
        '''
        Perform necessary initialization measures out of init.
        '''
        self.packet = self.env.packet

        # add agents for default entities; initial list will have any existin defaults
        # and none of them will exist in the gym yet
        for entity in self.packet['state']['entities']:
            if 'default' in self.entity_agent_map:
                agent = self.entity_agent_map['default']()
                self.register_agent(agent, 'default', eid)

    def run(self, gens=-1):
        self.start()
        while self.gen != gens:
            self.tick()
            yield {'gen'  : self.gen,
                   'state': self.state}

    def register_agent(self, agent, entity='random', eid=None):
        '''
        TODO: allow simple override, can specify agent already in gym
        along with new entity to assign it to
        '''
        # check if agent already in gym
        if agent.id in self.agents: return

        if entity is not None:
            # instance is provided, register directly
            #eid = self.env.create(entity)
            pass
        elif type(agent) in self.agent_entity_map:
            # exists a map behaviour, use it
            eclass = self.agent_entity_map[type(agent)]()
            #self.env.create(eclass)
        elif entity == 'default':
            # do not register any entities, do nothing
            pass
        else:
            # create default entity randomly?
            #eid = self.env.create('random')
            pass

        # otherwise assign id and add to
        # active and historical agent sets
        aid = 'a'+''.join(next(self.idgen))
        agent.id = aid
        self.agents[aid] = agent
        self.registry[aid] = eid
        self.agent_history.append((aid,agent))

    def remove_agent(self, agent):
        self.agents.pop(agent.id, None)
        self.env.remove_entity(self.registry[agent.id])
        self.registry.pop(agent.id)

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

        for aid, eid in self.registry.copy().items():
            if aid not in self.agents:
                self.env.remove_entity(eid)
                self.registry.pop(aid)
        self.fresh_state = False


class PhysicsGym(Gym):
    '''
    Extend standard Gym interface by adding physics entity-agent
    management. Overrides agent registry methods with additional
    entity updates propogated back to the env.
    '''
    def __init__(self, env, agents=[]):

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
