import os
import json

# Setting class
class MainSetting():
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
            self.path_dir = os.path.dirname(os.path.abspath(__file__))
            self.system_prompt = open(config['llm']['system_prompt_file'], 'r', encoding='utf-8').read()

            # TTS
            self.default_voice = config['tts']['default_voice']
            self.default_rate = config['tts']['default_rate']
            self.default_volume = config['tts']['default_volume']

            # Speech Recognition

    # STT Setting
    def load_audio_path(self):
        path = os.path.join(self.audio_directory, self.audio_file)
        return path

    # def load_system_prompt(self):
    #     path = os.path.join(self.path_dir, self.system_prompt)
    #     return open(path, 'r').read()

    # def get_content(self):
    #     content_history = [{'role': 'system', 'content': f'{self.system_prompt}'}]
    #     return content_history

