from .. import genetic
from .. import selection
from .. import crossover
from .. import mutation
from .. import candidate

from problib.simulation.gym import env
from problib.simulation.gym import gym

from ...utils.generator import exhaust

class PhysicsNE(genetic.GeneticAlgorithm):
    '''Neuroevolution implementation'''
    def fitness(self, candidate):
        # assumes env has just been ticked
        state = self.gym.agent_state(candidate)

        # penalize agents for being far from center
        dx = self.gym.env.width/2 - state[0]
        dy = self.gym.env.height/2 - state[1]
        return -(dx**2 + dy**2)**(5/4)+candidate.time_alive**2

if __name__ == '__main__':
    grid = env.Grid(100, 100, [-3,3], [-3,3])
    sgym = gym.PhysicsGym(grid)

    params = {
        'population_size': 100,
        'num_generations': 150000,
        'mutation_params': {'rate':0.5, 'rng':0.5},
        'candidate'      : candidate.NeuralNetwork,
        'cand_params'    : {'layers':[6,5,4]},
        'gym'            : sgym,
    }

    sim = PhysicsNE(**params)
    sim.selection = selection.roulette
    sim.crossover = crossover.single_point
    sim.mutation = mutation.alter_weight

    # consider if this is the best approach
    exhaust(sim.run(), interval=200)