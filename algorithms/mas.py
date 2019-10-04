import numpy as np
import pulp
from collections import deque
from tqdm import tqdm
import time
from timeit import timeit

# input for assignment problem is matrix, rows as agents, 
# cols as objects, entries are values

def auction(matrix, epsilon):
  S = {} # initializpe assignment map
  n, m = matrix.shape # get number of agents (n), objects (m)
  prices = np.zeros(m) # initialize object prices
  agents = deque([i for i in range(n)]) # intitialize agent list

  # iterate until feasible assignment
  while len(S) < n:
    agent = agents.popleft()
    values = matrix[agent]
    utility = values - prices
    obj1, obj2 = np.argsort(-utility)[:2]
    b = utility[obj1] - utility[obj2] + epsilon
    if obj1 in S: agents.append(S[obj1])
    S[obj1] = agent
    prices[obj1] += b

  #return {agent: obj for obj, agent in S.items()}
  return S

def lp_auction(matrix, epsilon):
  n, m = matrix.shape # get number of agents (n), objects (m)
  prob = pulp.LpProblem("Auction", pulp.LpMaximize)
  assign_vars = np.array([[pulp.LpVariable(f'x_{i:0{len(str(i))}}_{j:0{len(str(j))}}', cat="Binary") for j in range(m)] for i in range(n)])

  # objective fucnction
  #prob += np.sum(np.multiply(matrix, assign_vars))
  vals = np.multiply(matrix, assign_vars).flatten()
  #prob += pulp.LpAffineExpression([(val,1) for val in vals])
  prob += pulp.lpSum(list(vals))

  # add agent constraints
  for i in range(n):
    #prob += np.sum(assign_vars[i,:]) <= 1
    #prob += pulp.LpAffineExpression([(val,1) for val in assign_vars[i,:]]) <= 1
    prob += pulp.lpSum(list(assign_vars[i,:])) <= 1

  # add object constraints
  for j in range(n):
    #prob += np.sum(assign_vars[:,j]) <= 1
    #prob += pulp.LpAffineExpression([(val,1) for val in assign_vars[:,j]]) <= 1
    prob += pulp.lpSum(list(assign_vars[:,j])) <= 1

  # solve lp problem
  prob.solve()
  #pulp.GLPK_CMD()
  #print(pulp.LpStatus[prob.status])
  return np.array(list(map(lambda x: x.varValue, prob.variables()))).reshape((n,m))

def assignment_generator(n, M):
  return np.random.randint(0, M-1, (n,n))

def experiment(trials, pow_range, M):
  exp_avg = []
  for i in range(*pow_range):
    n = 2**i
    print('Starting n={}\n'.format(n))
    trial_avg = 0
    for j in tqdm(range(trials)):
      prob = assignment_generator(n, M)
      assignment = auction(prob, 1/(2*n))
      objects = sorted(assignment.keys(), key=lambda x: assignment[x])
      trial_avg += np.mean(prob[np.arange(n), np.array(objects)])
    exp_avg.append(trial_avg/trials)
  return exp_avge

def time_experiment(trials, n, pow_range):
  auc_list = []
  lp_auc_list = []
  for i in range(*pow_range):
    M = 10**i
    prob = assignment_generator(n, M)
    auc_time = 0
    lp_auc_time = 0
    for j in tqdm(range(trials)):
      # regular auction algo
      start = time.process_time()
      auction(prob, 1/(2*n))
      end = time.process_time()
      auc_time += (end-start)

      # lp auction algo
      start = time.process_time()
      lp_auction(prob, 1/(2*n))
      end = time.process_time()
      lp_auc_time += (end-start)
    auc_list.append(auc_time/trials)
    lp_auc_list.append(lp_auc_time/trials)
  return auc_list, lp_auc_list
