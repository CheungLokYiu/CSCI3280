import struct
import wave
import numpy as np
import sounddevice as sd
start = 5
end = 15
speed = 0.75
wav_file = wave.open('test.wav','r')
with open('test.wav', 'rb') as file:
    riff_header = file.read(12)
    # fmt_chunk_header = file.read(14)
    # fmt_chunk_size = int.from_bytes(fmt_chunk_header[4:], 'little')
    # fmt_chunk_data = file.read(fmt_chunk_size)
    fmtid = file.read(4)
    cksize = file.read(4)
    wFormatTag = file.read(2)
    nchannels = file.read(2)
    nSamplesPerSec = file.read(4)
    nAvgBytesPerSec = file.read(4)
    nBlockAlign = file.read(2)
    wBitsPerSample = file.read(2)
    datalabel = file.read(4)
    nframe = file.read(4)
    audio_data = file.read(int.from_bytes(nframe, 'little') // int.from_bytes(nchannels, 'little') // (int.from_bytes(wBitsPerSample, 'little') // 8) * int.from_bytes(wBitsPerSample, 'little') // int.from_bytes(nBlockAlign, 'little'))
    rest = file.read()
    
    

    # data_chunk_header = file.read(8)
    # data_chunk_size = int.from_bytes(data_chunk_header[4:], 'little')
    # audio_data = file.read(data_chunk_size)


print("riff_header:", riff_header)
print("fmt", fmtid)
print("cksize", int.from_bytes(cksize, 'little'))
print(len(wFormatTag))
print("wFormatTag", wFormatTag)
print("nchannels", int.from_bytes(nchannels, 'little'), wav_file.getnchannels())
print("nSamplesPerSec", int.from_bytes(nSamplesPerSec, 'little'), wav_file.getframerate())
print("nAvgBytesPerSec", int.from_bytes(nAvgBytesPerSec, 'little'))
print("nBlockAlign", int.from_bytes(nBlockAlign, 'little'), int.from_bytes(nchannels, 'little') * int.from_bytes(wBitsPerSample, 'little') // 8)
print("wBitsPerSample", int.from_bytes(wBitsPerSample, 'little'), wav_file.getsampwidth()*8)
print("datalabel", datalabel)
print("nframes", int.from_bytes(nframe, 'little'), int.from_bytes(nframe, 'little') // int.from_bytes(nchannels, 'little') // (int.from_bytes(wBitsPerSample, 'little') // 8), wav_file.getnframes())

bytesperframe = int.from_bytes(nchannels, 'little') * (int.from_bytes(wBitsPerSample, 'little') // 8)*int.from_bytes(nSamplesPerSec, 'little')
new_audio_data = audio_data[start*bytesperframe:end*bytesperframe]
nframe = (end-start)*int.from_bytes(nSamplesPerSec, 'little')
nframe = nframe * int.from_bytes(nchannels, 'little') * (int.from_bytes(wBitsPerSample, 'little') // 8)
nframe = struct.pack('<i', nframe)

nSamplesPerSec = int(int.from_bytes(nSamplesPerSec, 'little') * speed)
nSamplesPerSec = struct.pack('<i', nSamplesPerSec)

with open("myfile-5.wav", "wb") as f:
    f.write(riff_header+fmtid+cksize+wFormatTag+nchannels+nSamplesPerSec+nAvgBytesPerSec+nBlockAlign+wBitsPerSample+datalabel+nframe+new_audio_data+rest)


with open('myfile-5.wav', 'rb') as file:
    riff_header = file.read(12)
    fmtid = file.read(4)
    cksize = file.read(4)
    wFormatTag = file.read(2)
    nchannels = file.read(2)
    nSamplesPerSec = file.read(4)
    nAvgBytesPerSec = file.read(4)
    nBlockAlign = file.read(2)
    wBitsPerSample = file.read(2)
    datalabel = file.read(4)
    nframe = file.read(4)
    audio_data = file.read(int.from_bytes(nframe, 'little') // int.from_bytes(nchannels, 'little') // (int.from_bytes(wBitsPerSample, 'little') // 8) * int.from_bytes(wBitsPerSample, 'little') // int.from_bytes(nBlockAlign, 'little'))
    rest = file.read()

print("riff_header:", riff_header)
print("fmt", fmtid)
print("cksize", int.from_bytes(cksize, 'little'))
print(len(wFormatTag))
print("wFormatTag", wFormatTag)
print("nchannels", int.from_bytes(nchannels, 'little'), wav_file.getnchannels())
print("nSamplesPerSec", int.from_bytes(nSamplesPerSec, 'little'), wav_file.getframerate())
print("nAvgBytesPerSec", int.from_bytes(nAvgBytesPerSec, 'little'))
print("nBlockAlign", int.from_bytes(nBlockAlign, 'little'), int.from_bytes(nchannels, 'little') * int.from_bytes(wBitsPerSample, 'little') // 8)
print("wBitsPerSample", int.from_bytes(wBitsPerSample, 'little'), wav_file.getsampwidth()*8)
print("datalabel", datalabel)
print("nframes", int.from_bytes(nframe, 'little') // int.from_bytes(nchannels, 'little') // (int.from_bytes(wBitsPerSample, 'little') // 8), wav_file.getnframes())
play_audio_data = np.frombuffer(audio_data, dtype=np.int16) / 32767
sd.play(play_audio_data, int.from_bytes(nSamplesPerSec, 'little'))


