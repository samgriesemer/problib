from .. import genetic
from .. import selection
from .. import crossover
from .. import mutation
from .. import candidate

from problib.simulation.gym import env
from problib.simulation.gym import gym

from ...utils.generator import exhaust

# def fitness(target):
#   def wrapper(candidate):
#     value = 0
#     candidate = candidate.genotype
#     for (i,c) in enumerate(candidate):
#       value += (ord(c)-ord(target[i]))**2
#     return -value
#   return wrapper

# def termination(target):
#   def wrapper(population):
#     return population[0].epigenesis() == target
#   return wrapper

# if __name__ == '__main__':
#   target = 'abcdefghijklmnopqrstuvwxyz'
#   sim = genetic.GeneticAlgorithm(100, 15000, 0.66, candidate.AlphaString, {'length':26})
#   sim.selection = selection.roulette
#   sim.crossover = crossover.single_point
#   sim.mutation = mutation.alterchar
#   sim.fitness = fitness(target)
#   sim.termination = termination(target)
  
#   # run simulation
#   exhaust(sim.run(), interval=500)

class Alphanumeric(genetic.GeneticAlgorithm):
    def fitness(self, candidate):
        target = self.gym.state
        gene = candidate.genotype
        cost = 0
        for (i,c) in enumerate(gene):
          cost += (ord(c)-ord(target[i]))**2
        return -cost

    def termination(self, population):
        target = self.gym.state
        return population[0].epigenesis() == target

# begin setup
if __name__ == '__main__':
    # establish canidate context
    target = 'abcdefghijklmnopqrstuvwxyz'
    sgym = gym.Gym(env.StaticContext(target))

    params = {
        'population_size': 100,
        'num_generations': 15000,
        'mutation_params': {'rate':0.5},
        'candidate'      : candidate.AlphaString,
        'cand_params'    : {'length':26},
        'gym'            : sgym,
    }

    sim = Alphanumeric(**params)
    sim.selection = selection.roulette
    sim.crossover = crossover.single_point
    sim.mutation = mutation.alterchar

    # run simulation
    exhaust(sim.run(), interval=500)