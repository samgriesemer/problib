from math import factorial
import itertools
import random

class Product:
  '''Cartesian product of iterables'''
  def __init__(self, *data, repeat=1):
    '''
    TODO: address repeat variable in more efficient manner (i.e. dont repeat explicitly in memory)
    params: any number of iterables
    -> data: list of all passed iterables
    '''
    self.data = data*repeat

  def count(self):
    '''Compute number of elements in product'''
    count = 1
    for datum in self.data: count *= len(datum)
    return count

  def generate(self):
    '''Generate all Cartesian product set'''
    return itertools.product(*self.data)

  def sample(self, m=1):
    '''Randomly generate m samples from the product'''
    for _ in range(m):
      yield tuple(random.choice(exp) for exp in self.data)

  def sample_without_replacement(self, m=1):
    '''
    Randomly generate m unique samples from the product. If m
    greater than the number of possibles samples, return as
    many as possible.
    '''
    if m > self.count(): return None
    generated = set()
    while len(generated) < m:
      gtuple = next(self.sample(1))
      if gtuple not in generated:
        generated.add(gtuple)
        yield gtuple

class Permutation:
  '''Permutations of iterables'''
  def __init__(self, data):
    self.data = data
    self.n = len(data)

  @staticmethod
  def nPk(n, k):
    '''Compute nPk'''
    return int(factorial(n) / factorial(n-k))

  def count(self, k=None):
    '''Compute nPk expxlicitly on object data'''
    if k is None: k = self.n
    if k > self.n: return None
    return Permutation.nPk(self.n, k)
    
  def generate(self, k=None):
    '''Return generator over all permutations of object data'''
    if k is None: k = self.n
    return itertools.permutations(self.data, k)

  def generate_with_repetition(self, k=None):
    pass

  def sample(self, k=None, m=1):
    '''Return generator over m random samples from k-permutations of object data'''
    if k is None: k = self.n
    if k > self.n: return None
    for _ in range(m):
      yield tuple(random.sample(self.data, k))

  def sample_without_replacement(self, m=1):
    '''Randomly generate m unique permutations of object data'''
    if m > self.count(): return None
    generated = []
    while len(generated) < m:
      gtuple = next(self.sample(1))
      if gtuple not in generated:
        generated.append(gtuple)
        yield gtuple

  def duplicates(self, k=None):
    if k is None: k = self.n
    if k > self.n: return None
    return set(self.generate(k))

class Combination:
  '''Combinations of iterables'''
  def __init__(self, data):
    self.data = data
    self.n = len(data)

  @staticmethod
  def nCk(n, k):
    '''Compute nCk'''
    return int(factorial(n) / (factorial(k)*factorial(n-k)))

  def count(self, k=None):
    '''Compute nCk implicitly on object data'''
    if k is None: k = self.n
    if k > self.n: return None
    return Combination.nCk(self.n, k)
    
  def generate(self, k=None):
    '''Return generator over all combinations of object data'''
    if k is None: k = self.n
    return itertools.combinations(self.data, k)

  def generate_with_repetition(self, k=None):
    pass

  def sample(self, k=None, m=1):
    '''Return generator over m random samples from k-combinations of object data'''
    if k is None: k = self.n
    if k > self.n: return None
    for _ in range(m):
      indices = sorted(random.sample(range(self.n), k))
      yield tuple(self.data[i] for i in indices)

  def sample_without_replacement(self, m=1):
    '''Randomly generate m unique permutations of object data'''
    if m > self.count(): return None
    generated = []
    while len(generated) < m:
      gtuple = next(self.sample(1))
      if gtuple not in generated:
        generated.append(gtuple)
        yield gtuple

  def duplicates(self, k):
    if k is None: k = self.n
    if k > self.n: return None
    return set(self.generate(k))
