import random

def roulette(population):
  rand = random.random()*random.random()
  rand = int(rand*len(population))
  return population[rand]
