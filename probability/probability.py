import math
import random

def sample(population, k):
  results = []
  for i in range(k):
    r = math.floor(random.random()*len(population))
    results.append(population[r])
    population.pop(r)
  return results

def inverse_transform(inv_cdf):
  r = random.random()
  return inv_cdf(r)

def normal():
  def inv_normal(): pass

def exponential():
  pass
