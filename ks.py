"""
ks.py

Uses the Karplus-Strong algorithm to generate musical notes
in a pentatonic scale

Author: Katherine Oriol
"""

import matplotlib
import os
import time, random
import wave, argparse
import numpy as np
from collections import deque
from matplotlib import pyplot as plt
import pyaudio
# to fix graph display issues on macOS
matplotlib.use('TkAgg')

# show plot of algorithm in action?
gShowPlot = False

# notes of a pentatonic minor scale
# piano C4-E(b)-F-G-B(b)-C5
pmNotes = {'C4':262, 'Eb':311, 'F':349, 'G':391, 'Bb':466}

CHUNK = 1024

# initialize plotting
# make a matplotlib figure
fig, ax = plt.subplots(1)
# and line plot
line, = ax.plot([], [])


# write out WAV file
def writeWAVE(fname, data):
    """write data to WAV file"""
    # open file to write 'wb'
    file = wave.open(fname, 'wb')
    # WAV file parameters
    nChannels = 1
    sampleWidth = 2
    frameRate = 44100
    nFrames = 44100
    # set parameters
    file.setparams((nChannels, sampleWidth, frameRate, nFrames,
                    'NONE', 'noncompressed'))
    file.writeframes(data)
    file.close()


def generateNote(freq):
    """generate note using Karplus-Strong algorithm"""
    nSamples = 44100
    sampleRate = 44100
    # rate and speed is 44100 Hz = 1 second long
    N = int(sampleRate/freq)
    # length of Karplus-Strong ring buffer = sample rate / frequency3
    
    if gShowPlot:
        # set axis
        ax.set_xlim([0, N])
        ax.set_ylim([-1.0, 1.0])
        line.set_xdata(np.arange(0,N))
        # if I have a plot, this is the x and y range. 
        # x range is from 0 to N - 1

    # initialize ring buffer in deque container with 
    # random numbers in range -0.5 to 0.5 with max length N
    buf = deque([random.random() - 0.5 for i in range(N)], maxlen=N)
    # init sample buffer
    samples = np.array([0]*nSamples,'float32')

    for i in range(nSamples):
        samples[i] = buf[0]
        avg = 0.995*0.5*(buf[0] + buf[1])
        buf.append(avg)
        # plot of flag set
        if gShowPlot:
            if i % 1000 == 0:
                line.set_ydata(buf)
                fig.canvas.draw()
                fig.canvas.flush_events()

    # samples to 16-bit to string
    # max value is 32767 for 16-bit
    samples = np.array(samples * 32767, 'int16')
    # turn into bytes for WAV file
    return samples.tobytes()


# play a WAV file
class NotePlayer:
    # constructor
    def __init__(self):
        # init pyaudio object that'll use WAV file
        self.pa = pyaudio.PyAudio()
        # open stream 16-bit single channel
        self.stream = self.pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            output=True)
        # dictionary of notes with filenames of 
        # 5 pentatonic note WAV files
        self.notes = []

    # failure to provide a __del__() method for a class causes 
    # problems when objects are repeatedly created and destroyed. 
    # Some system-wide resources, like pyaudio, 
    # may not be cleaned up properly
    def __del__(self):
        # destructor
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()
    
    # add a WAV filename to the class, adds to notes list
    # class will draw on this list to play a WAV file
    def add(self, fileName):
        self.notes.append(fileName)

    # play a note
    def play(self, fileName):
        try:
            print("playing " + fileName)
            # open WAV file and read 'rb'
            wf = wave.open(fileName, 'rb')
            # read a chunk (1024 frames) from file to data
            data = wf.readframes(CHUNK)
            # read rest
            while data != b'':
                # write the contents of data to PyAudio output
                # stream aka speaker. Read data in chunks to 
                # maintain sample rate at output side
                self.stream.write(data)
                # read the next chunk of data from WAV file
                data = wf.readframes(CHUNK)
            # clean up
            wf.close()
        except BaseException as err:
            print(f"Exception! {err=}, {type(err)=}.\nExiting.")
            exit(0)
    
    def playRandom(self):
        """play a random note"""
        index = random.randint(0, len(self.notes)-1)
        note = self.notes[index]
        self.play(note)

# main() function
def main():
    # declare global var
    global gShowPlot
    parser = argparse.ArgumentParser(description="Generating sounds " \
    "with Karplu-Strong Algorithm.")

    # add arguments
    parser.add_argument('--display', action='store_true', required=False)
    parser.add_argument('--play', action='store_true', required=False)
    args = parser.parse_args()

    # show plot if flag set
    if args.display:
        gShowPlot = True
        # plt.ion()
        plt.show(block=False)

    # create note player
    nplayer = NotePlayer()

    print('creating notes...')
    for name, freq in list(pmNotes.items()):
        fileName = name + '.wav'
        if not os.path.exists(fileName) or args.display:
            data = generateNote(freq)
            print('creating ' + fileName + '...')
            writeWAVE(fileName, data)
        else:
            print('fileName already created. skipping...')

        # add note to player
        nplayer.add(name + '.wav')

        # play note if display flag set
        if args.display:
            nplayer.play(name + '.wav')
            time.sleep(0.5)
        
    # play a random tune
    if args.play:
        while True:
            try:
                nplayer.playRandom()

                # rest - 1 to 8 beats
                rest = np.random.choice([1, 2, 4, 8], 1,
                                        p = [0.15, 0.7, 0.1, 0.05])
                time.sleep(0.25*rest[0])
            except KeyboardInterrupt:
                exit()

# call main
if __name__ == '__main__':
    main()

### Expirements to try:
# - Create a method that replicates the sound of two string of 
# different frequencies vibrating together. The KS algorithm
# produces a ring buffer full of sound amplitude values. You
# can combine two sounds by adding their amplitudes together

# - Replicate the sound of two strings vibrating together, as
# described above, but add a time delat between the first and 
# second string plucks.

# Write a method to read music from a text file and generate 
# musical notes. Then play te music using these notes. You can 
# use a format where the note names are followed by integer rest 
# time intervals, like: C4 1 F4 2 G4 1