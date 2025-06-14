import speech_recognition as sr

recognizer = sr.Recognizer()

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = recognizer

    def record(self, recognizer, language='en-US'):
        """
        录音并识别
        :param recognizer: 语音识别器实例
        :param language: 识别语言
        :return: 识别结果
        """
        with sr.Microphone() as source:
            # 调整麦克风参数以减少环境噪音
            self.recognizer.dynamic_energy_threshold = False
            self.recognizer.energy_threshold = 300
            self.recognizer.pause_threshold = 0.5

            try:
                # 减少超时时间，提高响应速度
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio, language=language)

                print(f"You told: {text}")
                return text
            except sr.UnknownValueError:
                print('Can not understand audio')
                return None
            except sr.WaitTimeoutError:
                print('No Sound detected')
                return None
            except sr.RequestError as e:
                print(f"Identification service error: {e}")
                return None
        
# if __name__ == "__main__":
#     speech_recognizer = SpeechRecognizer()

#     sound = True  # 设置为True表示有声音输入
#     # 如果没有声音输入，可以将sound设置为False

#     while True:
#         # 检测是否有唤醒词，如果没有则继续等待
#         result = speech_recognizer.record(recognizer, language='zh-CN')
#         if result == "你好小智":
#             print("唤醒成功")
#             text = speech_recognizer.record(recognizer, language='zh-CN')  # 可以根据需要修改语言参数
#         elif sound == False:
#             print("没有声音输入，继续等待...")
#             continue