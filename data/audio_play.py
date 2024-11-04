import pyaudio
import wave

# 录音
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "output.wav"

audio = pyaudio.PyAudio()

# 开始录音
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
print("Recording...")

frames = []

try:
    while True:
        data = stream.read(CHUNK)
        frames.append(data)
except KeyboardInterrupt:
    print("Recording finished.")

# 结束录音
stream.stop_stream()
stream.close()
audio.terminate()

# 保存为 WAV 文件
with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"Audio saved as {WAVE_OUTPUT_FILENAME}")