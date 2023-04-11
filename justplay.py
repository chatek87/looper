import pyaudio
import wave
import datetime
import sounddevice

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096
RECORD_SECONDS = 1

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
#now = datetime.datetime.now()
#filename = "output_" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".wav"
filename = "output.wav"

# Open a stream to record audio using the Tapco USB Interface
# stream = audio.open(format=FORMAT, 
#                     channels=CHANNELS,
#                     rate=RATE, input=True, input_device_index=input_device_index,
#                     frames_per_buffer=CHUNK)

# print("Recording...")
# frames = []

# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     frames.append(data)

# print("Finished recording!")

# stream.stop_stream()
# stream.close()
# audio.terminate()

# # Save the recorded audio to a WAV file with the unique filename
# wf = wave.open(filename, 'wb')
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(audio.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(b''.join(frames))
# wf.close()

# Open a stream to play the recorded audio in a loop
wf = wave.open(filename, 'rb')
stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    output_device_index=output_device_index)
if not stream:
    print("Error: Could not open audio stream!")
    
print("Playing audio...")

# while True:
#     data = wf.readframes(CHUNK)
#     if not data:
#         # Reached the end of the audio file, rewind and play from the beginning
#         wf.rewind()
#         data = wf.readframes(CHUNK)
#     stream.write(data)
play_count = 0
play_limit = 3  # play the audio 3 times
while play_count < play_limit:
    data = wf.readframes(CHUNK)
    if not data:
        # Reached the end of the audio file, rewind and increment the play count
        wf.rewind()
        play_count += 1
        continue  # continue playing the audio
    stream.write(data)


stream.stop_stream()
stream.close()
wf.close()
audio.terminate()