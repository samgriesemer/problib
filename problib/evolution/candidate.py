from ..combinatorics import counting
import string

class Candidate:
  '''Base candidate class for evolutionary algorithms'''
  def __init__(self, genotype):
    #create(**kwargs)
    self.genotype = genotype

  def __str__(self):
    return self.epigenesis()

  @classmethod
  def random(cls, genotype):
    self.genotype = genotype

  def epigenesis(self):
    '''Process of turning genotype into phenotype'''
    return self.genotype

class AlphaString(Candidate):
  '''Candidate child for genetic string'''
  @classmethod
  def random(cls, length, alphabet=string.printable):
    '''
    Create random AlphaString

    alphastr = AlphaString.random(length)
    alphastr = AlphaString.random(length, 'abc')

    genotype: list (mutable)
    phenotype: conversion to string
    '''
    gene = counting.Product(*[alphabet]*length)
    gene = list(next(gene.sample()))
    return cls(gene)

  def epigenesis(self):
    return ''.join(self.genotype)

class BitString(AlphaString):
  '''Candidate child for genetic string'''
  @classmethod
  def random(cls, length):
    return super().random(length, '01')
