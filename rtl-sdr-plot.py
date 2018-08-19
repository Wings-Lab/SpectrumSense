import matplotlib
matplotlib.rcParams["backend"] = "TkAgg"
from pylab import *
from rtlsdr import *
import time
import matplotlib.animation as anim
import matplotlib.pyplot as plt
'''Reads data from RTL-SDR and plots the live data as animation.'''
# print (matplotlib.get_backend())

def restart():
	root = Tkinter.Tk()
	root.withdraw()
	result = tkMessageBox.askyesno("Restart", "Do you want to restart animation?")
	if result:
		ani.frame_seq = ani.new_frame_seq()
		ani.event_source.start()
	else:
		plt.close()

def update(i):
	plt.cla()
	samples = sdr.read_samples(512 * 128)
	values = psd(samples, NFFT=128, Fs=sdr.sample_rate / 1e6, Fc=sdr.center_freq / 1e6)

	firsthalf = 10 * np.log10(values[0][int(2 * len(values[0]) / 8):int(1 * len(values[0]) / 2) - 1])
	averageValues = np.average(firsthalf)
	#print (time.time(), firsthalf[20])
	# if i == len(samples)-1:
	# 	plt.clf()
	#     # restart()
# 
sdr = RtlSdr()

# configure device
sdr.sample_rate = 2.4e6
sdr.center_freq = 916e6 
sdr.gain = 1

xlabel('Frequency (MHz)')
ylabel('Relative power (dB)')

#samples = sdr.read_samples(256*1024)

# use matplotlib to estimate and plot the PSD

fig = plt.figure()
a = anim.FuncAnimation(fig, update, frames=1000, repeat=False)
plt.show()
# a.save('mymovie.mp4')


