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

			
		elif (element['event']['nodenumber'] == macs[1]):
			sensor2_time.append(element['event']['timestamp'])
			sensor2_power.append(element['event']['power'])
			sensor2_freq.append(element['event']['frequency'])


		if(element['event']['nodenumber'] == macs[2]):
			sensor3_time.append(element['event']['timestamp'])
			sensor3_power.append(element['event']['power'])
			sensor3_freq.append(element['event']['frequency'])

	print (sensor2_freq)	
	db.drop_collection(collection)	
	return (sensor1_time, sensor1_power, sensor1_freq, sensor2_time, sensor2_power, sensor2_freq, sensor3_time, sensor3_power, sensor3_freq)




def padding(p1,t1,start,end,stp):
	time = np.arange(start,end+1,stp)
	# print("SIZE = ", len(time))
	new_series = []
	i = 0
	done = 0

	while(not done):
		if(time[i] < t1[0]):
			# print(time[i], " < ", t1[0])
			new_series.append(-80.00)
			i = i+1
		else:
			done = 1
			break

	for index in range(0,len(p1)-1):
		for i in range(t1[index]+1,t1[index+1],stp):
			x = []
			y = []
			x.append(t1[index])	
			x.append(t1[index+1])	
			y.append(p1[index])	
			y.append(p1[index+1])	
			z = np.polyfit(x, y, 1)	
			x = []
			y = []
			p= np.poly1d((z))
			new_series.append(p(i))


	done = 0
	f = len(t1)-1		
	while(not done):
		if(time[f] > t1[-1]):
			new_series.append(-80.00)
			f = f+1
		else:
			done = 1
			break

	# print("SERIES DONE!!!")		
	return(new_series, time)		




sensor1_time, sensor1_power, sensor1_freq, sensor2_time, sensor2_power, sensor2_freq, sensor3_time, sensor3_power, sensor3_freq = connect_and_fetch(['130.245.9.243', '8.8.8.8' ,'130.245.74.108'])



p1,t1 = new_generate_time_series(sensor1_freq,sensor1_time, sensor1_power)
p2,t2 = new_generate_time_series(sensor2_freq,sensor2_time, sensor2_power)
p3,t3 = new_generate_time_series(sensor3_freq,sensor3_time, sensor3_power)

print(p1,t1)
print("__________________________________________")
print(p2,t2)
print("__________________________________________")
print(p3,t3)
print("__________________________________________")



restrict = min(len(p1),len(p2),len(p3))
number_of_sensors = 3
# series = (p1[0:restrict],p2[],p3)

# print(len(sen1), len(sen2), len(sen3), len(t1))

series = (p1[0:restrict-1],p2[0:restrict-1],p3[0:restrict-1])
signal_length = len(p1)

# cross_correlations,lags = find_correlation(series)
print(len(series[0]),len(series[1]),len(series[2]))
shift1 = compute_shift(series[0],series[1])
shift2 = compute_shift(series[0],series[2])
lags = [shift1, shift2]

# print(lags)

time1 = range(0,restrict-1)
time2 = range(0,restrict-1)
time3 = range(0,restrict-1)




new_t2 = adjust(time2,lags[0])
new_t3 = adjust(time3,lags[1])


# plt.subplot(2,1,1)
# plt.plot(time1,p1[0:restrict-1], marker='*')
# plt.plot(time2,p2[0:restrict-1],marker = '*')
# plt.plot(time3,p3[0:restrict-1],marker = '*')

# plt.subplot(2,1,2)
# plt.plot(t1[0:restrict-1],p1[0:restrict-1],marker = '*')
# plt.show()
# plt.plot(t2[0:restrict-1],p2[0:restrict-1],marker = '*')
# plt.show()
# plt.plot(t3[0:restrict-1],p3[0:restrict-1],marker ='*')
# plt.show()

count1  = 0
found_low_power = 1
for power in p1:
	if power > -65 and found_low_power == 1:
		count1 = count1+1
		found_low_power = 0
	if power < -65:
		found_low_power = 1


print ("COUNT1 = ", count1)
count2  = 0
found_low_power = 1
for power in p2:
	if power > -65 and found_low_power == 1:
		count2 = count2+1
		found_low_power = 0
	if power < -65:
		found_low_power = 1


print ("COUNT2 = ", count2)		
count3  = 0
found_low_power = 1
for power in p3:
	if power > -65 and found_low_power == 1:
		found_low_power = 0
		count3 = count3+1
	if power < -65:
		found_low_power = 1



print ("COUNT3 = ", count3);
tfile = open('exp-data.txt', 'a')
tfile.write("%s\t"%str(count1))
tfile.write("%s\t"%str(count2))
tfile.write("%s\n"%str(count3))
tfile.close()
