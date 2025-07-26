'''Pattern on how to write a WAV file'''

import numpy as np
import wave, math

sRate = 44100
nSamples = sRate * 5
x = np.arange(nSamples)/float(sRate)
# create a numpy array of numbers from 0 to nSamples - 1
# then divide those numbers by the sample rate to get the 
# time value (s) when each audio clip is taken (i/R)
vals = np.sin(2.0*math.pi*220.0*x)
# use x array to make a new array containing sine wave
# amplitude values
data = np.array(vals*32767, 'int16').tobytes()
# convert sin wave to range [-1,1] in 16-bit values
# then turn into a string for WAV file
file = wave.open('sine220.wav', 'wb')
file.setparams((1, 2, sRate, nSamples, 'NONE', 'uncompressed'))
# params: single channel(mono), two-bit (2), uncompressed
file.writeframes(data)
# write the data to the file
file.close()

# WAV files consist of a series of values,
# each representing the amplitude of the stored
# sound at a given point. Each is allotted a fixed
# number of bits(16) called RESOLUTION

# set smpling rate = number of times audio 
# is sampled in seconds (44100 Hz)
# WAV file = 44100 16-bit values for every second

# A = sin(2pift); A = amplitude 
# f = frequency; t = current time

# A = sin(2pifi/R); i = index of sample
# R = sampling rate; f = frequency