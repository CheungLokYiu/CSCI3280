#windows may need $ sudo apt install pulseaudio -y to use sounddevice
#wave only for checking, can comment out import wave and all print()

import struct
import wave
import numpy as np
import sounddevice as sd

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

    # with open('./recording/waverecording.wav', 'rb') as sample:
    #     sriff_header = sample.read(4)
    #     sriffcksize = sample.read(4)
    #     swaveid = sample.read(4)
    #     sfmtid = sample.read(4)
    #     sfmtcksize = sample.read(4)
    #     swFormatTag = sample.read(2)
    #     snchannels = sample.read(2)
    #     snSamplesPerSec = sample.read(4)
    #     snAvgBytesPerSec = sample.read(4)
    #     snBlockAlign = sample.read(2)
    #     swBitsPerSample = sample.read(2)
    #     sdatalabel = sample.read(4)
    #     sdatacksize = sample.read(4)
    #     snframe = int.from_bytes(sdatacksize, 'little') // int.from_bytes(snBlockAlign, 'little') * int.from_bytes(snchannels, 'little')
    #     saudio_data = sample.read(int.from_bytes(sdatacksize, 'little'))


    # #print property of original .wav
    # print("riff_header:", riff_header, sriff_header)
    # print("riffcksize", int.from_bytes(riffcksize, 'little'), int.from_bytes(sriffcksize, 'little'))
    # print("waveid", waveid, swaveid)
    # print("fmtid", fmtid, sfmtid)
    # print("fmtcksize", int.from_bytes(fmtcksize, 'little'), int.from_bytes(sfmtcksize, 'little'))
    # print("wFormatTag", wFormatTag, swFormatTag)
    # print("nchannels", int.from_bytes(nchannels, 'little'), int.from_bytes(snchannels, 'little'))
    # print("nSamplesPerSec", int.from_bytes(nSamplesPerSec, 'little'), int.from_bytes(snSamplesPerSec, 'little'))
    # print("nAvgBytesPerSec", int.from_bytes(nAvgBytesPerSec, 'little'), int.from_bytes(snAvgBytesPerSec, 'little'))
    # print("nBlockAlign", int.from_bytes(nBlockAlign, 'little'), int.from_bytes(snBlockAlign, 'little'))
    # print("wBitsPerSample", int.from_bytes(wBitsPerSample, 'little'), int.from_bytes(swBitsPerSample, 'little'))
    # print("datalabel", datalabel, sdatalabel)
    # print("datacksize", int.from_bytes(datacksize, 'little'), int.from_bytes(sdatacksize, 'little'))
    # print("nframes", nframe, snframe)
    # print("content", audio_data[-3000:-2950])
    # print("real content", saudio_data[-3000:-2950])
        #print property of original .wav
    print("riff_header:", riff_header)
    print("riffcksize", int.from_bytes(riffcksize, 'little'))
    print("waveid", waveid)
    print("fmtid", fmtid)
    print("fmtcksize", int.from_bytes(fmtcksize, 'little'),)
    print("wFormatTag", wFormatTag, )
    print("nchannels", int.from_bytes(nchannels, 'little'))
    print("nSamplesPerSec", int.from_bytes(nSamplesPerSec, 'little'))
    print("nAvgBytesPerSec", int.from_bytes(nAvgBytesPerSec, 'little'))
    print("nBlockAlign", int.from_bytes(nBlockAlign, 'little'))
    print("wBitsPerSample", int.from_bytes(wBitsPerSample, 'little'))
    print("datalabel", datalabel)
    print("datacksize", int.from_bytes(datacksize, 'little'))
    print("nframes", nframe)
    print("content", audio_data[-3000:-2950])

    #change new property accounding to edit property
    bytesperframe = int.from_bytes(nBlockAlign, 'little') // int.from_bytes(nchannels, 'little') #get bytes per frame to set read range
    framerate = int.from_bytes(nSamplesPerSec, 'little') #get current framerate
    new_audio_data = audio_data[start*bytesperframe*framerate:end*bytesperframe*framerate] #get new_audio_data of editting range
    nframe = (end-start)*framerate #get new no. of frame
    datacksize = nframe * int.from_bytes(nBlockAlign, 'little') #get new datacksize
    datacksize = struct.pack('<i', datacksize) #change dataacksize to bytes
    framerate = int(framerate * speed) #get new framrate from speed
    nSamplesPerSec = struct.pack('<i', framerate) #get nSamplesPerSec(bytes) from framerate(int)
    raw_data = riff_header+riffcksize+waveid+fmtid+fmtcksize+wFormatTag+nchannels+nSamplesPerSec+nAvgBytesPerSec+nBlockAlign+wBitsPerSample+datalabel+datacksize+new_audio_data
    if int.from_bytes(datacksize, 'little') % 2 == 1:
        raw_data += bytes([10])
    file_data = {
                "raw_data": raw_data,
                "audio_data": audio_data,
                "framerate": framerate
                }
    return file_data
        
def streamplay(file_data):
    # play new audio without saving
    play_audio_data = np.frombuffer(file_data["audio_data"], dtype=np.int16) / 32767
    sd.play(play_audio_data, file_data["framerate"])
    sd.wait()

def savefile(outfilename, data):
    #write new edited .wav
    with open(outfilename, "wb") as f:
        f.write(data["raw_data"])
        # f.write(riff_header+fmtid+fmtcksize+wFormatTag+nchannels+nSamplesPerSec+nAvgBytesPerSec+nBlockAlign+wBitsPerSample+datalabel+datacksize+new_audio_data)
        # if int.from_bytes(datacksize, 'little') % 2 == 1:
        #     f.write(bytes([10]))

def open_and_check(filename):
    #open and check the new .wav, can comment
    with open(filename, 'rb') as file:
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

    print("riff_header:", riff_header)
    print("fmtid", fmtid)
    print("fmtcksize", int.from_bytes(fmtcksize, 'little'))
    print("wFormatTag", wFormatTag)
    print("nchannels", int.from_bytes(nchannels, 'little'))
    print("nSamplesPerSec", int.from_bytes(nSamplesPerSec, 'little'))
    print("nAvgBytesPerSec", int.from_bytes(nAvgBytesPerSec, 'little'))
    print("nBlockAlign", int.from_bytes(nBlockAlign, 'little'))
    print("wBitsPerSample", int.from_bytes(wBitsPerSample, 'little'))
    print("datalabel", datalabel)


data = open_and_edit("output.wav", 2, 8, 2)
streamplay(data)
savefile("output_edit.wav",data)