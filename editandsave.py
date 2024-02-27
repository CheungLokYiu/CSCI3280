import struct
import wave
import numpy as np
import sounddevice as sd

#edit property
start = 0
end = 17
speed = 0.5

#read original .wav
wav_file = wave.open('test.wav','r')
with open('test.wav', 'rb') as file:
    riff_header = file.read(12)
    fmtid = file.read(4)
    fmtcksize = file.read(4)
    wFormatTag = file.read(2)
    nchannels = file.read(2)
    nSamplesPerSec = file.read(4)
    nAvgBytesPerSec = file.read(4)
    nBlockAlign = file.read(2)
    wBitsPerSample = file.read(2)
    datalabel = file.read(4)
    datacksize = file.read(4)
    nframe = int.from_bytes(datacksize, 'little') // int.from_bytes(nBlockAlign, 'little') * int.from_bytes(nchannels, 'little')
    audio_data = file.read(int.from_bytes(datacksize, 'little'))
    rest = file.read()

#print property of original .wav
print("riff_header:", riff_header)
print("fmtid", fmtid)
print("fmtcksize", int.from_bytes(fmtcksize, 'little'))
print("wFormatTag", wFormatTag)
print("nchannels", int.from_bytes(nchannels, 'little'), wav_file.getnchannels())
print("nSamplesPerSec", int.from_bytes(nSamplesPerSec, 'little'), wav_file.getframerate())
print("nAvgBytesPerSec", int.from_bytes(nAvgBytesPerSec, 'little'))
print("nBlockAlign", int.from_bytes(nBlockAlign, 'little'), int.from_bytes(nchannels, 'little') * int.from_bytes(nBlockAlign, 'little'))
print("wBitsPerSample", int.from_bytes(wBitsPerSample, 'little'), wav_file.getsampwidth()*8)
print("datalabel", datalabel)
print("nframes", nframe, wav_file.getnframes())

#change new property accounding to edit property
bytesperframe = int.from_bytes(nBlockAlign, 'little') // int.from_bytes(nchannels, 'little') #get bytes per frame to set read range
framerate = int.from_bytes(nSamplesPerSec, 'little') #get current framerate
new_audio_data = audio_data[start*bytesperframe*framerate:end*bytesperframe*framerate] #get new_audio_data of editting range
nframe = (end-start)*framerate #get new no. of frame
datacksize = nframe * int.from_bytes(nBlockAlign, 'little') #get new datacksize
datacksize = struct.pack('<i', datacksize) #change dataacksize to bytes
framerate = int(framerate * speed) #get new framrate from speed
nSamplesPerSec = struct.pack('<i', framerate) #get nSamplesPerSec(bytes) from framerate(int)

#play new audio without saving
play_audio_data = np.frombuffer(audio_data, dtype=np.int16) / 32767
sd.play(play_audio_data, int.from_bytes(nSamplesPerSec, 'little'))

#write new edited .wav
with open("myfile-5.wav", "wb") as f:
    f.write(riff_header+fmtid+fmtcksize+wFormatTag+nchannels+nSamplesPerSec+nAvgBytesPerSec+nBlockAlign+wBitsPerSample+datalabel+datacksize+new_audio_data+rest)

#open and check the new .wav, can comment
with open('myfile-5.wav', 'rb') as file:
    ff_header = file.read(12)
    fmtid = file.read(4)
    fmtcksize = file.read(4)
    wFormatTag = file.read(2)
    nchannels = file.read(2)
    nSamplesPerSec = file.read(4)
    nAvgBytesPerSec = file.read(4)
    nBlockAlign = file.read(2)
    wBitsPerSample = file.read(2)
    datalabel = file.read(4)
    datacksize = file.read(4)
    nframe = int.from_bytes(datacksize, 'little') // int.from_bytes(nBlockAlign, 'little') * int.from_bytes(nchannels, 'little')
    audio_data = file.read(int.from_bytes(datacksize, 'little'))
    rest = file.read()

print("riff_header:", riff_header)
print("fmtid", fmtid)
print("fmtcksize", int.from_bytes(fmtcksize, 'little'))
print("wFormatTag", wFormatTag)
print("nchannels", int.from_bytes(nchannels, 'little'), wav_file.getnchannels())
print("nSamplesPerSec", int.from_bytes(nSamplesPerSec, 'little'), wav_file.getframerate())
print("nAvgBytesPerSec", int.from_bytes(nAvgBytesPerSec, 'little'))
print("nBlockAlign", int.from_bytes(nBlockAlign, 'little'), int.from_bytes(nchannels, 'little') * int.from_bytes(nBlockAlign, 'little'))
print("wBitsPerSample", int.from_bytes(wBitsPerSample, 'little'), wav_file.getsampwidth()*8)
print("datalabel", datalabel)
print("nframes", nframe, wav_file.getnframes())
