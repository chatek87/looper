import sounddevice as sd
import soundfile as sf

filename = "output.wav"
data, fs = sf.read(filename, dtype='float32')

buffer_size = 4096
buffer_pos = 0
buffer = data[:buffer_size]

def buffer_callback(outdata, frames, time, status):
    global buffer_pos, buffer

    if status:
        print(status)

    read_start = buffer_pos
    read_end = buffer_pos + frames
    out_end = buffer_pos + frames

    if read_end > len(data):
        read_end = len(data)
        out_end = len(data) - buffer_pos

    outdata[:, 0] = buffer[:read_end-buffer_pos]
    outdata[:, 1:] = 0

    buffer_pos += frames

    if buffer_pos >= len(data):
        buffer_pos = 0

    buffer = data[buffer_pos:buffer_pos+buffer_size]

with sd.OutputStream(channels=2, blocksize=buffer_size, samplerate=fs, callback=buffer_callback):
    print("Starting playback...")

    while True:
        if buffer_pos == 0:
            print("Looping audio file...")
        sd.sleep(100) # Give the callback function time to process data.
