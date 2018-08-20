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


def filter(start,end,s1_freq_samples,s1_time_samples,s1_power_samples):
	new_freq = []
	new_power = []
	new_time = []
	number = len(s1_freq_samples[0])
	# print("---> " ,number)
	for i,f in enumerate(s1_freq_samples):
		print(f)
		print(start)
		print(end)	
		# if (set([start,end]).issubset(set(f))):
		if (set([915800000.00]).issubset(set(f))):

			# print(f)
			# print("*************CAME HERE***********************")
			new_freq.append(f)
			new_power.append(s1_power_samples[i])
			new_time.append(s1_time_samples[i])

	return(new_freq,new_time,new_power)		



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
	return (sensor1_time, sensor1_power, sensor1_freq, sensor2_time, sensor2_power, sensor2_freq, sensor3_time, sensor3_power, sensor3_freq)


def organize_data (sensor1_time, sensor1_power, sensor1_freq, sensor2_time, sensor2_power, sensor2_freq, sensor3_time, sensor3_power, sensor3_freq):

	new_freq = sorted(sensor1_freq)

	points_1 = zip(sensor1_time,sensor1_freq,sensor1_power)
	points_2 = zip(sensor2_time,sensor2_freq,sensor2_power)
	points_3 = zip(sensor3_time,sensor3_freq,sensor3_power)

	sorted_points_1 = sorted(points_1)
	sorted_points_2 = sorted(points_2)
	sorted_points_3 = sorted(points_3)

	new_sensor1_freq = [point[1] for point in sorted_points_1]
	new_sensor2_freq = [point[1] for point in sorted_points_2]
	new_sensor3_freq = [point[1] for point in sorted_points_3]

	new_sensor1_time = [point[0] for point in sorted_points_1]
	new_sensor2_time = [point[0] for point in sorted_points_2]
	new_sensor3_time = [point[0] for point in sorted_points_3]


	new_sensor1_power = [point[2] for point in sorted_points_1]
	new_sensor2_power = [point[2] for point in sorted_points_2]
	new_sensor3_power = [point[2] for point in sorted_points_3]


	strart_value = new_sensor1_freq[0]
	start_index = 0
	count = 0
	s1_freq_samples = []
	s1_power_samples = []
	s1_time_samples = []
	for  index, freq in enumerate(new_sensor1_freq):
		if count == 0:
			count = count + 1
		elif count > 0 and freq == strart_value:
			count = count+1
			end_value = new_sensor1_freq[index-1]
			end_index = index-1
			# print(end_value)
			s1_time_samples.append(new_sensor1_time[start_index:end_index])
			s1_power_samples.append(new_sensor1_power[start_index:end_index])
			s1_freq_samples.append(new_sensor1_freq[start_index:end_index])
			start_index = index

		
			

	s1_time_samples.append(new_sensor1_time[start_index:])
	s1_power_samples.append(new_sensor1_power[start_index:])
	s1_freq_samples.append(new_sensor1_freq[start_index:])


	strart_value = new_sensor2_freq[0]
	start_index = 0
	count = 0
	s2_freq_samples = []
	s2_power_samples = []
	s2_time_samples = []
	for  index, freq in enumerate(new_sensor2_freq):
		if count == 0:
			count = count + 1
		elif count > 0 and freq == strart_value:
			count = count+1
			end_value = new_sensor2_freq[index-1]
			end_index = index-1
			s2_time_samples.append(new_sensor2_time[start_index:end_index])
			s2_power_samples.append(new_sensor2_power[start_index:end_index])
			s2_freq_samples.append(new_sensor2_freq[start_index:end_index])
			start_index = index

			

	s2_time_samples.append(new_sensor2_time[start_index:])
	s2_power_samples.append(new_sensor2_power[start_index:])
	s2_freq_samples.append(new_sensor2_freq[start_index:])


	strart_value = new_sensor3_freq[0]
	start_index = 0
	count = 0
	s3_freq_samples = []
	s3_power_samples = []
	s3_time_samples = []
	for  index, freq in enumerate(new_sensor3_freq):
		if count == 0:
			count = count + 1
		elif count > 0 and freq == strart_value:
			count = count+1
			end_value = new_sensor3_freq[index-1]
			end_index = index-1
			s3_time_samples.append(new_sensor3_time[start_index:end_index])
			s3_power_samples.append(new_sensor3_power[start_index:end_index])
			s3_freq_samples.append(new_sensor3_freq[start_index:end_index])
			start_index = index

			

	s3_time_samples.append(new_sensor3_time[start_index:])
	s3_power_samples.append(new_sensor3_power[start_index:])
	s3_freq_samples.append(new_sensor3_freq[start_index:])

	return(s1_time_samples,s1_power_samples,s1_freq_samples,s2_time_samples,s2_power_samples,s2_freq_samples,s3_time_samples,s3_power_samples,s3_freq_samples)	

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




sensor1_time, sensor1_power, sensor1_freq, sensor2_time, sensor2_power, sensor2_freq, sensor3_time, sensor3_power, sensor3_freq = connect_and_fetch(['130.245.9.243', '130.245.144.129' ,'130.245.72.45'])
# print(max(sensor1_power))
# print(max(sensor2_power))
# print(max(sensor3_power))

s1_time_samples,s1_power_samples,s1_freq_samples,s2_time_samples,s2_power_samples,s2_freq_samples,s3_time_samples,s3_power_samples,s3_freq_samples = organize_data(sensor1_time, sensor1_power, sensor1_freq, sensor2_time, sensor2_power, sensor2_freq, sensor3_time, sensor3_power, sensor3_freq)

start_freq = min(sensor1_freq)
end_freq = 915800000.00


s1_freq_filtered, s1_time_filtered, s1_power_filtered = filter(start_freq,end_freq,s1_freq_samples,s1_time_samples,s1_power_samples)
s2_freq_filtered, s2_time_filtered, s2_power_filtered = filter(start_freq,end_freq,s2_freq_samples,s2_time_samples,s2_power_samples)
s3_freq_filtered, s3_time_filtered, s3_power_filtered = filter(start_freq,end_freq,s3_freq_samples,s3_time_samples,s3_power_samples)



p1,t1 = generate_time_series(s1_freq_filtered,s1_time_filtered, s1_power_filtered)
p2,t2 = generate_time_series(s2_freq_filtered,s2_time_filtered, s2_power_filtered)
p3,t3 = generate_time_series(s3_freq_filtered,s3_time_filtered, s3_power_filtered)

print(p1,t1)
print("__________________________________________")
print(p2,t2)
print("__________________________________________")
print(p3,t3)
print("__________________________________________")


stp = 1000
t1 = np.divide(t1,stp)
t1 = np.round(t1)*stp

t2 = np.divide(t2,stp)
t2 = np.round(t2)*stp

t3 = np.divide(t3,stp)
t3 = np.round(t3)*stp

t1 = t1.astype(int)
t2 = t2.astype(int)
t3 = t3.astype(int)

min_time = min(min(t1),min(t2),min(t3))
max_time = min(max(t1),max(t2),max(t3))




# for i in t1:
# 	print(i)


# sen1,t1= padding(p1,t1,min_time,max_time,stp)
# sen2,t2 = padding(p2,t2,min_time,max_time,stp)
# sen3,t3 = padding(p3,t3,min_time,max_time,stp)

# plt.figure()
# plt.plot(sen1)
# plt.plot(sen2)
# plt.plot(sen3)

# plt.show()












p1,t1 = new_generate_time_series(sensor1_freq,sensor1_time, sensor1_power)
p2,t2 = new_generate_time_series(sensor2_freq,sensor2_time, sensor2_power)
p3,t3 = new_generate_time_series(sensor3_freq,sensor3_time, sensor3_power)


# p1 = np.divide(p1,10) 
# p2 = np.divide(p2,10) 
# p3 = np.divide(p3,10) 

# new_p1 = [10**i for i in p1]
# new_p2 = [10**i for i in p2]
# new_p3 = [10**i for i in p3]

# p1 = new_p1
# p2 = new_p2
# p3 = new_p3


# Filter requirements.
order = 6
fs = 10000.0       # sample rate, Hz
cutoff = 1000  # desired cutoff frequency of the filter, Hz

# Get the filter coefficients so we can check its frequency response.
b, a = butter_lowpass(cutoff, fs, order)
y1 = butter_lowpass_filter(p1, cutoff, fs, order)
y2 = butter_lowpass_filter(p2, cutoff, fs, order)
y3 = butter_lowpass_filter(p3, cutoff, fs, order)

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

# t1 = t1[0:restrict-1]
# t2 = t2[0:restrict-1]
# t3 = t3[0:restrict-1]



new_t2 = adjust(time2,lags[0])
new_t3 = adjust(time3,lags[1])




# for i in range(0,6):
# 	plt.subplot(1,6,i+1)
# 	plt.plot(cross_correlations[i])

# plt.show()


# print(len(y1),len(time1))
# print(len(y2),len(time1))
# print(len(y3),len(time1))


for i in range(0,20):
	print(t1[i+1]-t1[i])
	print("*************************************")
	print(t2[i+1]-t2[i])
	print("*************************************")
	print(t3[i+1]-t3[i])
	print("*************************************")

# print(time1)
# print("*************************************")
# print(t2)
# print("*************************************")

# print(t3)

print(len(p1[0:restrict-1]), len(p2[0:restrict-1]), len(p3[0:restrict-1]) )
# print(len(time1))

plt.subplot(2,1,1)
plt.plot(time1,p1[0:restrict-1], marker='*')
plt.plot(time2,p2[0:restrict-1],marker = '*')
plt.plot(time3,p3[0:restrict-1],marker = '*')

plt.subplot(2,1,2)
plt.plot(time1,p1[0:restrict-1],marker = '*')
plt.plot(new_t2,p2[0:restrict-1],marker = '*')
plt.plot(new_t3,p3[0:restrict-1],marker ='*')

plt.show()

count  = 0
for power in p1:
	if power > -65:
		count = count+1


print (count)
# plt.figure()
# plt.plot(t1[0:restrict-1], p1[0:restrict-1])
# plt.plot(t2[0:restrict-1], p2[0:restrict-1])
# plt.plot(t3[0:restrict-1], p3[0:restrict-1])
# plt.show()

# plt.subplot(2,1,1)
# plt.plot(t1,sen1)
# plt.plot(t2,sen2)
# plt.plot(t3,sen3)

# plt.subplot(2,1,2)
# plt.plot(t1,sen1)
# plt.plot(new_t2,sen2)
# plt.plot(new_t3,sen3)

# plt.show()






# fig = plt.figure(1)
# print (len(s1_freq_filtered))
# print (len(s2_freq_filtered))
# print (len(s3_freq_filtered))

# for i in range(1,100):
# 	plt.subplot(10,10,i)
# 	plt.plot(s1_freq_filtered[i],s1_power_filtered[i])
# 	plt.plot(s2_freq_filtered[i],s2_power_filtered[i])
# 	plt.plot(s3_freq_filtered[i],s3_power_filtered[i])
# 	plt.xlabel('Frequency')
# 	plt.ylabel('Power')
# 	# plt.show()
# plt.show()

# for i in range(100,200):
# 	plt.subplot(10,10,i-99)
# 	plt.plot(s1_freq_filtered[i],s1_power_filtered[i])
# 	plt.plot(s2_freq_filtered[i],s2_power_filtered[i])
# 	plt.plot(s3_freq_filtered[i],s3_power_filtered[i])
# 	plt.xlabel('Frequency')
# 	plt.ylabel('Power')
# 	# plt.show()

# plt.show()

# for i in range(200,300):
# 	plt.subplot(10,10,i-199)
# 	plt.plot(s1_freq_filtered[i],s1_power_filtered[i])
# 	plt.plot(s2_freq_filtered[i],s2_power_filtered[i])
# 	plt.plot(s3_freq_filtered[i],s3_power_filtered[i])
# 	plt.xlabel('Frequency')
# 	plt.ylabel('Power')
# 	# plt.show()		

# plt.show()

# for i in range(300,400):
# 	plt.subplot(10,10,i-299)
# 	plt.plot(s1_freq_filtered[i],s1_power_filtered[i])
# 	plt.plot(s2_freq_filtered[i],s2_power_filtered[i])
# 	plt.plot(s3_freq_filtered[i],s3_power_filtered[i])
# 	plt.xlabel('Frequency')
# 	plt.ylabel('Power')
# 	# plt.show()
# plt.show()


# plt.savefig('All_Sweeps.jpeg')






# plt.figure()
# plt.plot(t1,y1)
# plt.plot(t2,y2)
# plt.plot(t3,y3)
# plt.show()


