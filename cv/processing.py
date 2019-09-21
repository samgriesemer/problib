import numpy as np
from scipy.signal import convolve2d

def edge_gradient(X):
  # define x and y derivative kernels
  xkernel = np.array([[1,0,-1],[2,0,-2],[1,0,-1]])
  ykernel = np.transpose(xkernel)

  # convolve (same) image with sobel kernels
  ix = convolve2d(X, xkernel, boundary='symm', mode='same')
  iy = convolve2d(X, ykernel, boundary='symm', mode='same')

  # compute gradient magnitudes and angles
  G = np.sqrt(ix**2 + iy**2)
  theta = np.arctan2(iy, ix)
  return G, theta

def nm_suppression(E, G, theta):
  # descretize angles
  theta = np.round(theta/(np.pi/4))

  # get weighted edges
  G = np.multiply(G, E)

  # define four angle types
  edge_x = (theta == 0) | (theta == 4) | (theta == -4)
  edge_y = (theta == 2) | (theta == -2)
  edge_pd = (theta == 1) | (theta == -3)
  edge_nd = (theta == 3) | (theta == -1)

  # compute shifted maps in eight directions
  shift_px = np.roll(G,1,1)
  shift_nx = np.roll(G,-1,1)
  shift_py = np.roll(G,1,0)
  shift_ny = np.roll(G,-1,0)
  shift_ppd = np.roll(shift_px,-1,0)
  shift_npd = np.roll(shift_nx,1,0)
  shift_pnd = np.roll(shift_px,1,0)
  shift_nnd = np.roll(shift_nx,-1,0)

  # find local maxima in any of discretized directions
  ix = np.logical_and(G > shift_px, G > shift_nx) & edge_x
  iy = np.logical_and(G > shift_py, G > shift_ny) & edge_y
  ipd = np.logical_and(G > shift_ppd, G > shift_npd) & edge_pd
  ind = np.logical_and(G > shift_pnd, G > shift_nnd) & edge_nd

  # combine all edge directions
  E = (ix | iy | ipd | ind).astype(float)
  return E

def edge_detection(X, threshold, suppression=True):
  G, theta = edge_gradient(X)
  E = np.float32(G > threshold)
  if suppression: 
    E = nm_suppression(E, G, theta)
  return E
