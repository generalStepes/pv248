import wave
import struct
import numpy as np
import sys
from math import log2, pow

max = 0
min = 0
A4 = 440
C0 = A4*pow(2, -4.75)
name = ["c", "cis", "d", "es", "e", "f", "fis", "g", "gis", "a", "bes", "b"]

def pitch(freq):
    h = round(12*log2(freq/C0))
    n = h % 12
    totalName = name[n]
    if h // 12 < 2:
        totalName = totalName[0].upper()
        for item in range(0,h // 12):
            totalName = totalName + ","
    if h // 12 == 2:
        totalName = totalName[0].upper() + totalName[1:]
    if h // 12 > 2:
        for item in range(0,h // 12 - 3):
            totalName = totalName + "’"

    return totalName


def structUnpackFun(frames, nOfFrames):
    data = struct.unpack(str(nOfFrames) + "h", frames)
    return data

def convertStereo(data):
    tempVarArr = []
    for i in range(0,len(data)):
            if i % 2 ==0:
                tempVar = data[i]
            else:
                tempVar = (tempVar + data[i]) / 2
                tempVarArr.append(tempVar)
    data=np.array(tempVarArr)
    return data

def returnAvg(data, framerate):
    threshold = 20
    average = np.fft.rfft(data) / framerate
    average = np.abs(average)
    absArr = average
    average = np.average(average)
    return (average * threshold, absArr)


sound_file = wave.open(sys.argv[1], "r")
framerate = sound_file.getframerate()
nOfFrames = sound_file.getnframes()
nOfChannels = sound_file.getnchannels()
repeated = int(nOfFrames/framerate)
print(repeated)
frames = sound_file.readframes(framerate)
data = structUnpackFun(frames, nOfChannels * framerate)
data = np.array(data)

if (nOfChannels == 2): data = convertStereo(data)
print(data)
np.array_split(data,repeated)
print(data[0])

average, absArr = returnAvg(data, framerate)


for index, item in enumerate(absArr):
    if item > average:
        print(pitch(index))
