    bytesperframe = int.from_bytes(nBlockAlign, 'little') // int.from_bytes(nchannels, 'little') #get bytes per frame to set read range
    framerate = int.from_bytes(nSamplesPerSec, 'little') #get current framerate
    new_audio_data = audio_data[int(start*bytesperframe*framerate):int(end*bytesperframe*framerate)] #get new_audio_data of editting range
    nframe = int((end-start)*framerate) #get new no. of frame
    datacksize = nframe * int.from_bytes(nBlockAlign, 'little') #get new datacksize
    datacksize = struct.pack('<i', datacksize) #change dataacksize to bytes
    framerate = int(framerate * speed) #get new framrate from speed
    nSamplesPerSec = struct.pack('<i', framerate) #get nSamplesPerSec(bytes) from framerate(int)