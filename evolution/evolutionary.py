import random

class Evolutionary:
  '''Base evolutionary algorithm class'''
  def __init__(self, population_size, num_generations, candidate):
    self.population_size = population_size
    self.num_generations = num_generations
    self.candidate = candidate
    create_population()

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

  def create_population(self):
    self.population = []
    for _ in range(self.population_size):
      cand = self.candidate()
      self.population.append(cand.create())

  def run(self):
    raise NotImplementedError
