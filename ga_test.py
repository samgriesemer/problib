from evolution import *

# can use factory methods or subclassing

# heres an example of subclassing, similiar to DL libs
# can define you own functions write in the class or just set
# the appropriate class methods to the predefined methods, no
# need to define functions
class GeneticExample(genetic.GeneticAlgorithm):

  def fitness(candidate):
    return sum([int(bit) for bit in candidate.genotype])

  self.selection = selection.roulette
  self.crossover = crossover.single_point
  self.mutation = mutation

  # WHY NOT SET INPUT PARAMS HERE AS WELL? because we're trying to extend and define a
  # reusable class structure. In theory this could be instantiated multiple times in an 
  # experiment, using different population sizes, etc. So while technically possible, as
  # long as the user is setting the defining the characteristics which make up the class,
  # then there shouldn't be any issues.

###
# TODO: create and compare analogous "class factory" look for DEAP lib,
# see what is cleaner

toolbox.register("selection", selection.roulette)
toolbox.register("crossover", crossover.single_point)

###

params = {
  'population_size': 100,
  'num_generations': 10,
  'mutation_rate': 0.1,
  'candidate': candidate.AlphaString,
  'fitness': fitness,
  'selection': selection.roulette,
  'crossover': crossover.single_point,
}

ge = genetic.GeneticAlgorithm(**params)
ge.run()

###

params = {
  'population_size': 100,
  'num_generations': 10,
}

ge = genetic.GeneticAlgorithm(**params)
ge.candidate = candidate.AlphaString
ge.fitness = fitness
ge.selection = selection.roulette
ge.crossover = crossover.single_point
ge.run()
