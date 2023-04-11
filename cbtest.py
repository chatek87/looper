#circular buffer test
import sounddevice as sd
import soundfile as sf
import numpy as np

filename = "output.wav"
data, fs = sf.read(filename, dtype='float32')

buffer_size = 4096
buffer = np.zeros((buffer_size, 2), dtype='float32')
buffer_pos = 0

def generate_samples():
    global buffer_pos
    while True:
        if buffer_pos + buffer_size < len(data):
            read_start = buffer_pos
            read_end = buffer_pos + buffer_size
            buffer[:] = data[read_start:read_end]
            buffer_pos = read_end
        else:
            samples_remaining = len(data) - buffer_pos
            read_start = buffer_pos
            read_end = buffer_size - samples_remaining
            buffer[:samples_remaining] = data[read_start:]
            buffer[samples_remaining:] = data[:read_end]
            buffer_pos = read_end
        yield buffer
        
play_count = 0
play_limit = 3
stream = sd.OutputStream(channels=2, blocksize=buffer_size, callback=generate_samples())

with stream:
    while play_count < play_limit:
        print("Starting playback...")
        stream.start()
        sd.sleep(3000)
        stream.stop()
        print("Finished playback.")
        play_count += 1
