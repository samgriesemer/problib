import random

def roulette(population):
  rand = random.random()*random.random()
  cand = rand*len(population)
  return population[cand]