from . import evolutionary

class GeneticAlgorithm(evolutionary.Evolutionary):
  '''Standard genetic algorithm'''
  def run(self):
    # initialize population of canidates
    self.create_population()
    new_canidates = self.population
    old_canidates = []

    # begin generation loop
    for gen in range(self.num_generations):
      # rank individuals based on current fitness
      self.population.sort(key=lambda x: self.fitness(x), reverse=True)

      # yield generation specific details
      top_candidate = self.population[0]
      bot_candidate = self.population[-1]
      yield {'generation'    : gen,
             'new_canidates' : new_canidates,
             'old_canidates' : old_canidates,
             #'best_candidate': top_candidate.epigenesis(),
             'best_fitness'  : self.fitness(top_candidate),
             'worst_fitness' : self.fitness(bot_candidate)}

      # check termination condition
      if self.termination(self.population): 
        return self.population[0]

      # consider multiple offspring per generation
      new_canidates = []
      old_canidates = []
      for _ in range(self.num_offspring):
        # stochastically select parent candidates
        parent1 = self.selection(self.population)
        parent2 = self.selection(self.population)

        # create child candidate via crossover
        child_genotype = self.crossover(parent1, parent2)
        child = self.candidate(child_genotype)

        # perform (possible) mutations on child
        self.mutation(child, self.mutation_rate)

        # add child to population if suitable
        if self.fitness(child) > self.fitness(self.population[-1]):
          new_canidates.append(child)
          old_canidates.append(population[-1])
          self.population[-1] = child
