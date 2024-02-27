#windows may need $ sudo apt install pulseaudio -y to use sounddevice
#wave only for checking, can comment out import wave and all print()

import struct
import wave
import numpy as np
# import sounddevice as sd

#edit property
start = 0
end = 17
speed = 1.5

#read original .wav
wav_file = wave.open('test.wav','r')
with open('test.wav', 'rb') as file:
    riff_header = file.read(4)
    riffcksize = file.read(4)
    waveid = file.read(4)
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
    # rest = file.read()

#print property of original .wav
print("riff_header:", riff_header)
print("riffcksize", int.from_bytes(riffcksize, 'little'))
print("waveid", waveid)
print("fmtid", fmtid)
print("fmtcksize", int.from_bytes(fmtcksize, 'little'))
print("wFormatTag", wFormatTag)
print("nchannels", int.from_bytes(nchannels, 'little'), wav_file.getnchannels())
print("nSamplesPerSec", int.from_bytes(nSamplesPerSec, 'little'), wav_file.getframerate())
print("nAvgBytesPerSec", int.from_bytes(nAvgBytesPerSec, 'little'))
print("nBlockAlign", int.from_bytes(nBlockAlign, 'little'), int.from_bytes(nchannels, 'little') * int.from_bytes(nBlockAlign, 'little'))
print("wBitsPerSample", int.from_bytes(wBitsPerSample, 'little'), wav_file.getsampwidth()*8)
print("datalabel", datalabel)
print("datacksize", int.from_bytes(datacksize, 'little'))
print("nframes", nframe, wav_file.getnframes())
# print("rest", rest)

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
# play_audio_data = np.frombuffer(audio_data, dtype=np.int16) / 32767
# print("play edit audio")
# sd.play(play_audio_data, int.from_bytes(nSamplesPerSec, 'little'))
# status = sd.wait()

#write new edited .wav
with open("myfile.wav", "wb") as f:
    # f.write(riff_header+fmtid+fmtcksize+wFormatTag+nchannels+nSamplesPerSec+nAvgBytesPerSec+nBlockAlign+wBitsPerSample+datalabel+datacksize+new_audio_data)
    f.write(riff_header+riffcksize+waveid+fmtid+fmtcksize+wFormatTag+nchannels+nSamplesPerSec)
    f.write(nAvgBytesPerSec+nBlockAlign+wBitsPerSample+datalabel+datacksize+new_audio_data)
    if int.from_bytes(datacksize, 'little') % 2 == 1:
        f.write(bytes([10]))

#open and check the new .wav, can comment
with open('myfile.wav', 'rb') as file:
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
    # rest = file.read()

# print("riff_header:", riff_header)
# print("fmtid", fmtid)
# print("fmtcksize", int.from_bytes(fmtcksize, 'little'))
# print("wFormatTag", wFormatTag)
# print("nchannels", int.from_bytes(nchannels, 'little'), wav_file.getnchannels())
# print("nSamplesPerSec", int.from_bytes(nSamplesPerSec, 'little'), wav_file.getframerate())
# print("nAvgBytesPerSec", int.from_bytes(nAvgBytesPerSec, 'little'))
# print("nBlockAlign", int.from_bytes(nBlockAlign, 'little'), int.from_bytes(nchannels, 'little') * int.from_bytes(nBlockAlign, 'little'))
# print("wBitsPerSample", int.from_bytes(wBitsPerSample, 'little'), wav_file.getsampwidth()*8)
# print("datalabel", datalabel)
# print("nframes", nframe, wav_file.getnframes())
