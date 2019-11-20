from .. import genetic
from .. import selection
from .. import crossover
from .. import mutation
from .. import candidate

from ...simulation import gym
from ...utils.generator import exhaust

class GridNE(genetic.GeneticAlgorithm):
  '''Neuroevolution implementation'''
  def fitness(self, candidate):
    net = candidate.epigenesis()
    obs = self.obs[id(candidate)]
    res = net.predict(obs)
    return -(obs-res)**2

  def run(self):
    # initialize genetic process and gym environment
    self.gym = gym.Grid(100, 100, [-3,3], [-3,3])
    self.obs = self.gym.start()

    # main NE loop
    for gendata in super().run():
      action = []

      # update gym agents
      for candidate in gendata['new_candidates']:
        self.gym.register_agent(candidate)

      for candidate in gendata['old_candidates']:
        self.gym.remove_agent(candidate)

      # get current agent actions
      for candidate in self.population:
        aid = id(candidate)
        val = candidate.predict(self.obs[aid])
        action.append({'aid':aid, 'val':val})

      # send actions to gym
      self.obs = self.gym.step(action)

      # yield NE metadata and gym state
      yield {'gen':gendata, 'state':self.obs}

if __name__ == '__main__':
  sim = SimpleNE(100, 10000, 0.2, candidate.NeuralNetwork, {'layers':[6,5,4]})
  sim.selection = selection.roulette
  sim.crossover = crossover.weight_slice
  sim.mutation = mutation.alter_weight

  # consider if this is the best approach
  exhaust(sim.run(), interval=500)
