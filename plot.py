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
plt.xticks(np.arange(5), ('0.01-0.02', '0.03-0.05', '0.08-0.1', '0.13-0.15', '0.18-0.2'))
trans_lenght =['0.01-0.02',0.05]
plt.plot(x, linewidth = '3', marker = '*', markersize = 12, fontsize = 12)
plt.plot(y, linewidth = '3', marker = '*', markersize = 12, fontsize = 12)
plt.plot(z, linewidth = '3', marker = '*', markersize = 12, fontsize = 12)

plt.ylabel("Detection Ratio", fontsize = 15)
plt.xlabel("Transmission length", fontsize = 15)
plt.title("Variarion of Detection Probability with Transmission Time", fontsize = 12)

plt.show()
