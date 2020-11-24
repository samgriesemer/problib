import string
import copy

from ..combinatorics.counting import Product
from ..utils.options import Opt

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
    def __init__(self, env, agent_space):
        self.packet = {}

        # active agent registry, dict by {aid:agent}
        self.agents = {}

        # create internal agent-entity registry
        self.registry = {}

        # agent groups
        self.groups = {}

        # create views registry for agents {aid:view}, dynamically filled on creation
        self.views = {}

        # create agent archive
        self.agent_history = []

        # create id generator
        chars = string.printable[:61]
        self.idgen = Product(chars, repeat=6).sample_without_replacement(-1)

        self.gen = 0

    def tick(self):
        action = {}
        self.gen += 1
        
        state = self.packet['state']
        for aid, agent in self.agents.items():
            eid = self.registry[aid]

            # simple check for agent in current state
            if eid not in state['entities']: continue
            entity = state['entities'][eid]

            # render agent view
            #subpacket = self.views[aid](copy.deepcopy(self.packet), aid, eid)
            subpacket = self.views[aid](self.packet, aid, eid)
            action[eid] = agent.auto(subpacket)
        self.packet = self.env.tick(action)

    def start(self):
        '''
        Perform necessary initialization measures out of init.
        '''
        self.packet = self.env.packet

        # add agents for default entities; initial list will have any existin
        # defaults and none of them will exist in the gym yet
        for eid in self.packet['state']['entities']:
            if 'default' in self.entity_agent_map:
                agent_name = self.entity_agent_map['default']
                self.create(agent_name, {'eid':eid})
 
    def run(self, gens=-1):
        self.start()
        while self.gen != gens:
            self.tick()
            yield {
                'gen'  : self.gen,
                'state': [vars(e) for e in self.packet['state']['entities'].values()],
                'pos': self.packet['extra']['indexes']['pos']
            }

    def add(self, entities, groups=[]):
        '''
        Add entities to the environment, under an optional group. Function accepts either
        a list of objects, a dictionary of named groups, or a singleton entity. Checks to
        ensure the entity types are with the specified entity space.
        '''
        if type(entities) is list:
            for entity in entities:
                self._add(entity, groups)
        elif type(entities) is dict:
            for group, entities in entities.items():
                for entity in entities:
                    self._add(entity, groups)
        else:
            self._add(entities, groups)


    def create(self, agent_name, options={}):
        '''
        Create new agent

        TODO: allow simple override, can specify agent already in gym
        along with new entity to assign it to
        '''
        if agent_name not in self.agent_map:
            raise Exception('Entity not recognized by gym')

        # get defaults based on groups
        plist = []
        vlist = []
        elist = []
        eoptlist = []
        for group in options.get('groups', [])+['all', agent_name]:
            default = self.default_map.get(group, {})
            if default is not None:
                if default.get('view') is not None:
                    vlist.append(default['view'])
                if default.get('params') is not None:
                    plist.append(default['params'])
                if default.get('entity') is not None:
                    elist.append(default['entity'])
                if default.get('entity_opts') is not None:
                    eoptlist.append(default['entity_opts'])

        # if all params are the same, use that as default, else use {}
        params = {}
        if len(plist) > 0 and plist.count(plist[0]) == len(plist):
            params = plist[0]

        # use default views if all are same, otherwise set default as identity
        view = lambda s: s
        if len(vlist) > 0 and vlist.count(vlist[0]) == len(vlist):
            view = vlist[0]

        # if all params are the same, use that as default, else use {}
        entity = None
        if len(elist) > 0 and elist.count(elist[0]) == len(elist):
            entity = elist[0]

        # if all params are the same, use that as default, else use {}
        entity_opts = {}
        if len(eoptlist) > 0 and eoptlist.count(eoptlist[0]) == len(eoptlist):
            entity_opts = eoptlist[0]

        # set defaults and merge with user options
        opts = Opt({
            'params': params,
            'count': 1,
            'groups': ['all', agent_name],
            'view': view,
            'entity': entity,
            'entity_opts': entity_opts
        })

        opts.set_pattern({
            'params': 'merge',
            'groups': 'merge',
        })

        opts.update(options)
        
        # create agents 
        agent_class = self.agent_map[agent_name]
        for _ in range(opts['count']):
            agent = agent_class(**opts['params'])
            aid = agent_name+''.join(next(self.idgen))
            agent.id = aid
            self.agents[aid] = agent
            self.agent_history.append((aid,agent))

            # add agent to groups
            for group in opts['groups']:
                if group not in self.groups:
                    self.groups[group] = []
                self.groups[group].append(agent)

            # add view to view index
            self.views[aid] = opts['view']

            # create associated entity (if desired, kind of hacky? functionality to skip entity creation)
            if opts.get('eid') is not None:
                # skip creation, register directly
                self.registry[aid] = opts['eid']
            else:
                self.registry[aid] = self.env.create(opts['entity'], opts['entity_opts'])[0]

    def remove(self, agent):
        self.agents.pop(agent.id, None)
        self.env.remove_entity(self.registry[agent.id])
        self.registry.pop(agent.id)

    def update(self, agents, entity_group='all'):
        '''
        Takes a list of agents to sets gym to have only those agents. This
        process is slightly more nuanced than setting the .agents variable;
        we need to track and maintain the same agent and internal id if an
        existing agent is passed as part of list to set. This is to ensure
        ID constancy and unique ID<->agent mapping throughout the lifetime
        of the gym. Note that this identification is based on the signature
        of the agent instance itself; that is, the gym will treat a copy of
        an existing agent as something different than the original.

        Perform update pattern, recognizing the overlap between the given list
        of agents and those already registering, and actually registering those
        not currently in the system to new entities under the provided group.
        This provided group sets the boundary of the update set. This is roughly
        equivalent to an `enter()` and `remove()` application like in D3
        '''
        

        #temp = {}
        #for agent in agents:
            #self.register_agent(agent, {group)
            #temp[agent.id] = agent
        #self.agents = temp
#
        #for aid, eid in self.registry.copy().items():
            #if aid not in self.agents:
                #self.env.remove_entity(eid)
                #self.registry.pop(aid)
        #self.fresh_state = False


