import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt

SCALE_FACTOR_EEG = (4500000)/24/(2**23-1) #uV/count
SCALE_FACTOR_AUX = 0.002 / (2**4)
channels = 8

def read_from_file():
	with open("record2.txt", "rb") as f:
		xdata = [line.decode('utf-8').split(' ') for line in f]
	data = np.array(xdata)
	data = data[:, 1:8]
	#print(data)
	alldata = [[float(a) for a in row] for row in data]
	return np.array(alldata)

def main():
	fs = 250 # 250 hz
	ori_data = read_from_file()

	# Define EEG bands
	eeg_bands = {'Delta': (0, 4),
				'Theta': (4, 8),
				'Alpha': (8, 12),
				'Beta': (12, 30),
				'Gamma': (30, 45)}

	eeg_band_fft = {}
	for band in eeg_bands:
		eeg_band_fft[band] = 0

	print(len(ori_data[0]))
	for i in range(channels-1):
		
		data = ori_data[2*fs:3*fs, i]

		f, psd = signal.welch(data, fs, nperseg = fs)
		for band in eeg_bands:
			x = np.where((f >= eeg_bands[band][0]) & (f <= eeg_bands[band][1]))
			eeg_band_fft[band] += np.mean(psd[x])

	
	# Plot the data (using pandas here cause it's easy)
	df = pd.DataFrame(columns=['band', 'val'])
	df['band'] = eeg_bands.keys()
	df['val'] = [eeg_band_fft[band] for band in eeg_bands]
	ax = df.plot.bar(x='band', y='val', legend=False)
	ax.set_xlabel("EEG band")
	ax.set_ylabel("band Power")
	plt.show()

if __name__ == '__main__':
	main()