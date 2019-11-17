def sigmoid(z):
  return 1/(1+np.exp(-z))

def s_prime(z):
  #return np.multiply(sigmoid(z), sigmoid(1.0-z))
  return np.multiply(z, (1.0-z))

