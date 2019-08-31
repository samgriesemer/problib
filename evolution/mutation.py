import random

def mutation_decorator(mutate):
  def wrapper(candidate, rate):
    if random.random() < rate:
      mutate(candidate)
  return wrapper

@mutation_decorator
def bitflip(candidate):
  '''in-place flip bit in bit-array'''
  gene = candidate.genotype
  rand = random.randint(0, len(gene)-1)
  gene[rand] = str(int(gene[rand])^1)

@mutation_decorator
def alterchar(candidate):
  '''shift character up or down'''
  gene = candidate.genotype
  rand = random.randint(0, len(gene)-1)
  gene[rand] = chr(ord(gene[rand]) + random.choice([-1, 1]))