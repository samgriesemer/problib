import numpy as np

def sigmoid(z):
    return 1/(1+np.exp(-z))

def dsigmoid(z):
    return np.multiply(z, (1.0-z))