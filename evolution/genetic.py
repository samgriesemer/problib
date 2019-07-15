class GeneticAlgorithm(evolution.Evolutionary):

  def run():
    for _ in range(self.num_generations):
        population.sort(key=lambda x: fitness(x))