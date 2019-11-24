import string

from ..simulation.gym.agent import Agent
from ..combinatorics import counting
from ..ml import nn

class Candidate(Agent):
  '''
  Base candidate class for evolutionary algorithms
  NOTE: can always consider switching the constructor to
  by default take random attributes and yield a stochastic
  candidate. This might make sense if we are to strictly
  follow what is most commonly used. However, it's not
  obvious how to go from specified genotype into a constructor
  expecting parameters for random generation; this would certainly
  be more sloppy than the current simple entry point constructor.

  Want to separate candidate from agent. Candidates dont need to be 
  defined in the context of a gym evnironment. They just hold a genotype
  and inherit the basic functions seen in base

  UPDATE: candidates ARE agents. They NEED to be defined in the context
  of a gym environment, as there must be a way of evaluating the candidates
  in an objective manner. This environment can be completely static, but
  the point is that it provides context for evaluating fitness. Canddiates
  are to inherit the same methods as any agent, but have the additional
  `genotype` attribute which holds their internal representation in the
  context of a genetic algorithm process. 
  '''
  def __init__(self, genotype):
    super().__init__()
    self.genotype = genotype

  def __str__(self):
    return self.epigenesis()

  @classmethod
  def random(cls, genotype):
    '''
    Alternate constructor for random candidate construction,
    to be implemented by subclassing type
    '''
    pass

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

    :genotype: list (mutable)
    :phenotype: conversion to string
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

class NeuralNetwork(Candidate):
  '''
  NeuralNetwork candidate object for use in
  neuroevolution implementations. This candidate
  has a phenotype represented by its observable
  actions resulting from inference, and a genotype
  represented by its underlying internal network
  structure and weights. All evolution operations (as
  usual) are performed on the genotype level.

  :phenotype: output from inference and resulting behavior
  :genotype: internal network structure and weight values
  '''
  def __init__(self, genotype):
    '''
    Genotype expected to be of the form of `.weights`
    attribute from the NeuralNetwork class (i.e. a list
    of NumPy arrays)
    THIS METHOD CURRENTLY NOT NEEDED
    '''
    self.genotype = genotype
    self.time_alive = 0

  @classmethod
  def random(cls, layers, rng=1):
    '''
    Take layers structure as input, instantiate neural
    network with given layers, set random weights according
    to [-rng, +rng]

    :layers: list of network layer size
    :rng: weights generated from [-rng, +rng]
    '''
    net = nn.NeuralNetwork(layers, epsilon=rng)
    return cls(net.weights)

  def epigenesis(self):
    '''
    Convert from network structure to observable actions
    via inference on live neural network architecture using
    genotype weights. This process requires a data point on
    which to evaluate the network

    TODO: consider how this is being done; should a nn object
    be kept in memory at all times and modifications be made
    directly to its weights so come inference time everything is
    ready to go? This seems a little bulky but may end up being
    more efficient. Initializing a network each time from weights
    though has a tiny overhead; it just sets the nn object's weights
    and no additional computation is needed.
    Also how are we going to pass the incoming data to the network
    for the actual inference procedure? Should the data be set to
    the network itself, passed to the function, or set under the
    candidate object?
    '''
    net = nn.NeuralNetwork.from_weights(self.genotype)
    return net

  def act(self, obs):
    net = self.epigenesis()
    data = [x[prop] for prop in ['px','py','vx','vy','ax','ay']]
    return net.predict(np.array(data))
