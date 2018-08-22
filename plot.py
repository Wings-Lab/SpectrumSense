import numpy as np
import os
import matplotlib.pyplot as plt

d1 = np.loadtxt('001.txt')
d2 = np.loadtxt('005.txt')
d3 = np.loadtxt('01.txt')
d4 = np.loadtxt('015.txt')
d5 = np.loadtxt('02.txt')

d1 = np.mean(d1, axis=0)
d2 = np.mean(d2, axis=0)
d3 = np.mean(d3, axis=0)
d4 = np.mean(d4, axis=0)
d5 = np.mean(d5, axis=0)

x = [d1[0], d2[0], d3[0], d4[0], d5[0]]
y = [d1[1], d2[1], d3[1], d4[1], d5[1]]
z = [d1[2], d2[2], d3[2], d4[2], d5[2]]

plt.plot(x)
plt.plot(y)
plt.plot(z)

plt.ylabel("Detection Ratio")
plt.xlabel("Transmission length")

plt.show()
