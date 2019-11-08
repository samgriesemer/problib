from .. import genetic
from .. import selection
from .. import crossover
from .. import mutation
from .. import candidate

from ...utils.generator import exhaust

class OneMax(genetic.GeneticAlgorithm):
  
  def fitness(self, candidate):
    return sum([int(bit) for bit in candidate.genotype])

if __name__ == '__main__':
  sim = OneMax(100,10000,0.2,candidate.BitString,[200])
  sim.selection = selection.roulette
  sim.crossover = crossover.single_point
  sim.mutation = mutation.bitflip

  # consider if this is the best approach
  print(exhaust(sim.run(), interval=500))
