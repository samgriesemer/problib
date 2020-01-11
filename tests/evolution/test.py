# test api adventure
env = Env('grid')
gym = Gym(env, []) 
sim = GeneticAlgorithm(100, 15000, 0.66, candidate.AlphaString, {'length':26}, gym)

# sim responsible for creating individuals, adding them to the gym
from problib.simulation.gym import agent
from problib.simulation.gym import env
from problib.simulation.gym import gym
from problib.evolution.candidate import NeuralNetwork

tagent = agent.Agent()
tenv = env.Grid(100,100,[-1,1],[-1,1])
tgym = gym.PhysicsGym(tenv)
tgym.register_agent(tagent)
tgym.remove_agent(tagent)

nn = NeuralNetwork.random([6,5,4])
tgym.register_agent(nn)
nn3 = NeuralNetwork.random([6,5,4])
tgym.register_agent(nn3)
loop = tgym.run()
next(loop)