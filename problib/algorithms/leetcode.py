# Container with most water
# https://leetcode.com/problems/container-with-most-water/

# visualization tool
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

arr = np.array([1,8,6,2,5,4,8,3,7])
x = np.arange(0,len(arr))
y = np.arange(0,len(arr))
X, Y = np.meshgrid(x,y)
t = (X-Y)
m = np.minimum(arr[X],arr[Y])
Z = np.multiply(t,m)

# contour plot
fig, ax = plt.subplots()
CS = ax.contour(X, Y, Z)
ax.clabel(CS, inline=1, fontsize=10)
plt.show()