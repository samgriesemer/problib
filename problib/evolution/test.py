# test api adventure
env = Env('grid')
gym = Gym(env, []) 
sim = GeneticAlgorithm(100, 15000, 0.66, candidate.AlphaString, {'length':26}, gym)

# sim responsible for creating individuals, adding them to the gym
