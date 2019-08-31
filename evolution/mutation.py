import random

def mutation_decorator(mutate):
  def wrapper(candidate, rate):
    if random.random() < rate:
      mutate(candidate)
  return wrapper

@mutation_decorator
def flip(candidate):
  '''in-place randomly flip bit in bit-array'''
  gene = candidate.genotype
  rand = random.randint(0, len(gene)-1)
  gene[rand] = str(int(gene[rand])^1)