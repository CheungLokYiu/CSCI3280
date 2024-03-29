import pyaudio
import struct
import numpy as np

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

def hex_to_dec(frames):
    
    bframe = b''.join(frames)
    raw_data = [s for s in bframe]
    #print (raw_data)
    return raw_data


#print(audio_data)
# Output: [254, 139, 254, 140, 254, 138, 254, 139]
# Example audio data as a string of bytes in hexadecimal format
#audio_data_hex = b'\xfe\x8b\xfe\x8c\xfe\x8a\xfe\x8b'

# Convert the hexadecimal data to a list of integers
#audio_data = [s for s in struct.unpack(f'{len(audio_data_hex)}B', audio_data_hex)]

#print(audio_data)
# Output: [254, 139, 254, 140, 254, 138, 254, 139]

def convert_audio_to_wav(audio_data, output_file, sample_rate, bits_per_sample, channels):
    # Convert the audio data to 16-bit PCM using numpy
    audio_data = np.array(audio_data, dtype=np.int8)
    audio_data = np.divide(audio_data, 2**7)
    audio_data = np.int16(audio_data * 2**(bits_per_sample - 8))

    # Convert the audio data to little-endian format
    audio_data = audio_data.astype('<i2')

    # Calculate the number of audio frames
    num_frames = len(audio_data) // (bits_per_sample // 8)

    # Calculate the size of the audio data
    audio_data_size = num_frames * (bits_per_sample // 8)

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
    header_6 = struct.pack('>i2', channels) 
    header_7 = struct.pack('<2i', 
                         sample_rate, 
                         sample_rate * channels * (bits_per_sample // 8))
    header_8 = struct.pack ('>i2',
                         (bits_per_sample // 8) * channels, 
                         bits_per_sample)
    header_9 = b'data'
    header_10 = struct.pack('<i', audio_data_size)

    # Write the WAV file header to the output file
    with open(output_file, 'wb') as f:
        f.write(header_1 + header_2 + header_3 +header_4+header_5+header_6+header_7+ header_8 + header_9)
        # Write the audio data to the output file
        f.write(audio_data.tobytes())

# Example usage
frame =  s_record(10)


output_file = 'output.wav'
sample_rate = 44100
bits_per_sample = 16
channels = 1
convert_audio_to_wav(hex_to_dec(frame), output_file, sample_rate, bits_per_sample, channels)