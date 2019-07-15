import random

class Evolutionary:
  '''Base evolutionary algorithm class'''
  def __init__(self, population_size, num_generations):
    self.population_size = population_size
    self.num_generations = num_generations

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

  def run(self):
    raise NotImplementedError
