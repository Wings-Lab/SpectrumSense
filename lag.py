from pymongo import MongoClient
import datetime
import pprint
import json
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import butter, lfilter, freqz
from scipy import signal
import collections
import numpy as np
from numpy.fft import fft, ifft, fft2, ifft2, fftshift
# from scipy import fftpack
# while 1:

def cross_correlation_using_fft(x, y):
    f1 = fft(x)
    f2 = fft(np.flipud(y))
    cc = np.real(ifft(f1 * f2))
    return fftshift(cc)

def compute_shift(x, y):
    assert len(x) == len(y)
    c = cross_correlation_using_fft(x, y)
    assert len(c) == len(x)
    zero_index = int(len(x) / 2) - 1
    shift = zero_index - np.argmax(c)
    return shift    

def square_and_sum(arr):
    temp = 0
    for val in arr:
        temp = temp + val**2
    return temp
        
def find_correlation(series):
    results = []
    lags = []
    for i in series:
        for j in series:
            compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
            if not compare(i,j):
                var_i = square_and_sum(i)
                var_j = square_and_sum(j)
                den = (var_i*var_j)**(0.5)
                results.append(signal.correlate(i,j))
                lags.append(np.argmax(signal.correlate(i,j))-len(j)-1)
                print(len(i),len(j),len(signal.correlate(i,j)))
    return(results,lags)

sig1 = [0,1,0,1,0]
sig2 = [1,0,1,0,1]
t = [0,1,2,3,4]
corr,lags = find_correlation([sig1,sig2])
print("--->",lags)
t1 = t+lags[0]
print(t1)
plt.subplot(1,2,1)
plt.plot(t,sig1)
plt.plot(t,sig2)

plt.subplot(1,2,2)
plt.plot(t,sig1)
plt.plot(t1,sig2)
plt.show()



