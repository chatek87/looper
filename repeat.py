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

filename = "output.wav"

# Open a stream to play the recorded audio in a loop
wf = wave.open(filename, 'rb')
stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    output_device_index=1)
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