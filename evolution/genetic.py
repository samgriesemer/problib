from evolution import evolutionary

class GeneticAlgorithm(evolutionary.Evolutionary):

  def run(self):
    # initialize population of canidates
    self.create_population()

    # begin generation loop
    for gen in range(self.num_generations):
      # rank individuals based on current fitness
      self.population.sort(key=lambda x: self.fitness(x), reverse=True)

      print('Generation {}, best candidate: {}, fitness: {}'.format(gen, \
            self.population[0].epigenesis(), self.fitness(self.population[0])))

      # check termination condition
      if self.termination(self.population): 
        return self.population[0]

      # consider multiple offspring per generation
      self.num_offspring = 1
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
          self.population[-1] = child