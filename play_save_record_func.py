import pyaudio
import wave
import os
import playsound

p = pyaudio.PyAudio()
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


def s_record(seconds):
    
    stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, input_device_index = 0, frames_per_buffer = CHUNK)

    print("start recording")
    frames = []
    for i in range (0, int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    print("recording stopped")
    return frames

def saverecording(name,frames):
    wf = wave.open(os.path.join('recording', name + ".wav"), "wb") # open a folder first to store all recording
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def play_audio(filename): # ok 
     print("playing " + filename)
     playsound.playsound("recording/"+filename)
     print("end of " + filename)

saverecording("first", s_record(10))
play_audio("first.wav")
