from evolution import genetic, selection, candidate

class GeneticExample(genetic.GeneticAlgorithm):

  def fitness(self, candidate):
    return sum(candidate)

  def selection(self, population):
    return selection.roulette(population)

  def crossover(self, parent1, parent2):

  def mutation(self):
    pass

class BitString(candidate.Candidate):

ge = GeneticExample(
    population_size=100,
    num_generations=10,
  )

ge.run()
