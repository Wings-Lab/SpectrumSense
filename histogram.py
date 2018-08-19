from pymongo import MongoClient
import datetime
import pprint
import json
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
import matplotlib.mlab as mlab
# from scipy import fftpack
# while 1:


def remove_noise(data):
	for index,value  in enumerate(data):
		if value < -40:
			data[index] = -70

	return data					
 
def generate_time_series(freqs, times, power):
	new_power = []
	new_time = []
	max_power = max(power[0])
	new_power.append(max_power)
	index = power[0].index(max_power)
	new_time.append(times[0][index])
	print(index)
	print(len(freqs))
	for i in range(1,len(freqs)-1):
		# print(len(power[i]), len(times[i]), )
		new_power.append(power[i][index])
		new_time.append(times[i][index])
	return new_power,new_time	

def filter(s1_freq_samples,s1_time_samples,s1_power_samples):
	new_freq = []
	new_power = []
	new_time = []
	for i,f in enumerate(s1_freq_samples):
		if(len(f) != 0):
			new_freq.append(f)
			new_power.append(s1_power_samples[i])
			new_time.append(s1_time_samples[i])
		else:
			print("ANOMALY FOUND")
			print(len(f))
			print(f)
			print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
	return(new_freq,new_time,new_power)		




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

print (data[0]['event']['nodenumber'])
sensor1_time = []
sensor1_power = []
sensor1_freq = []
for element in data:
	# if(element['event']['nodenumber'] == '9c:b6:d0:e9:73:4d'):
	sensor1_time.append(element['event']['timestamp'])
	sensor1_power.append(element['event']['power'])
	sensor1_freq.append(element['event']['frequency'])

		




points_1 = zip(sensor1_time,sensor1_freq,sensor1_power)


sorted_points_1 = sorted(points_1)


new_sensor1_freq = [point[1] for point in sorted_points_1]


new_sensor1_time = [point[0] for point in sorted_points_1]



new_sensor1_power = [point[2] for point in sorted_points_1]


strart_value = new_sensor1_freq[0]
start_index = 0
count = 0
s1_freq_samples = []
s1_power_samples = []
s1_time_samples = []
for  index, freq in enumerate(new_sensor1_freq):
	if index == 0:
		count = count + 1
	elif count > 0 and freq == strart_value:
		end_value = new_sensor1_freq[index-1]
		end_index = index-1
		# print(start_index,end_index, freq, new_sensor1_freq[index-1], index)
		# print('****************************************************')
		# print(len(new_sensor1_freq[start_index:end_index]))
		# print(new_sensor1_freq[start_index:end_index])

		s1_time_samples.append(new_sensor1_time[start_index:end_index])
		s1_power_samples.append(new_sensor1_power[start_index:end_index])
		s1_freq_samples.append(new_sensor1_freq[start_index:end_index])
		start_index = index

s1_time_samples.append(new_sensor1_time[start_index:-1])
s1_power_samples.append(new_sensor1_power[start_index:-1])
s1_freq_samples.append(new_sensor1_freq[start_index:-1])









total_sweeps = len(s1_freq_samples) 




s1_freq_samples,s1_time_samples,s1_power_samples = filter(s1_freq_samples ,s1_time_samples, s1_power_samples)
new_power,new_time = generate_time_series(s1_freq_samples,s1_time_samples,s1_power_samples)
f= open('Wireless_Transmission_distribution_test4','w')
print(new_power,file=f)


std = np.std(new_power)
mean = sum(new_power)/len(new_power)

 
num_bins = 30
# the histogram of the data
n, bins, patches = plt.hist(new_power, num_bins, facecolor='blue', alpha=0.5, density=True)
 
# add a 'best fit' line
y = mlab.normpdf(bins, mean, std)
plt.plot(bins, y, 'r--')
plt.xlabel('Power')
plt.ylabel('Probability')
# plt.title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')
 
# Tweak spacing to prevent clipping of ylabel
plt.subplots_adjust(left=0.15)
plt.show()


a =5


# fig = plt.figure(1)
# plt.plot(new_time,new_power)
# plt.show()

