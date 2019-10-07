import random

from probability import distribution

class Bernoulli(distribution.Distribution):
  def __init__(self, p):
    self.p = p

  def pdf(self, x):
    return self.p**x * (1-self.p)**(1-x)

  def cdf(self, x):
    return (1-self.p)**(1-int(x))

  def sample(self, n=1):
    for _ in range(n):
      yield 1 if random.random() < self.p else 0

