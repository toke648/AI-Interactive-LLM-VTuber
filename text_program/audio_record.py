# Like Chatgpt Real time voice input
import speech_recognition as sr

def record(recognizer, language='en-US'):  # 默认值，如果没有传入参数，则使用默认值

    with sr.Microphone() as source:
        # print("Please start talking...")

        try:
            # Detecting sound
            audio = recognizer.listen(source, timeout=2, phrase_time_limit=5) # phrase_time_limit=15 意思是最多录制5秒的音频
            text = recognizer.recognize_google(audio, language=language)

            print(f"You told: {text}")
            return text
        except sr.UnknownValueError as u:
            # If you cannot understand the voice, you can choose to ignore it
            print(f'Can not understand audio')
            return
        except sr.WaitTimeoutError as w:
            # No sound detected for more than 2 seconds, continue looping
            print(f'No Sound detected for more than 2 seconds')
            return
        except sr.RequestError as e:
            print(f"Identification service error: {e}")
            return

if __name__ == '__main__':
    record()
