from combinatorics import counting

class Candidate:
  '''Base candidate class for evolutionary algorithms'''
  def __init__(self, **kwargs):
    create(**kwargs)

  @classmethod
  def from_genotype(cls, genotype):
    self.gen

  def epigenesis(self):
    return self.genotype

  def create(self):
    raise NotImplementedError

class AlphaString(Candidate):
  '''Candidate child for genetic string'''
  def create(self, length, alphabet):
    gene = counting.Product(*[alphabet]*length)
    self.genotype = gene.sample()