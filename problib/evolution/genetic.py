from . import evolutionary

class GeneticAlgorithm(evolutionary.Evolutionary):
  '''
  Standard genetic algorithm (in a way, the genetic algo is
  itself an agent, taking states, maintaining internal representation,
  reacting and responding to the environment
  '''
  def run(self):
    # initialize population of canidates
    self.create_population()
    self.obs = self.gym.start()

    # begin generation loop
    for gen in range(self.num_generations):
      # rank individuals based on current fitness
      self.action = []
      self.population.sort(key=lambda x: self.fitness(x), reverse=True)

      # yield generation specific details
      top_candidate = self.population[0]
      bot_candidate = self.population[-1]
      yield {'generation'    : gen,
             'best_candidate': top_candidate.epigenesis(),
             'best_fitness'  : self.fitness(top_candidate),
             'worst_fitness' : self.fitness(bot_candidate)}

      # check termination condition
      if self.termination(self.population):
        return self.population[0]

      # execute actions and get new state
      if self.gym:
        self.obs = self.gym.step(self.action)

      # consider multiple offspring per generation
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
          # maintain gym agent registry
          if self.gym:
            self.gym.remove_agent(self.population[-1])
            self.gym.register_agent(child)

          # replace worst candidate with child
          self.population[-1] = child
