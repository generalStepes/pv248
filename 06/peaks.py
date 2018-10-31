import wave
import struct
import numpy as np

sound_file = wave.open("audio.wav", "r")
print (sound_file)

file_length = sound_file.getnframes()
data = sound_file.readframes(-1)
data = struct.unpack('{n}h'.format(n=file_length), data)
data = np.array(data)
sound_file.close()

print (data)
