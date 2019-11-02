import random
import math

from ..combinatorics.counting import Combination

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
    '''return cdf^{-1}(p) = [Pr(x <= X) == p]'''
    pass

  def sample(self, n):
    '''n: number of samples'''
    pass

  '''common moments'''
  def mean(self):
    '''distribution mean'''
    pass

  def variance(self):
    '''distribution variance'''
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

  def mean(self):
    return self.p

  def variance(self):
    return self.p*(1-self.p) 

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

  def mean(self):
    return self.n*self.p

  def variance(self):
    return self.n* self.p*(1-self.p) 

class Exponential: pass

class Normal: pass

class Poisson:
  def __init__(self, lmda):
    self.lmda = lmda  

  def pdf(self, k):
    return self.lmda**k*math.e**(-self.lmda)/math.factorial(k)

  def cdf(self, x):
    pass

  def quantile(self, x):
    pass

  def sample(self, n):
    for _ in range(n):
      yield None

  def mean(self):
    return self.lmda

  def variance(self):
    return self.lmda

class Uniform:
  def __init__(self, a, b):
    self.a = a
    self.b = b
    self.lower = min(a,b)
    self.width = abs(a-b)

  def pdf(self, x):
    return 1 / self.width

  def cdf(self, x):
    return (x-self.lower) / self.width

  def quantile(self, x):
    pass

  def sample(self, n):
    for _ in range(n):
      yield random.random()*self.width+self.lower

  def mean(self):
    return (self.a+self.b)/2

  def variance(self):
    return self.p*(1-self.p) 
