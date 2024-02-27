import pyaudio
import struct
import os
import playsound 
import numpy as np
import sounddevice as sd

p = pyaudio.PyAudio()
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
BITPERSAMPLE =16

#start recording 
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
    #print(len(frames))
    #print(type(frames))
    #print(type(frames[0]))
    return frames

def hex_to_dec(frames):
    bframe = b''.join(frames)
    raw_data = [s for s in bframe]
    #print (raw_data)
    return raw_data

# raw audio file save to wav file  
def convert_audio_to_wav(audio_data, frame, output_file):

    # Convert the audio data to little-endian format
    #audio_data = audio_data.astype('<i2')

    # Calculate the number of audio frames
    num_frames = len(audio_data) // (BITPERSAMPLE // 8)

    # Calculate the size of the audio data
    audio_data_size = num_frames * (BITPERSAMPLE // 8)

    # Calculate the size of the WAV file header
    header_size = 36
    header_10 = 0

    if (audio_data_size % 2 == 1):
        header_size += 1
        header_10 = 1 

    # Calculate the total size of the WAV file
    file_size = header_size + audio_data_size

    # Pack the WAV file header data
    #header_1 = struct.pack('<4sI4sI4sIHII')
    header_1 = b'RIFF'
    header_2 = struct.pack('<i', file_size)
    header_3 = b'WAVE'+ b'fmt '              
    header_4 = struct.pack ('<i',16)
    header_5 = b'\x01\x00'
    header_6 = struct.pack('<h', CHANNELS) 
    header_7 = struct.pack('<2i', 
                         RATE, 
                         RATE * CHANNELS * (BITPERSAMPLE // 8))
    header_8 = struct.pack ('<2h',
                         (BITPERSAMPLE // 8) * CHANNELS, 
                         BITPERSAMPLE)
    header_9 = b'data'
    header_10 = struct.pack('<i', audio_data_size)

    # Write the WAV file header to the output file
    with open(output_file+".wav", 'wb') as f:
        f.write(header_1 + header_2 + header_3 +header_4+header_5+header_6+header_7+ header_8 + header_9 + header_10)
        # Write the audio data to the output file
        #f.write(audio_data.tobytes())
        # print(audio_data.tobytes())
        for _ in frame:
            f.write(_)


def play_wavaudio(filename): # ok 
     playsound.playsound(filename)

def open_and_edit(infilename,start,end,speed):
    #read original .wav
    with open(infilename, 'rb') as file:
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

    print("editing")
    bytesperframe = int.from_bytes(nBlockAlign, 'little') // int.from_bytes(nchannels, 'little') #get bytes per frame to set read range
    framerate = int.from_bytes(nSamplesPerSec, 'little') #get current framerate
    new_audio_data = audio_data[(int(start*bytesperframe*framerate)-int(start*bytesperframe*framerate)%2):int(end*bytesperframe*framerate)] #get new_audio_data of editting range
    # print((int(start*bytesperframe*framerate)-int(start*bytesperframe*framerate)%2), '-', int(end*bytesperframe*framerate))
    nframe = int((end-start)*framerate) #get new no. of frame
    datacksize = nframe * int.from_bytes(nBlockAlign, 'little') #get new datacksize
    datacksize = struct.pack('<i', datacksize) #change dataacksize to bytes
    framerate = int(framerate * speed) #get new framrate from speed
    nSamplesPerSec = struct.pack('<i', framerate) #get nSamplesPerSec(bytes) from framerate(int)
    print('write data')
    raw_data = riff_header+riffcksize+waveid+fmtid+fmtcksize+wFormatTag+nchannels+nSamplesPerSec+nAvgBytesPerSec+nBlockAlign+wBitsPerSample+datalabel+datacksize+new_audio_data
    if int.from_bytes(datacksize, 'little') % 2 == 1:
        raw_data += bytes([10])
    file_data = {
                "raw_data": raw_data,
                "audio_data": new_audio_data,
                "framerate": framerate
                }
    print('return file_data')
    return file_data
        
def streamplay(file_data):
    # play new audio without saving
    print('playing...')
    play_audio_data = np.frombuffer(file_data["audio_data"], dtype=np.int16) / 32767
    sd.play(play_audio_data, file_data["framerate"])
    sd.wait()
    print('end play')

def savefile(outfilename, data):
    #write new edited .wav
    with open(outfilename, "wb") as f:
        f.write(data["raw_data"])



# Example usage
output_file = 'output'
sample_rate = 44100
bits_per_sample = 16
channels = 1
start = 4.56
end = 9.5
speed = 0.5

frame1 =  s_record(10) # raw audio file 
convert_audio_to_wav(hex_to_dec(frame1),frame1, output_file) # raw audio file save to wav file  
data = open_and_edit(output_file+'.wav', start, end, speed)
streamplay(data)
start = 0
end = 6
data = open_and_edit(output_file+'.wav', start, end, speed)
streamplay(data)
savefile('output_edit.wav', data)




