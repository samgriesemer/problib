from .. import genetic
from .. import selection
from .. import crossover
from .. import mutation
from .. import candidate
from ...simulation.gym import env
from ...simulation.gym import gym
from ...utils.generator import exhaust
from ...combinatorics import counting

import random
import copy
import numpy as np
from sklearn.gaussian_process import kernels, GaussianProcessRegressor

class KernelGenetic(genetic.GeneticAlgorithm):
    def fitness(self, candidate):
        data = self.gym.state['data']
        kernel = candidate.epigenesis()
        gp = GaussianProcessRegressor(kernel=kernel, alpha=0.001, normalize_y=False)
        try: 
            gp = gp.fit(*data)
        except np.linalg.linalg.LinAlgError:
            return -1e10
        return gp.log_marginal_likelihood()
    
    def termination(self, population):
        return False

    @mutation.class_mutation_decorator
    def mutation(self, candidate, size_rate, big_rate, kernel_rate):
        '''
        Mutates the kernel by either changing its size (adding or 
        removing a kernel), or modifies an existing kernel or operator

        :size_rate: probability of changing size (1-size_rate is probability
            of in-place modification)
        :kernel_rate: if changing kernel in-place, the chance a kernel is changed
            over an operator
        '''
        kernels = self.gym.state['kernels']
        ops = self.gym.state['ops']
        cand_kernels = candidate.genotype['kernels']
        cand_ops = candidate.genotype['ops']
        k = random.randint(0, len(cand_kernels)-1) if len(cand_kernels) > 0 else -1
        o = random.randint(0, len(cand_ops)-1) if len(cand_ops) > 0 else -1
        newk = random.choice(kernels)
        newo = random.choice(ops)

        if random.random() < size_rate:
            # randomly mutate the candidates size
            if random.random() < big_rate:
                cand_kernels.insert(k, newk)
                cand_ops.insert(k, newo)
            else:
                if o == -1: return
                cand_kernels.pop(o)
                cand_ops.pop(o)
        else:
            # randomly mutate either a kernel or op
            if random.random() < kernel_rate:
                if k == -1: return
                cand_kernels[k] = newk
            else:
                if o == -1: return
                cand_ops[o] = newo

    def crossover(self, parent1, parent2):
        gene1 = parent1.genotype
        gene2 = parent2.genotype
        if len(gene1['ops']) >= len(gene2['ops']):
            maxg = gene1
            ming = gene2
        else: 
            maxg = gene2
            ming = gene1

        child = copy.deepcopy(maxg)
        begin = random.randint(0, len(ming['ops']))
        end   = random.randint(0, len(ming['ops']))
        shift = random.randint(0, len(maxg['ops'])-len(ming['ops']))
        start, stop = min(begin, end), max(begin, end)
        child['kernels'][shift+start:shift+stop] = ming['kernels'][start:stop]
        child['ops'][shift+start:shift+stop] = ming['ops'][start:stop]
        return child

class Kernel(candidate.Candidate):
    '''
    Kernel candidate class. Has a genotype that the individual
    kernels making up the candidate kernel, along with a list
    of operations that describe how those kernels are combined
    to produce the candidate as a whole. In other words, each Kernel
    candidate is a combination of one or more Scikit kernels using
    the operations of `+` or `*`.

    :genotype: {'kernels': [], 'ops': []}
    '''
    @classmethod
    def random(cls, kernels, ops, kernel_num=1):
        knum = random.randint(1, kernel_num)
        kprod = counting.Product(kernels, repeat=knum)
        oprod = counting.Product(ops, repeat=knum-1)
        genotype = {
            'kernels': list(next(kprod.sample())),
            'ops'    : list(next(oprod.sample()))
        }
        return cls(genotype)

    def epigenesis(self):
        '''
        Construct full kernel from internal genotype representation.
        Requires Sklearn kernels
        '''
        kstr = ''
        for i, op in enumerate(self.genotype['ops']):
            k = self.genotype['kernels'][i]
            kstr += (k + op)
        kstr += self.genotype['kernels'][-1]
        return eval(kstr)


# begin setup
if __name__ == '__main__':
    # establish canidate context
    state = {
        'data': [
            np.array([[ 2.5     ,  7.5     ],
                      [ 6.25    ,  3.75    ],
                      [-1.25    , 11.25    ],
                      [ 0.625   ,  5.625   ],
                      [ 8.125   , 13.125   ],
                      [ 4.375   ,  1.875   ],
                      [-3.125   ,  9.375   ],
                      [-2.1875  ,  4.6875  ],
                      [ 5.3125  , 12.1875  ],
                      [ 9.0625  ,  0.9375  ],
                      [ 1.5625  ,  8.4375  ],
                      [-0.3125  ,  2.8125  ],
                      [ 7.1875  , 10.3125  ],
                      [ 3.4375  ,  6.5625  ],
                      [-4.0625  , 14.0625  ],
                      [-3.59375 ,  7.03125 ],
                      [ 3.90625 , 14.53125 ],
                      [ 7.65625 ,  3.28125 ],
                      [ 0.15625 , 10.78125 ],
                      [ 2.03125 ,  1.40625 ],
                      [ 9.53125 ,  8.90625 ],
                      [ 5.78125 ,  5.15625 ],
                      [-1.71875 , 12.65625 ],
                      [-2.65625 ,  2.34375 ],
                      [ 4.84375 ,  9.84375 ],
                      [ 8.59375 ,  6.09375 ],
                      [ 1.09375 , 13.59375 ],
                      [-0.78125 ,  4.21875 ],
                      [ 6.71875 , 11.71875 ],
                      [ 2.96875 ,  0.46875 ],
                      [-4.53125 ,  7.96875 ],
                      [-4.296875,  3.984375]]),
            np.array([ 24.12996441,  26.62417122,  22.38348248,  18.11101127,
                       140.3274732 ,   6.95495174,   8.57972118,  33.73834462,
                       136.34953133,   2.58080756,  31.32165852,  32.80838305,
                       98.34760791,  21.127854  ,   4.47623958,  41.77178986,
                       166.3236985 ,  15.47349757,  44.75361137,   9.32021859,
                       40.64753379,  34.73673999,  21.11009416,  78.863836  ,
                       83.88052753,  21.42438676,  98.68064045,  26.4495125 ,
                       130.64996148,   4.32360504,  70.6075829 , 132.44958167])
        ],
        'ops': ['+','*'],
        'kernels': [
            'kernels.ConstantKernel()',
            '1*kernels.RBF()',
            '1*kernels.RationalQuadratic()',
            '1*kernels.ExpSineSquared()',
            '1*kernels.Matern()',
        ]
    }

    sgym = gym.Gym(env.StaticContext(state))

    params = {
        'population_size': 30,
        'num_generations': 15000,
        'mutation_params': {
            'rate'       : 0.5,
            'size_rate'  : 0.5,
            'big_rate'   : 0.5,
            'kernel_rate': 0.5
        },
        'candidate'      : Kernel,
        'cand_params'    : {
            'kernels'   : state['kernels'],
            'ops'       : state['ops'],
            'kernel_num': 1
        },
        'num_offspring'  : 3,
        'gym'            : sgym,
    }

    sim = KernelGenetic(**params)
    sim.selection = selection.roulette

    # run simulation
    exhaust(sim.run(), interval=5)
