from language_generate import large_language_model
from tts import speech_generation_model
from audio_record import record
from playsound import playsound
import pandas as pd
import asyncio

def main():
    # Add user input to conversation history
    conversation_history.append({'role': 'user', 'content': content})
    try:
        # Get the model's response
        response = large_language_model(content, conversation_history)
        print(response)

        # Add assistant's response to conversation history
        conversation_history.append({'role': 'assistant', 'content': response})

        # Generate speech
        asyncio.run(speech_generation_model(response))

        # Play audio file
        audio_file_path = "data/audio/audio.mp3"
        playsound(audio_file_path)
    except Exception as e:
        print(f'Error playing audio: {e}')


if __name__ == '__main__':
    conversation_history = [
        {'role': 'system', 'content': 'You are a helpful assistant.Notice:your every sentence do not exceed 30 word.'},
    ]

    while True:
        content = input('\n>>> ')
        if content.lower() == 'exit':
            break
        elif content.lower() == 'audio':
            content = record()
            if content:
                main()
            else:
                print('没有有效输入，无法构建信息')
        elif content.lower() == 'dictionary':
            print(pd.DataFrame(conversation_history))
        else:
            main()
