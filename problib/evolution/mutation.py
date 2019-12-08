import random

def mutation_decorator(mutate):
  def wrapper(candidate, rate, **kwargs):
    if random.random() < rate:
      mutate(candidate, **kwargs)
  return wrapper

def class_mutation_decorator(mutate):
  def wrapper(self, candidate, rate, **kwargs):
    if random.random() < rate:
      mutate(self, candidate, **kwargs)
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

@mutation_decorator
def alter_weight(candidate, rng):
  '''
  Modify real numbers uniformly at random from a 
  NeuralNetwork weight vector
  '''
  weights = candidate.genotype
  layer = random.randint(0,len(weights)-1)
  shape = weights[layer].shape
  i, j = random.randint(0,shape[0]-1), random.randint(0,shape[1]-1)
  weights[layer][i,j] += random.uniform(-rng, rng)

  