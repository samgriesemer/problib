from math import factorial
import itertools

class Permutation:
  '''Permutations of iterables'''
  def __init__(self, data):
    self.data = data
    self.n = len(data)

  def count(self, k=None):
    if k is None: k = self.n
    if k > self.n: return None
    return int(factorial(self.n) / factorial(self.n-k))
    
  def generate(self, k=None):
    if k is None: k = self.n
    return itertools.permutations(self.data, k)

  def duplicates(self, k):
    pass

class Combination:
  '''Combinations of iterables'''
  def __init__(self, data):
    self.data = data
    self.n = len(data)

  def count(self, k=None):
    if k is None: k = self.n
    if k > self.n: return None
    return int(factorial(self.n) / (factorial(k)*factorial(self.n-k)))
    
  def generate(self, k=None):
    if k is None: k = self.n
    return itertools.combinations(self.data, k)

  def duplicates(self, k):
    pass