import pyaudio
import sounddevice

CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 1

audio = pyaudio.PyAudio()

# Set up input stream
input_stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK_SIZE)

# Set up output stream
output_stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, output=True,
                frames_per_buffer=CHUNK_SIZE)

# Record and overdub audio
frames = []
overdub_frames = []
while True:
    # Record audio for a specified number of seconds
    for i in range(0, int(RATE / CHUNK_SIZE * RECORD_SECONDS)):
        data = input_stream.read(CHUNK_SIZE)
        frames.append(data)
        if overdub:
            overdub_frames.append(data)

    # Playback recorded audio
    for frame in frames:
        output_stream.write(frame)

    # Playback overdubbed audio
    if overdub:
        for frame in overdub_frames:
            output_stream.write(frame)
