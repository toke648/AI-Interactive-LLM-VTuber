from language_generate import large_language_model
from tts import speech_generation_model
from audio_record import record
from playsound import playsound
import pandas as pd
import asyncio

def main():
    # Add user input to conversation history
    try:
        # Get the model's response
        response = large_language_model(content, conversation_history)
        print(response)

        # Generate speech
        # Play audio file
        audio_file_path = r"audio\output.mp3"
        asyncio.run(speech_generation_model(response, audio_file_path))
        playsound(audio_file_path)
    except Exception as e:
        print(f'Error playing audio: {e}')


if __name__ == '__main__':
    # You can set Initial Setting of AI
    setting = open('ai_setting_VTuber-Neuro sama.txt', 'r').read()

    # You can use dictionary to show it
    conversation_history = [
        {'role': 'system', 'content': f'{setting}'},
    ]

    while True:
        content = input('\n>>> ')
        if content.lower() == 'exit':
            break
        elif content.lower() == 'audio':
            for i in range(3):
                content = record()
                if content:
                    main()
                else:
                    print('No valid input, unable to construct information')
        elif content.lower() == 'dictionary':
            print(pd.DataFrame(conversation_history))
        else:
            main()
