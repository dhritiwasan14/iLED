import pyaudio
from collections import namedtuple
import wave
import aubio
import sys

# length of data to read.
chunk = 1024
# behind namedtuple
# '''
# Point = namedtuple('Point', 'x y')
# pt1 = Point(1.0, 5.0)
# pt2 = Point(2.5, 1.5)
# '''
reading = namedtuple('reading', ['pitch', 'volume'])
p = pyaudio.PyAudio()

def main(args):
    # open the file for reading, wav file
    wf = wave.open(sys.argv[1], 'rb')
    mic = pA.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)

    readings = []
    pDetection = aubio.pitch("default", 2048,
        2048//2, 44100)
    while True:

        data = mic.read(2048//2) # per chunk
        samples = np.fromstring(data, dtype=aubio.float_type) 
        pitch = pDetection(samples)[0]
        volume = np.sqrt(np.sum(samples**2)/len(samples))*1E4
        readings.append(reading(pitch, volume))

        
    