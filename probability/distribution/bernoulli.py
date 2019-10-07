class Bernoulli(Distribution):
  def __init__(self, p):
    self.p = p

  def sample(self, n=1):
    for _ in range(n):
      yield 1 if random.random() < self.p else 0