import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
import function
def plotSignalWave(song_file, output_file):
	plt.clf()
	# open .wav file
	sound_wave = function.open_file(song_file)
	
	# extract raw audio from .wav file
	signal = sound_wave["audio_data"]
	signal = np.frombuffer(signal, np.int16)

	# frame rate of .wav file
	frame_rate = sound_wave["framerate"]

	# time vector spaced linearly with the size of the audio file
	Time = np.linspace(0, len(signal)/frame_rate, num = len(signal))

	# plot Time versus signal
	plt.axis('off')
	plt.plot(Time, signal, color="mediumpurple")
	plt.savefig(output_file, bbox_inches='tight',transparent=True, pad_inches=0)
	return 

# output_file = 'try.png'
# input_file = 'Output4.wav'
# plotSignalWave(input_file, output_file)