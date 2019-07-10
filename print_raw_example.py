from pyOpenBCI import OpenBCICyton
from pylsl import StreamInfo, StreamOutlet
import numpy as np
import signal
import pickle
import sys

alldata = []
SCALE_FACTOR_EEG = (4500000)/24/(2**23-1) #uV/count
SCALE_FACTOR_AUX = 0.002 / (2**4)

#print("Creating LSL stream for EEG. \nName: OpenBCIEEG\nID: OpenBCItestEEG\n")

#info_eeg = StreamInfo('OpenBCIEEG', 'EEG', 8, 250, 'float32', 'OpenBCItestEEG')

#print("Creating LSL stream for AUX. \nName: OpenBCIAUX\nID: OpenBCItestEEG\n")

#info_aux = StreamInfo('OpenBCIAUX', 'AUX', 3, 250, 'float32', 'OpenBCItestAUX')

#outlet_eeg = StreamOutlet(info_eeg)
#outlet_aux = StreamOutlet(info_aux)

def signal_handler(sig, frame):
	print("here")
	write_to_file()
	raise Exception("Timed out")

def print_raw(sample):
	#outlet_eeg.push_sample(np.array(sample.channels_data)*SCALE_FACTOR_EEG)
	#outlet_aux.push_sample(np.array(sample.aux_data)*SCALE_FACTOR_AUX)
	save_to_file(sample.channels_data)
	print(np.array(sample.channels_data))

def save_to_file(data):
	s = [str(i*SCALE_FACTOR_EEG) for i in data]
	x = " ".join(s)
	alldata.append(x)

def write_to_file():
	with open("record0.txt", "w") as f:
		#pickle.dump(alldata, f)
		f.write("\n".join(alldata))
	print("written")

def main():
	TIMEOUT = 60

	#Set (daisy = True) to stream 16 ch 
	board = OpenBCICyton(daisy = True)

	
	signal.signal(signal.SIGALRM, signal_handler)
	signal.alarm(TIMEOUT)
	try:
		board.start_stream(print_raw)
	except Exception as e:
		print("timed out")
		board.stop_stream()
		sys.exit(0)
	

if __name__ == '__main__':
	main()