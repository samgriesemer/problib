import random

def single_point(parent1, parent2):
  child = parent1.genotype.copy()
  begin = random.randint(0, len(child) - 1)
  end = random.randint(0, len(child) - 1)
  start, stop = min(begin, end), max(begin, end)
  child[start:stop] = parent2.genotype[start:stop]
  return child
