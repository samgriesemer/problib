import cPickle as pickle
import numpy as np

def unpickle(file):
    fo = open(file, 'rb')
    dict = pickle.load(fo)
    fo.close()
    return dict

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
