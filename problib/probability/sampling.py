import math
import random

def sample(population, k=1):
    for i in range(k):
        r = math.floor(random.random()*len(population))
        yield population[r]
        population.pop(r)

def inverse_transform(inv_cdf):
    r = random.random()
    return inv_cdf(r)

#def discrete_inverse_transform(cdf):
#  '''general naive implementation'''
#  def inv(p):
#    x = 0
#    for i in range(x):
#      p +=  
    
def rejection_sampling(): pass
def importance_sampling(): pass
