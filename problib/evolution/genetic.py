from . import evolutionary

class GeneticAlgorithm(evolutionary.Evolutionary):
    '''
    Standard genetic algorithm (in a way, the genetic algo is itself
    an agent, taking states, maintaining internal representation,
    reacting and responding to the environment
    '''
    def run(self):
        # initialize population of candidates
        self.create_population()
        self.gym.start()

        # begin generation loop
        for gen in range(self.num_generations):
            # execute actions and get new gym state
            self.gym.tick()

            # rank individuals based on current fitness
            self.population.sort(key=lambda x: self.fitness(x), reverse=True)

            # balance population size
            self.population = self.population[:self.population_size]

            # maintain gym agent registry
            self.gym.update_agents(self.population)
            self.gym.refresh_state()

            # yield generation specific details
            top_candidate = self.population[0]
            bot_candidate = self.population[-1]
            yield {'generation'    : gen,
                   'best_candidate': str(top_candidate.epigenesis()),
                   'best_fitness'  : self.fitness(top_candidate),
                   'worst_fitness' : self.fitness(bot_candidate),
                   'state'         : self.gym.state}

            # check termination condition
            if self.termination(self.population):
                return self.population[0]

            # consider multiple offspring per generation
            for _ in range(self.num_offspring):
                # stochastically select parent candidates
                parent1 = self.selection(self.population)
                parent2 = self.selection(self.population)

                # create child candidate via crossover
                child_genotype = self.crossover(parent1, parent2)
                child = self.candidate(child_genotype)

                # perform (possible) mutations on child
                self.mutation(child, **self.mutation_params)

                # add child to population, gym for next round eval
                self.population.append(child)
                self.gym.register_agent(child)
