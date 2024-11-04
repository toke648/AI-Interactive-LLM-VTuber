# 类OpenAi实时语音输入
import speech_recognition as sr

def record():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Please start talking...")

        while True:
            try:
                # 检测声音
                audio = recognizer.listen(source, timeout=2)
                text = recognizer.recognize_google(audio, language='en-US')

                print(f"You told: {text}")
                return text
            except sr.UnknownValueError as u:
                # 如果无法理解语音，可以选择忽略
                print(f'无法理解语音')
            except sr.WaitTimeoutError as w:
                # 超过 2 秒没有检测到声音，继续循环
                print(f'超过 2 秒没有检测到声音')
            except sr.RequestError as e:
                print(f"识别服务出错: {e}")

if __name__ == '__main__':
    record()
