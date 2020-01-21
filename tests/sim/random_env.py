from problib.sim import env, space, entity

action_space = space.Discrete(['a','b','c'])
state_space = space.Discrete([1,2,3])
entity_space = space.Discrete([entity.Entity])

renv = env.RandomEnv(action_space, state_space, entity_space)