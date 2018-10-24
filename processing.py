import pyaudio
from collections import namedtuple
import wave
import aubio
import sys

# length of data to read.
chunk = 1024
reading = namedtuple('reading', ['pitch', 'volume'])


def main(args):
    # open the file for reading, wav file
    wf = wave.open(sys.argv[1], 'rb')
    pA = pyaudio.PyAudio()
    mic = pA.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)

    readings = []
    pDetection = aubio.pitch(METHOD, BUFFER_SIZE,
        HOP_SIZE, SAMPLE_RATE)
    while True:

        data = mic.read(2048//2) # per chunk
        samples = np.fromstring(data, dtype=aubio.float_type) 
        pitch = pDetection(samples)[0]
        volume = np.sqrt(np.sum(samples**2)/len(samples))*1E4
        readings.append(reading(pitch, volume))

        
    