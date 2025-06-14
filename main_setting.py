import os
import json

class MainSetting:
    def __init__(self, config_file='main_setting.json'):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(self.base_path, config_file)

        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # Path
        self.audio_directory = config['path'].get('audio_directory', 'audio')
        self.audio_file = config['path'].get('audio_file', 'output.mp3')

        # TTS
        tts_cfg = config.get('tts', {})
        self.tts_voice = tts_cfg.get('default_voice', '')
        self.tts_rate = tts_cfg.get('default_rate', '0%')
        self.tts_volume = tts_cfg.get('default_volume', '0%')

        # STT
        sst_cfg = config.get('sst', {})
        self.sst_language = sst_cfg.get('default_language', 'zh-CN')
        self.sst_rate = sst_cfg.get('default_rate', '0%')
        self.sst_volume = sst_cfg.get('default_volume', '0%')

        # LLM
        llm_cfg = config.get('llm', {})
        self.openai_api_key = llm_cfg.get('openai_api_key', '')
        self.openai_base_url = llm_cfg.get('openai_base_url', '')
        self.models = llm_cfg.get('models', 'gpt-3.5-turbo')

        # System Prompt
        prompt_path = os.path.join(self.base_path, llm_cfg.get('system_prompt_file', 'system_prompt.txt'))
        self.system_prompt = self._read_file(prompt_path)

    def _read_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return ''

    def get_audio_path(self):
        return os.path.join(self.audio_directory, self.audio_file)
    
