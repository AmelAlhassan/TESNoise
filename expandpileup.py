#expandpileup
#Author Amel Alhassan
#Date 15.1.2016
# to seperate a pile up noticed in the noise test.


import numpy as np
import sys
import os
import matplotlib.pylab as plt


data = np.load(sys.argv[1])
pulse = data['pulse']
time_data = data['time']
del data.f
data.close()# del/close open file



# constants
time_scaling = 1e6 #us
voltage_scaling = 1e3 #mV
total_sum_raw = np.array([], dtype=float)
total_peak_raw = np.array([], dtype=float)
index = 0

for i in range(len(pulse)): 
#		if 'CHA' in x[0]:
	offline_trigger = -0.03#TL1 # Definition of an off_line trigger level (-0.03)
#		if 'CHB' in x[0]:
#			offline_trigger = TL2 # Definition of an off_line trigger level (-0.019)

	if (pulse[i] < offline_trigger):
		if (index != 0) & ((i - index) < 120):
			continue

		else:
			pulse_in = []  # Voltage coordinates
			time_in = []   # Time coordinates
			time_norm = []  # Normalised time coordinates (triggered point at 0 us)

			time_norm_single = 0
			loop_m = 1
			loop_n = 2
			n = i+1
			m = i

			# Event windows going from - 2 us to + 6 us around the triggered point
			start_point = time_data[i]-(2e-6)
			end_point = time_data[i]+(6e-6)
#			if start_point and end_point in time_data:

			# Select points before the triggered point
			while time_data[m] > start_point:


				pulse_in.append(pulse[m])
				time_in.append(time_data[m])
				time_norm.append(time_norm_single)
				time_norm_single = -(50e-9 * loop_m)
				loop_m = loop_m + 1
				m = m-1
			# Lists need to be reversed so that the first point is at -5 us instead of 0 us
			pulse_in = list(reversed(pulse_in))
			time_in = list(reversed(time_in))
			time_norm = list(reversed(time_norm))


			# Select points after the triggered point
			time_norm_single = 50e-9
			while time_data[n] < end_point:

				pulse_in.append(pulse[n])
				time_in.append(time_data[n])
				time_norm.append(time_norm_single)
				time_norm_single = (50e-9 * loop_n)
				loop_n = loop_n + 1
				n = n+1

			# Convert lists into arrays
			pulse_in = np.array(pulse_in)*1e3
			time_in = np.array(time_in)*1e6
			time_norm = np.array(time_norm)


			identifiant = str(i)
			index = np.array(i)
#				outpath = os.makedirs('pileup')
			save_name = os.path.join('pileup',identifiant)
 			np.savez(save_name, time=time_in, pulse=pulse_in,time_norm = time_norm,index=index)
			index = i
			print 'output', save_name+'.npz'

			time_bin = time_in[0] - time_in[1]
			PH = np.min(pulse_in)
			PI = sum_raw = abs(np.sum(time_bin * pulse_in))

			f = plt.figure()#figsize=(30,10))

			x1 = f.add_subplot(111)

			x1.plot(time_in,pulse_in*1e-3, label='PH = %.3f mV, PI= %.3f us' %(PH,PI))
			x1.axhline(y=-0)
			x1.axhline(y=-.03)
			x1.axhline(y=-.05)
			x1.axhline(y=-.06)
			x1.set_ylim(-.08,.04)
			x1.set_xlim(min(time_in),max(time_in))
#			x1.text = ()
			x1.legend( loc='best')
			x1.set_title('QE 3.1 ON CHA Run 2 #12 '+identifiant)
			plt.savefig('QE3_1_CHA_ON_012_pileup'+identifiant+'.pdf')
			plt.show()


