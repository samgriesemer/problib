from evolution import *

# can use factory methods or subclassing

class GeneticExample(genetic.GeneticAlgorithm):

  def fitness(self, candidate):
    return sum(candidate)

  def selection(self, population):
    return selection.roulette(population)

  def crossover(self, parent1, parent2):
    return crossover.single_point(parent1, parent2)

  def mutation(self):
    pass



def fitness(candidate):
  return sum([int(bit) for bit in candidate.genotype])

params = {
  'population_size': 100,
  'num_generations': 10,
  'candidate': candidate.AlphaString,
  'fitness': fitness
  'selection': selection.roulette,
  'crossover': crossover.single_point
}

ge = genetic.GeneticAlgorithm(**params)
ge.run()
