from language_generate import large_language_model
from tts_speech import speech_edge_tts
from audio_record import record
from playsound import playsound
import speech_recognition as sr
import logging
import asyncio

# 配置日志记录
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

setting = open('text_program/ai_setting_VTuber-Neuro sama.txt', 'r', encoding="utf-8").read()
conversation_history = [{'role': 'system', 'content': f'{setting}'}]  # You can use dictionary to show it

record_language = "en-US"
speech_language = 'en-US-AvaNeural'
output_path = "text_program/audio/output.mp3"

recognizer = sr.Recognizer() # 初始化识别器

def main(content, conversation_history):
    # Add user input to conversation history
    try:
        # Get the model's response
        print(f"User: {content}")
        response = large_language_model(content, conversation_history)
        print(f"Agent: {response}")

        # 这里需要注意一下，因为这是一个内部路径，而主程序是在根目录下运行的，所以这里的路径是相对于根目录的
        asyncio.run(speech_edge_tts(text=response, path=output_path, speech_language=speech_language))
        playsound(output_path)

    except Exception as e:
        print(f'Error playing audio: {e}')

def run():
    while True:
        content = record(recognizer, record_language)
        if not content: # 如果没有检测到音频，则跳过循环
            # logging.info("No audio detected")  # 使用 logging 替代 print
            continue
        else:
            try:
                main(content, conversation_history)
            except Exception as e:
                print(f"Error in main function: {e}")

if __name__ == '__main__':
    run()

