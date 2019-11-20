import random

def single_point(parent1, parent2):
  child = parent1.genotype.copy()
  begin = random.randint(0, len(child) - 1)
  end = random.randint(0, len(child) - 1)
  start, stop = min(begin, end), max(begin, end)
  child[start:stop] = parent2.genotype[start:stop]
  return child

def multipoint(parent1, parent2):
  '''Generalizes single point crossover, could make redundant'''
  pass

def weight_slice(net1, net2):
  return net1