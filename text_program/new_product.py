from language_generate import large_language_model
from tts_speech import speech_edge_tts
from audio_record import record
from playsound import playsound
import pandas as pd
import logging
import asyncio

# 配置日志记录
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main(content, conversation_history):
    # Add user input to conversation history
    try:
        # Get the model's response
        response = large_language_model(content, conversation_history)
        print(response)

        # Generate speech
        # Play audio file
        # 这里需要注意一下，因为这是一个内部路径，而主程序是在根目录下运行的，所以这里的路径是相对于根目录的
        output_path = "text_program/audio/output.mp3"
        asyncio.run(speech_edge_tts(response, output_path))
        playsound(output_path)
    except Exception as e:
        print(f'Error playing audio: {e}')


if __name__ == '__main__':
    # You can set Initial Setting of AI
    setting = open('text_program/ai_setting_VTuber-Neuro sama.txt', 'r', encoding="utf-8").read()

    # You can use dictionary to show it
    conversation_history = [
        {'role': 'system', 'content': f'{setting}'},
    ]

    input_path = "text_program/audio/record.mp3"

    while True:
        audio_text = record()
        if "Hey Siri" in audio_text:
            logging.debug(f"识别到的音频文本: {audio_text}")
            playsound("text_program/audio/fixed.mp3")

            content = record()
            main(content, conversation_history)

        elif "再见Siri" in audio_text:
            logging.info("检测到 '再见Siri'")
            print("Exit")
            break
