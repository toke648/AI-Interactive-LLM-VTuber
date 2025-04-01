import json
import os

class Settings:
    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), 'main_setting.json'), 'r', encoding='utf-8') as f:
            config = json.load(f)

            # Path
            self.audio_directory = config['path']['audio_directory']
            self.audio_file = config['path']['audio_file']
            
            # LLM
            self.openai_api_key = config['llm']['openai_api_key']
            self.openai_base_url = config['llm']['openai_base_url']
            self.models = config['llm']['models']
            self.system_prompt_file = config['llm']['system_prompt_file']

            # TTS
            self.default_voice = config['tts']['default_voice']
            self.default_rate = config['tts']['default_rate']
            self.default_volume = config['tts']['default_volume']

            # Speech Recognition


settings = Settings()

