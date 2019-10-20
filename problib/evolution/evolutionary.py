import random

class Evolutionary:
  '''Base evolutionary algorithm class'''
  def __init__(self, population_size, num_generations, mutation_rate, candidate, cand_params):
    self.population = []
    self.population_size = population_size
    self.num_generations = num_generations
    self.mutation_rate = mutation_rate
    self.candidate = candidate
    self.cand_params = cand_params

  def fitness(self, candidate):
    '''Fitness function for evaluating candidate quality'''
    raise NotImplementedError

  def selection(self, population):
    '''Method of parent selection for crossover'''
    raise NotImplementedError

  def crossover(self, parent1, parent2):
    '''Method of reproduction between candidates'''
    raise NotImplementedError

  def mutation(self, candidate):
    '''Method of random mutation in candidate'''
    raise NotImplementedError

  def termination(self, population):
    '''
    Termination condition for simulation
    By default, return False so that simulation
    runs for all generations
    '''
    return False

  def create_population(self):
    for _ in range(self.population_size):
      self.population.append(self.candidate.random(*self.cand_params))

  def run(self):
    raise NotImplementedError
