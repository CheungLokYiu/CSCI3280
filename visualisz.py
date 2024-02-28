
import matplotlib.pyplot as plt
import wave
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from function import *
def plotSignalWave(song_file):
	# open .wav file
	# sound_wave = wave.open(song_file, 'r')
	sound_wave = open_file(song_file)
	
	# extract raw audio from .wav file
	signal = sound_wave["audio_data"]
	signal = np.frombuffer(signal, np.int16)

	# frame rate of .wav file
	frame_rate = sound_wave["framerate"]

	# time vector spaced linearly with
	# the size of the audio file
	Time = np.linspace(0, len(signal)/frame_rate, num = len(signal))

	# plot Time versus signal
	# plt.title("Signal Wave")
	plt.axis('off')
	plt.plot(Time, signal)
	plt.savefig('out.png', bbox_inches='tight',transparent=True, pad_inches=0)

	return ''
plotSignalWave('Output2.wav')