# utf-8 encoding
# main_setting.py
import os
import json

class MainSetting:
    """初始化主设置类"""
    
    def __init__(self, config_file='main_setting.json'):
        """
        主设置类，用于加载和保存设置，默认加载main_setting.json文件
        
        属性:
        - audio_directory: 音频目录
        - audio_file: 音频文件
        - tts_voice: TTS语音
        - tts_rate: TTS语速
        - tts_volume: TTS音量
        - sst_language: STT语言
        - sst_rate: STT语速
        - sst_volume: STT音量
        - llm_model: LLM模型
        - system_prompt: 系统提示
        
        Args:
            config_file: 配置文件路径，默认加载main_setting.json文件
        """

        # 获取当前文件的目录
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(self.base_path, config_file)

        # 加载配置文件
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # 路径
        self.audio_directory = config['path'].get('audio_directory', 'audio')
        self.audio_file = config['path'].get('audio_file', 'output.mp3')

        # TTS配置
        tts_cfg = config.get('tts', {})
        self.tts_voice = tts_cfg.get('default_voice', '')
        self.tts_rate = tts_cfg.get('default_rate', '0%')
        self.tts_volume = tts_cfg.get('default_volume', '0%')

        # STT配置
        sst_cfg = config.get('sst', {})
        self.sst_language = sst_cfg.get('default_language', 'zh-CN')
        self.sst_rate = sst_cfg.get('default_rate', '0%')
        self.sst_volume = sst_cfg.get('default_volume', '0%')

        # LLM配置
        llm_cfg = config.get('llm', {})
        self.openai_api_key = llm_cfg.get('openai_api_key', '')
        self.openai_base_url = llm_cfg.get('openai_base_url', '')
        self.models = llm_cfg.get('models', 'gpt-3.5-turbo')

        # 系统提示
        prompt_path = os.path.join(self.base_path, llm_cfg.get('system_prompt_file', 'system_prompt.txt'))
        self.system_prompt = self._read_file(prompt_path)

    def _read_file(self, path: str) -> str:
        """读取文件"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return ''

    def get_audio_path(self):
        """获取音频路径"""
        return os.path.join(self.audio_directory, self.audio_file)
    
