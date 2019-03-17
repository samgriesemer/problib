import math
import random

def sample(population, k):
  results = []
  for i in range(k):
    r = math.floor(random.random()*len(population))
    results.append(population[r])
    population.pop(r)
  return results