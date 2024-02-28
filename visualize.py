
import matplotlib.pyplot as plt
import wave
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
def plotSignalWave(song_file):
	# open .wav file
	sound_wave = wave.open(song_file, 'r')
	
	# extract raw audio from .wav file
	signal = sound_wave.readframes(-1)
	signal = np.frombuffer(signal, np.int16)

	# frame rate of .wav file
	frame_rate = sound_wave.getframerate()

	# time vector spaced linearly with
	# the size of the audio file
	Time = np.linspace(0, len(signal)/frame_rate, num = len(signal))

	# plot Time versus signal
	# plt.title("Signal Wave")
	plt.axis('off')
	plt.plot(Time, signal)
	plt.savefig('out.png', bbox_inches='tight',transparent=True, pad_inches=0)

	return ''
plotSignalWave('test.wav')