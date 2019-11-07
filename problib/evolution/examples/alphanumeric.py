from .. import genetic
from .. import selection
from .. import crossover
from .. import mutation
from .. import candidate

from ...utils.generator import exhaust

def fitness(target):
  def wrapper(candidate):
    value = 0
    candidate = candidate.genotype
    for (i,c) in enumerate(candidate):
      value += (ord(c)-ord(target[i]))**2
    return -value
  return wrapper

def termination(target):
  def wrapper(population):
    return population[0].epigenesis() == target
  return wrapper

if __name__ == '__main__':
  target = 'abcdefghijklmnopqrstuvwxyz'
  sim = genetic.GeneticAlgorithm(100, 15000, 0.66, candidate.AlphaString, [26])
  sim.selection = selection.roulette
  sim.crossover = crossover.single_point
  sim.mutation = mutation.alterchar
  sim.fitness = fitness(target)
  sim.termination = termination(target)
  
  # run simulation
  print(exhaust(sim.run(), interval=500))
