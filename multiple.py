#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Fri Nov 24 15:33:37 2017
##################################################

if __name__ == '__main__':
	import ctypes
	import sys
	if sys.platform.startswith('linux'):
		try:
			x11 = ctypes.cdll.LoadLibrary('libX11.so')
			x11.XInitThreads()
		except:
			print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import sip
import sys
import time
import random


class top_block(gr.top_block):

	def __init__(self):
		gr.top_block.__init__(self, "Top Block")

		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 32000
		self.gain = gain = 25

		##################################################
		# Blocks
		##################################################
		self.uhd_usrp_sink_0 = uhd.usrp_sink(
			",".join(("", "")),
			uhd.stream_args(
				cpu_format="fc32",
				channels=range(1),
			),
		)
		self.uhd_usrp_sink_0.set_samp_rate(10)
		self.uhd_usrp_sink_0.set_center_freq(915800000, 0)
		self.uhd_usrp_sink_0.set_gain(gain, 0)
		self.uhd_usrp_sink_0.set_bandwidth(samp_rate, 0)
		device_info = self.uhd_usrp_sink_0.get_usrp_info()
	
		print device_info['mboard_serial']
		  
		self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 915.8e6, 1, 0)

		##################################################
		# Connections
		##################################################
		self.connect((self.analog_sig_source_x_0, 0), (self.uhd_usrp_sink_0, 0))    

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.uhd_usrp_sink_0.set_bandwidth(self.samp_rate, 0)
		self.qtgui_sink_x_0.set_frequency_range(915.8e6, self.samp_rate)
		self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

	def get_gain(self):
		return self.gain

	def set_gain(self, gain):
		self.gain = gain
		self.uhd_usrp_sink_0.set_gain(self.gain, 0)
			

import time
import spur
from subprocess import call
import numpy as np
import matplotlib.pyplot as plt

def start_iq_read(gain):
	print "Starting to read ", str(gain)
	output_file = str(gain)
	command = "rtl_sdr -f 916e6 -s 1e6 -n 3e7 -g 1 " + output_file
	print command
	call([command], shell=True)

def main(top_block_cls=top_block, options=None):

	tb = top_block_cls()
	tb.start()
	
	# gain_list = [i for i in range(50, 85, 5)]
	gain_list = np.random.choice(np.arange(70,100,5), 100, replace=True) 
	# gain_list = [50,100,150,200,250,50,100,150,200,250]
	# gain_list.extend([i for i in range(20, 51)])
	#gain_list.extend([i for i in range(5, 51, 5)])

	# gain_list = [70,80,90,100,110] # ++++++++++++++++++++++++++++++++++++++++++++++++++++++
	t = []
	values = []
	elapsd_time = 0
	for gain in gain_list:
		gain = 100 # ++++++++++++++++++++++++++++++++++++++++++++++++++++++
		tb.set_gain(gain)
		values.append(gain)
		t.append(elapsd_time)
		transmit_time = np.random.uniform(0,0.1)
		# transmit_time = 0.5 # ++++++++++++++++++++++++++++++++++++++++++++++++++++++
		elapsd_time = elapsd_time+transmit_time
		values.append(gain)
		t.append(elapsd_time)
		values.append(0)        
		t.append(elapsd_time)
		time .sleep(transmit_time)
		sleep_time = np.random.uniform(0.6,1)
		# sleep_time = 1 # ++++++++++++++++++++++++++++++++++++++++++++++++++++++
		elapsd_time = elapsd_time + sleep_time
		values.append(0)
		t.append(elapsd_time)
		tb.set_gain(0)
		time.sleep(sleep_time)
	   # start_iq_read(gain)

		# time.sleep(3) #Allow 20s for transmitter to respond
	plt.figure()
	plt.plot(t,values)
	plt.show()	
	
	thefile = open('/home/muhammad/Desktop/Dropbox/Research/PhD/Specsense/Intrusion_detection/Code/SpecSense/transmitter.txt', 'w')
	for gain in gain_list:
		print>>thefile,gain

	def quitting():
		tb.stop()
		tb.wait()

if __name__ == '__main__':
	main()
