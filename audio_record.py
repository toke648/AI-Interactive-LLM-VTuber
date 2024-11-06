# Like Chatgpt Real time voice input
import speech_recognition as sr

def record():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Please start talking...")

        while True:
            try:
                # Detecting sound
                audio = recognizer.listen(source, timeout=2)
                text = recognizer.recognize_google(audio, language='en-US')

                print(f"You told: {text}")
                return text
            except sr.UnknownValueError as u:
                # If you cannot understand the voice, you can choose to ignore it
                print(f'Can not understand audio')
            except sr.WaitTimeoutError as w:
                # No sound detected for more than 2 seconds, continue looping
                print(f'No Sound detected for more than 2 seconds')
            except sr.RequestError as e:
                print(f"Identification service error: {e}")

if __name__ == '__main__':
    record()
