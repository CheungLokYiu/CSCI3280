import pyaudio
import struct 
import sounddevice as sd
import os
import numpy as np

p = pyaudio.PyAudio()
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
BITPERSAMPLE =16

#start recording 
def start_record(seconds):
    
    stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, input_device_index = 0, frames_per_buffer = CHUNK)

    print("start recording")
    frames = [] 
    # add while button true 
    for i in range (0, int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(data)
    # if button false then close stream 
    stream.stop_stream()
    stream.close()
    print("recording stopped")
    return frames

# raw audio file save to wav file  
def convert_audio_to_wav(frames, output_file):
    audio_data = frames["audio_data"] if isinstance(frames, dict) else b''.join(frames)

    # Calculate the number of audio frames
    num_frames = len(audio_data) // (BITPERSAMPLE // 8)

    # Calculate the size of the audio data
    audio_data_size = num_frames * (BITPERSAMPLE // 8)

    # Calculate the size of the WAV file header
    header_size = 36

    if (audio_data_size % 2 == 1):
        header_size += 1

    # Calculate the total size of the WAV file
    file_size = header_size + audio_data_size

    # Pack the WAV file header data
    riff_header = b'RIFF'
    riffcksize = struct.pack('<i', file_size)
    waveid = b'WAVE'
    fmtid = b'fmt '              
    fmtcksize = struct.pack ('<i',16)
    wFormatTag = b'\x01\x00'
    nchannels = struct.pack('<h', CHANNELS) 
    nSamplesPerSec = struct.pack('<i', RATE)
    nAvgBytesPerSec = struct.pack('<i', RATE * CHANNELS * (BITPERSAMPLE // 8))
    nBlockAlign = struct.pack ('<h', (BITPERSAMPLE // 8) * CHANNELS)
    wBitsPerSample = struct.pack ('<h', BITPERSAMPLE)
    datalabel = b'data'
    datacksize = struct.pack('<i', audio_data_size)
    raw_data = riff_header + riffcksize + waveid +fmtid+fmtcksize+wFormatTag+nchannels+ nSamplesPerSec + nAvgBytesPerSec + nBlockAlign + wBitsPerSample + datalabel + datacksize + audio_data

    nframe = int.from_bytes(datacksize, 'little') // int.from_bytes(nBlockAlign, 'little') * int.from_bytes(nchannels, 'little')
    framerate = int.from_bytes(nSamplesPerSec, 'little')

    # Write the WAV file header to the output file
    with open(output_file+'.wav', 'wb') as f:
        f.write(raw_data)
    
    file_data = {
            "raw_data": raw_data,
            "audio_data": audio_data,
            "framerate": framerate,
            "bytesperframe": int.from_bytes(nBlockAlign, 'little') // int.from_bytes(nchannels, 'little'),
            "nchannel": int.from_bytes(nchannels, 'little'),
            "nframe": nframe,
            "length": nframe / framerate
            }
    print('return file_data')
    return file_data
    

#play wav audio 
# def play_wavaudio(filename): 
#      playsound.playsound(filename+'.wav')

def open_file(infilename):
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
    bytesperframe = int.from_bytes(nBlockAlign, 'little') // int.from_bytes(nchannels, 'little') #get bytes per frames to set read range
    framerate = int.from_bytes(nSamplesPerSec, 'little') #get current framerate
    raw_data = riff_header+riffcksize+waveid+fmtid+fmtcksize+wFormatTag+nchannels+nSamplesPerSec+nAvgBytesPerSec+nBlockAlign+wBitsPerSample+datalabel+datacksize+audio_data
    if int.from_bytes(datacksize, 'little') % 2 == 1:
        raw_data += bytes([10])
    file_data = {
                "raw_data": raw_data,
                "audio_data": audio_data,
                "nchannel": int.from_bytes(nchannels, 'little'),
                "framerate": framerate,
                "bytesperframe": bytesperframe,
                "nframe": nframe,
                "length": nframe / framerate
                }
    print('return file_data')
    return file_data

def speed_func(infilename, framerate):
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
    bytesperframe = int.from_bytes(nBlockAlign, 'little') // int.from_bytes(nchannels, 'little') #get bytes per frames to set read range
    framerate = int(framerate) #get current framerate
    # new_audio_data = audio_data[(int(start*bytesperframe*framerate)-int(start*byte
    # sperframe*framerate)%2):int(end*bytesperframe*framerate)-int(end*bytesperframe*framerate)%2] #get new_audio_data of editting range
    # nframe = int((end-start)*framerate) #get new no. of frames
    # datacksize = nframe * int.from_bytes(nBlockAlign, 'little') #get new datacksize
    # datacksize = struct.pack('<i', datacksize) #change dataacksize to bytes
    # framerate = int(framerate * speed) #get new framrate from speed
    nSamplesPerSec = struct.pack('<i', framerate) #get nSamplesPerSec(bytes) from framerate(int)
    print('write data')
    raw_data = riff_header+riffcksize+waveid+fmtid+fmtcksize+wFormatTag+nchannels+nSamplesPerSec+nAvgBytesPerSec+nBlockAlign+wBitsPerSample+datalabel+datacksize+audio_data
    if int.from_bytes(datacksize, 'little') % 2 == 1:
        raw_data += bytes([10])
    file_data = {
                "raw_data": raw_data,
                "audio_data": audio_data,
                "nchannel": int.from_bytes(nchannels, 'little'),
                "framerate": framerate,
                "bytesperframe": bytesperframe,
                "nframe": nframe,
                "length": nframe / framerate
                }
    print('return file_data')
    return file_data

def trim(infilename, start, end):
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
    bytesperframe = int.from_bytes(nBlockAlign, 'little') // int.from_bytes(nchannels, 'little') #get bytes per frames to set read range
    framerate = int.from_bytes(nSamplesPerSec, 'little') #get current framerate
    new_audio_data = audio_data[(int(start*bytesperframe*framerate)-int(start*bytesperframe*framerate)%2):int(end*bytesperframe*framerate)-int(end*bytesperframe*framerate)%2] #get new_audio_data of editting range
    nframe = int((end-start)*framerate) #get new no. of frames
    datacksize = nframe * int.from_bytes(nBlockAlign, 'little') #get new datacksize
    datacksize = struct.pack('<i', datacksize) #change dataacksize to bytes
    # framerate = int(framerate * speed) #get new framrate from speed
    # nSamplesPerSec = struct.pack('<i', framerate) #get nSamplesPerSec(bytes) from framerate(int)
    print('write data')
    raw_data = riff_header+riffcksize+waveid+fmtid+fmtcksize+wFormatTag+nchannels+nSamplesPerSec+nAvgBytesPerSec+nBlockAlign+wBitsPerSample+datalabel+datacksize+new_audio_data
    if int.from_bytes(datacksize, 'little') % 2 == 1:
        raw_data += bytes([10])
    file_data = {
                "raw_data": raw_data,
                "audio_data": new_audio_data,
                 "nchannel": int.from_bytes(nchannels, 'little'),
                "framerate": framerate,
                "bytesperframe": bytesperframe,
                "nframe": nframe,
                "length": nframe / framerate
                }
    print('return file_data')
    return file_data
        
def streamplay(file_data):
    # play new audio without saving
    play_data = file_data["audio_data"] if isinstance(file_data, dict) else b''.join(file_data)
    framerate = file_data["framerate"] if isinstance(file_data, dict) else RATE
    print('playing...')
    play_audio_data = np.frombuffer(play_data, dtype=np.int16) / 32767
    sd.play(play_audio_data, framerate)
    sd.wait()
    print('end play')

def savefile(outfilename, data):
    #write new edited .wav
    with open(outfilename, "wb") as f:
        f.write(data["raw_data"])

def replace_audio(start, end, replace_data, old_data):
    framerate = old_data["framerate"]
    bytesperframe = old_data["bytesperframe"]
    old_audio_data = old_data["audio_data"]
    new_audio_data = bytearray()
    i = 0
    while(i < int(start*bytesperframe*framerate)-int(start*bytesperframe*framerate)%2):
        new_audio_data.append(old_audio_data[i])
        i += 1
    for _ in replace_data:
        new_audio_data.append(_)
        i += 1
    while(i < len(old_audio_data)):
        new_audio_data.append(old_audio_data[i])
        i += 1
    new_audio_data = bytes(new_audio_data)
    new_audio_data_dict = {
                "audio_data": new_audio_data,
                "framerate": framerate,
                "bytesperframe": bytesperframe
                }
    return new_audio_data_dict

# Example usage
output_file = 'output'

start = 4.56
end = 9.5
speed = 0.5


# # Example usage
# output_file = 'output'
# final_output_file = 'final_output'
# replace_output_file = 'replace_output'


# start = 4.56
# end = 9.54
# speed = 2

# frame1 =  start_record(10) # raw audio file 
# # streamplay(frame1) # play recording before save as .wav
# data = convert_audio_to_wav(frame1, output_file) # raw audio file save to wav file  

# frame2 = start_record(4) #raw audio file 2
# data2 = replace_audio(output_file, 4, 4+4, b''.join(frame2), data) #replace the audio start to end to audio 2
# # streamplay(data2) # play data2 before save
# convert_audio_to_wav(data2, final_output_file)  #save data2

# streamplay(trim(final_output_file, 0.333, 2.5)) # edit final_out_file and play
# streamplay(speed_func(final_output_file, 1.443))