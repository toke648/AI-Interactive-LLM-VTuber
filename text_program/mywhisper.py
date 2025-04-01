import whisper
import sounddevice as sd
import numpy as np
import wave

# 录音参数
duration = 5  # 录音时间（秒）
sample_rate = 16000  # 采样率
channels = 1  # 单声道

print("开始录音...")
audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, dtype=np.int16)
sd.wait()
print("录音完成")


# 保存为 WAV 文件
wav_filename = "audio/record.mp3"
with wave.open(wav_filename, "wb") as wf:
    wf.setnchannels(channels)
    wf.setsampwidth(2)
    wf.setframerate(sample_rate)
    wf.writeframes(audio_data.tobytes())

# 加载 Whisper 识别
model = whisper.load_model("small")
result = model.transcribe(wav_filename)
print("识别文本:", result["text"])


# import whisper

# model = whisper.load_model("medium")  # 选择合适的模型
# result = model.transcribe("audio.mp3", fp16=False)  # 禁用 FP16
# print(result["text"])