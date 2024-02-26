import wave
import sounddevice as sd
import soundfile as sf
import numpy as np
start = 1
end = 9
obj = wave.open('test.wav','r')
print( "Number of channels",obj.getnchannels())
print ( "Sample width",obj.getsampwidth())
print ( "Frame rate.",obj.getframerate())
print ("Number of frames",obj.getnframes())
print ( "parameters:",obj.getparams())
obj.setpos(start*obj.getframerate())
audio_data_bytes = obj.readframes((end-start)*obj.getframerate())
audio_data = np.frombuffer(audio_data_bytes, dtype=np.int16) / 32767
sd.play(audio_data, obj.getframerate())
sd.wait()
new = wave.open('myfile-5.wav', 'w')
new.setframerate(obj.getframerate())
new.setnchannels(1)
new.setsampwidth(2)
new.writeframes(audio_data_bytes)
print ( "Frame rate.",new.getframerate())
new.close()
obj.close()

