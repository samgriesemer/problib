import random

from combinatorics.counting import Combination
from probability import distribution

class Binomial(distribution.Distribution):
  def __init__(self, n, p):
    self.n = n
    self.p = p

  def pdf(self, x):
    return Combination.nCk(self.n, x)*self.p**x*(1-self.p)**(n-x)

  def cdf(self, x):
    return (1-self.p)**(1-int(x))

  def sample(self, n=1):
    for _ in range(n):
      yield 1 if random.random() < self.p else 0
