from evolution import genetic
from evolution import selection
from evolution import crossover
from evolution import mutation
from evolution import candidate

class OneMax(genetic.GeneticAlgorithm):

  def fitness(self, candidate):
    return sum([int(bit) for bit in candidate.genotype])

#if __name__ == '__name__':
sim = OneMax(100,10000,0.2,candidate.BitString,[200])
sim.selection = selection.roulette
sim.crossover = crossover.single_point
sim.mutation = mutation.flip
sim.run()