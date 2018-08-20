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
import math
# from scipy import fftpack
# while 1:

def cross_correlation_using_fft(x, y):
	f1 = fft(x)
	f2 = fft(np.flipud(y))
	cc = np.real(ifft(f1 * f2))
	return fftshift(cc)

def compute_shift(x, y):
	# print(len(x),len(y))
	assert len(x) == len(y)
	c = cross_correlation_using_fft(x, y)
	assert len(c) == len(x)
	zero_index = int(len(x) / 2) - 1
	shift = zero_index - np.argmax(c)
	return shift    


def adjust(t1, lag):
	new_time=[]
	for index,value in enumerate(t1):
		new_time.append(t1[index]-lag)
	return new_time

def butter_lowpass(cutoff, fs, order=100):
	nyq = 0.5 * fs
	normal_cutoff = cutoff / nyq
	b, a = butter(order, normal_cutoff, btype='low', analog=False)
	return b, a

def butter_lowpass_filter(data, cutoff, fs, order=100):
	b, a = butter_lowpass(cutoff, fs, order=order)
	y = lfilter(b, a, data)
	return y

def generate_frequency_plots(s1_freq_filtered, s1_time_filtered, s1_power_filtered, s2_freq_filtered, s2_time_filtered, s2_power_filtered, s3_freq_filtered, s3_time_filtered, s3_power_filtered):
	fig = plt.figure(1)
	# print (len(s1_freq_filtered))
	# print (len(s2_freq_filtered))
	# print (len(s3_freq_filtered))

	for i in range(1,40):
		plt.subplot(8,5,i)
		plt.plot(s1_freq_filtered[i],s1_power_filtered[i])
		plt.plot(s2_freq_filtered[i],s2_power_filtered[i])
		plt.plot(s3_freq_filtered[i],s3_power_filtered[i])
		plt.xlabel('Frequency')
		plt.ylabel('Power')
		# plt.show()

	plt.show()
	fig = plt.figure(2)
	for i in range(40,80):
		plt.subplot(8,5,i-39)
		plt.plot(s1_freq_filtered[i],s1_power_filtered[i])
		plt.plot(s2_freq_samples[i],s2_power_filtered[i])
		plt.plot(s3_freq_filtered[i],s3_power_filtered[i])
		plt.xlabel('Frequency')
		plt.ylabel('Power')

	plt.show()
	fig = plt.figure(3)
	for i in range(80,110):
		plt.subplot(8,5,i-79)
		plt.plot(s1_freq_samples[i],s1_power_samples[i])
		plt.plot(s2_freq_samples[i],s2_power_samples[i])
		plt.plot(s3_freq_samples[i],s3_power_samples[i])
		plt.xlabel('Frequency')
		plt.ylabel('Power')


	# plt.savefig('All_Sweeps.jpeg')
	plt.show()	


def find_correlation(series):
	results = []
	lags = []
	for i in series:
		for j in series:
			compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
			if not compare(i,j):
				var_i = np.sum(i**2)
				var_j = np.sum(j**2)
				den = (var_i*var_j)**(0.5)
				results.append(signal.correlate(i,j,mode='full')/den)
				lags.append(np.argmax(signal.correlate(i,j,mode='full')/den)-len(j)-1)
				# print(len(i),len(j),len(signal.correlate(i,j,mode='full')/den))
	return(results,lags)	

def generate_time_series(freqs, times, power):
	# print ("freqs::::",freqs)
	new_power = []
	new_time = []
	max_power = max(power[0])
	new_power.append(max_power)
	index = power[0].index(max_power)
	new_time.append(times[0][index])
	freq_to_locate = freqs[0][index]
	# print("looking for: ", freq_to_locate, max_power)
	# print(freqs[1])
	# print("************************************")
	# print(len(freqs))
	for i in range(1,len(freqs)-2):
		# print(i)
		# print(freqs[i])
		index = freqs[i].index(freq_to_locate)
		new_power.append(power[i][index])
		new_time.append(times[i][index])
	return new_power,new_time

def new_generate_time_series(freqs, times, power):
	# print ("freqs::::",freqs)
	new_power = []
	new_time = []
	max_power = max(power)
	# print("----->",max_power)
	# new_power.append(max_power)
	index = power.index(max_power)
	# new_time.append(times[0][index])
	freq_to_locate = freqs[index]
	# print("looking for: ", freq_to_locate, max_power)
	# print(freqs[1])
	# print("************************************")
	# print(len(freqs))

	for i,f in enumerate(freqs):
		if f == freq_to_locate:
			new_power.append(power[i])
			new_time.append(times[i])

	return new_power,new_time	



def remove_noise(data):
	for index,value  in enumerate(data):
		if value < -40:
			data[index] = -70

	return data					

def connect_and_fetch(macs):
	# print (macs[0])
	client = MongoClient('mongodb://130.245.144.129:27017/')
	# print (client.database_names())
	db = client['kaa']
	# print (db.collection_names())
	collection = db['logs_94543827559106667076']
	# print (db)
	# print (collection)
	cursor = collection.find({})
	data = []
	# f= open("data.txt","w+")
	for document in cursor:
		data.append(document)

	# print (data[0]['event']['nodenumber'])
	sensor1_time = []
	sensor1_power = []
	sensor1_freq = []
	sensor2_time = []
	sensor2_power = []
	sensor2_freq = []
	sensor3_time = []
	sensor3_power = []
	sensor3_freq = []
	for element in data:
		if(element['event']['nodenumber'] == macs[0]):
			sensor1_time.append(element['event']['timestamp'])
			sensor1_power.append(element['event']['power'])
			sensor1_freq.append(element['event']['frequency'])
		
	return (sensor1_time, sensor1_power, sensor1_freq)




sensor1_time, sensor1_power, sensor1_freq= connect_and_fetch(['130.245.74.108'])

start_freq = min(sensor1_freq)
end_freq = 915800000.00



p1,t1 = new_generate_time_series(sensor1_freq,sensor1_time, sensor1_power)

pdf,bin_edges= np.histogram(p1,bins=10,density=False)
total_sum = sum(pdf)
pdf = np.divide(pdf,total_sum)
print(len(bin_edges[0:-1]), len(pdf))
plt.plot(bin_edges[0:-1],pdf, marker= '*')
plt.show()