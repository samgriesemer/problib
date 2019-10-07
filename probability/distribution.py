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