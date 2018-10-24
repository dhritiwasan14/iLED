import aubio
import numpy as np
import pyaudio
import wave

# PyAudio object.
p = pyaudio.PyAudio()

# Open stream.
stream = p.open(format=pyaudio.paFloat32,
    channels=1, rate=44100, input=True,
    frames_per_buffer=1024)

# Aubio's pitch detection.
pDetection = aubio.pitch("default", 2048,
    2048//2, 44100)
# Set unit.
pDetection.set_unit("Hz")
pDetection.set_silence(-40)
raw_pitches, raw_volumes = [], []

CHUNK_SIZE=20


def rms(values):

        return np.mean(np.square(values))**0.5


def moving_rms(values, thresh=CHUNK_SIZE):
        print (values)
        print(type(values))
        if values.any(): return None

        return rms( values[-thresh:] )

while True:

    data = stream.read(1024)
    samples = np.fromstring(data,
        dtype=aubio.float_type)
    pitch = pDetection(samples)[0]
    # Compute the energy (volume) of the
    # current frame.
    volume = np.sum(samples**2)/len(samples)
    # Format the volume output so that at most
    # it has six decimal npbers.
    volume = "{:.6f}".format(volume)

    raw_pitches.append(pitch)
    raw_volumes.append(volume)
 
    if len(raw_pitches) % 5 == 0:
        if len(raw_pitches) > 5000:
            assert len(raw_pitches) == len(raw_volumes)

            raw_pitches == raw_pitches[-CHUNK_SIZE:]
            raw_volumes == raw_volumes[-CHUNK_SIZE:]

        processed_pitch = moving_rms(np.asarray(raw_pitches).astype(np.float))
        processed_volume = moving_rms(np.asarray(raw_volumes).astype(np.float))

        print(processed_pitch, processed_volume)
        raw_pitches, raw_volumes = [], []
        # send_message(processed_pitch, processed_volume)

    if len(raw_pitches) > 5000:
        raw_pitches == raw_pitches[-CHUNK_SIZE:]
        raw_volumes == raw_volumes[-CHUNK_SIZE:]