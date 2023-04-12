import pyaudio
import wave
import sounddevice as sd
import soundfile as sf
import datetime
import sounddevice
import keyboard

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096

audio = pyaudio.PyAudio()

# Find the Tapco USB Interface device index and name
input_device_index = None
output_device_index = None
for i in range(audio.get_device_count()):
    device_info = audio.get_device_info_by_index(i)
    if "Tapco USB Interface" in device_info["name"]:
        if device_info["maxInputChannels"] > 0:
            input_device_index = i
        if device_info["maxOutputChannels"] > 0:
            output_device_index = i
    if input_device_index is not None and output_device_index is not None:
        break

if input_device_index is None:
    print("Error: Tapco USB Interface input not found!")
    audio.terminate()
    exit(1)
if output_device_index is None:
    print("Error: Tapco USB Interface output not found!")
    audio.terminate()
    exit(1)

# Generate a unique filename using the current date and time
# now = datetime.datetime.now()
# filename = "output_" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".wav"
filename = "output.wav"

# Wait for the user to press the spacebar to start the recording
print("Press the spacebar to start recording...")
while True:
    if keyboard.is_pressed('space'):
        break

# Open a stream to record audio using the Tapco USB Interface
stream = audio.open(format=FORMAT, 
                    channels=CHANNELS,
                    rate=RATE, input=True, input_device_index=input_device_index,
                    frames_per_buffer=CHUNK)

print("Recording...")
frames = []

# Wait for the user to press the spacebar again to stop the recording
while True:
    if keyboard.is_pressed('space'):
        break
    data = stream.read(CHUNK)
    frames.append(data)

print("Finished recording!")

stream.stop_stream()
stream.close()
audio.terminate()

# Save the recorded audio to a WAV file with the unique filename
wf = wave.open(filename, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()


#########################################################################################################################################


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
    print("Press the spacebar to start playback...")

    # Wait for the user to press the spacebar to start the playback
    while True:
        if keyboard.is_pressed('space'):
            break
