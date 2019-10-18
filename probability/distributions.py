import random

from combinatorics.counting import Combination

class Distribution():
  def __init__(self, *params):
    self.params = params

  def pdf(self, x):
    '''return pdf(x) = density(x)'''
    pass

  def cdf(self, x):
    '''return cdf(x) = Pr(x <= X)'''
    pass

  def quantile(self, x):
    '''return cdf(x) = Pr(x <= X)'''
    pass

  def sample(self, n):
    '''n: number of samples'''
    pass

class Bernoulli(Distribution):
  def __init__(self, p):
    self.p = p

  def pdf(self, x):
    return self.p**x * (1-self.p)**(1-x)

  def cdf(self, x):
    return (1-self.p)**(1-int(x))

  def sample(self, n=1):
    for _ in range(n):
      yield 1 if random.random() < self.p else 0

class Binomial(Distribution):
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

class Exponential: pass

class Normal: pass

class Poisson: pass

class Uniform: pass
