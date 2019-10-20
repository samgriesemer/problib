import numpy as np
import cPickle as pickle
#from scipy import optimize

def unpickle(file):
    fo = open(file, 'rb')
    dict = pickle.load(fo)
    fo.close()
    return dict

def sigmoid(z):
  return 1/(1+np.exp(-z))

def s_prime(z):
  #return np.multiply(sigmoid(z), sigmoid(1.0-z))
  return np.multiply(z, (1.0-z))

def flatten(w):
  temp_w = w[0].flatten()
  for i in range(1,len(w)):
    temp_w = np.concatenate((temp_w, w[i].flatten()), axis=1)
  return temp_w

def binary_vect(labels):
  low, hi = np.min(labels), np.max(labels)
  zeros = np.zeros((len(labels), (hi-low)+1))
  for i in range(len(labels)):
    zeros[i,labels[i]-low] = 1
  return zeros

def init_weights(layers, epsilon):
  weights = []
  for i in range(len(layers)-1):
    w = np.random.rand(layers[i+1], layers[i]+1)
    w = w * 2*epsilon - epsilon
    weights.append(w)
  return weights

def fit(X, Y, w, l, predict=False):
  w_grad = ([(np.zeros(np.shape(w[i]))) 
        for i in range(len(w))])
  a = X
  A = []

  # forward propagate
  for i in range(len(w)):
    ones = np.reshape(np.ones(len(a)), (-1,1))
    a = np.append(ones, a, 1)
    A.append(a)
    z = np.dot(a, w[i].T)
    a = sigmoid(z)
  if predict: return a

  # backpropagate
  delta = a - Y
  w_grad[-1] += np.dot(delta.T, A[-1])
  for i in reversed(range(1, len(w))):
    delta = delta[:,1:] if i != len(w)-1 else delta
    delta = np.multiply(np.dot(delta, w[i]), s_prime(A[i]))
    w_grad[i-1] += np.dot(delta[:,1:].T, A[i-1])

  # regularization
  for i in range(len(w)):
    w_grad[i] /= len(X)
    w_grad[i][:,1:] += l * w[i][:,1:]
  return w_grad

def cost(X, Y, w, l):
  J = 0
  m = len(X)
  h = fit(X, Y, w, l, True)
  J += ((1.0/m)*(np.sum((np.multiply(-Y,np.log(h))-
      np.multiply((1-Y),np.log(1-h))).flatten())))
  for i in range(len(w)):
    J += np.sum(((l/(2.0*m))*np.power(w[i],2)).flatten())
  return J

def predict(X, Y, w, l):
  out = fit(X, Y, w, l, True)
  return np.reshape(np.argmax(out, 1), (-1,1))

def test_net(X, Y, w, l, labels, ex=False):
  guess = predict(X, Y, w, l)
  count = sum(guess == labels)
  print "Accuracy :", (float(count)/len(X)) * 100, "%"
  return guess

def shape_back(w, u_w):
  h = 0
  w_list = []
  for i in range(len(w)):
    m, n = np.shape(w[i])
    w_list.append(np.reshape(u_w[h:h+(m*n)],(m,n)))
    h += m * n
  return w_list

def file_dump(data, file):
  f = open(file, 'wb')
  pickle.dump(data, f)
  f.close()

# data #

mnist_data = unpickle('mnist.pkl')
labels = np.reshape(mnist_data[0][1], (-1,1))
X = mnist_data[0][0]

#data = unpickle('data_batch_1')
#labels = np.reshape(data['labels'], (-1,1))
#X = data['data']
Y = binary_vect(labels)
layers = [np.shape(X)[1],25,np.shape(Y)[1]]

CV_X = mnist_data[2][0]
CV_L = np.reshape(mnist_data[2][1], (-1,1))
CV_Y = binary_vect(CV_L)

# initialize parameters #

w = init_weights(layers, 0.2)
epochs = 30001
alpha = 0.4
l = 0.001
b = 500

# trim data #

beg = 0
end = len(X)
Xi = X[beg:end]
Yi = Y[beg:end]
labelsi = labels[beg:end]

# preset weights from file # 

#f = open('mnist_w9.p', 'rb')
#w = pickle.load(f)
#f.close()

# gradient descent #

c =  cost(X, Y, w, l)
cost_l = [c]
print "Initial Cost:", c
for i in range(epochs):

  # set batch indices
  ind = b * i % len(Xi)

  # initialize batches
  Xb = Xi[ind:ind+b]
  Yb = Yi[ind:ind+b]

  # feed batches into network
  grad = fit(Xb, Yb, w, l)
  for j in range(len(w)):
    w[j] -= alpha * grad[j]

  ivl = 500
  if i != 0 and i % ivl == 0: 
    test_net(Xi, Yi, w, l, labelsi)
    c = cost(X, Y, w, l)
    print "Cost:", round(c, 4)

    # dump cost into file
    cost_l.append(c)
    file_dump(cost_l, 'mnist_c.p')

    if len(cost_l) > 1:
      print "Cost diff:", cost_l[-2]-cost_l[-1]

  if i % 50 == 0: print "Batch:", i

  # dump weights into file
  file_dump(w, 'mnist_w9.p')

  # decrease learning rate
  #alpha -= alpha / (i + 2)
  #print alpha


# print examples #
print "\nCross Validation Stats:"
guess = test_net(CV_X, CV_Y, w, l, CV_L)
for i in range(10):
  print guess[i], ":", CV_L[i]