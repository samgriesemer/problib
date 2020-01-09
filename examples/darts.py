from .probability.distributions import Uniform
import numpy as np
import matplotlib.pyplot as plt
import time

R = 4
S = 1000000
U = Uniform(-R, R)

scores = []
for i in range(S):
    r = R
    score = 1
    while True:
        x, y = list(U.sample(2))
        norm = np.sqrt(x**2+y**2)
        if norm > r: break

        #time.sleep(1)
        #print('norm: {}'.format(norm))
        #print('r: {}'.format(r))

        r = np.sqrt(r**2-norm**2)
        score += 1
    scores.append(score)
print('Mean: {}'.format(np.mean(scores)))
print('Std dev: {}'.format(np.std(scores)))

