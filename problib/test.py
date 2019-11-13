import random
import math

def binomial(n, k):
  nf  = math.factorial(n)
  kf  = math.factorial(k)
  nkf = math.factorial(n-k)
  return nf / (kf*nkf)

def cbf(k, n, p):
  res = 0
  for i in range(k,n+1):
    res += binomial(n,i) * p**i * (1-p)**(n-i)
  return res

# initialize default values
num_iters = 200000
M = 50
N = 5
R = 100

# initialize empty variables
count = 0
#test commit

# run experiment
for i in range(1, num_iters+1):
  # initialize empty loop variables
  user_nums   = []
  target_nums = []

  # generate random target numbers
  for j in range(M):
    target_nums.append(random.randint(1, R))

  # generate random user numbers
  for j in range(N):
    user_nums.append(random.randint(1, R))

  # check user numbers in target numbers
  all_match = True
  for unum in user_nums:
    match = False
    for tnum in target_nums:
      if (unum == tnum):
        match = True
        break
    if not match: all_match = False
  if all_match: count += 1

  # intermediate printing
  if (i % 1000 == 0):
    #with open('prob_log.txt', 'a') as f:
    print('Progress: {}%'.format(100*i/num_iters))
    print('Current percentage: {}%'.format(100*count/i))

# calculate probabilities
percentage  = count / num_iters
theoretical = cbf(1,M,1/R)**N

# print results
print('Observed percentage: {}%'.format(100*percentage))
print('theoretical percentage: {}%'.format(100*theoretical))
