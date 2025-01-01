import os
import yaml

# 此界面用于设置数据集
class MainSetting():
    def __init__(self):
        
        # config_file = 'config.yaml'
        # with open(config_file, 'r', encoding='utf-8') as f:
        #     config = yaml.safe_load(f)
        #
        #     # path Setting
        #     self.system_prompt = os.path.join(os.path.dirname(os.path.abspath(__file__)), config['system_prompt'])
        #
        #     self.audio_directory = config['audio_directory']
        #     self.audio_file = config['audio_file']
        #
        #     # llm Setting
        #     self.openai_api_key = config['openai_api_key']
        #     self.openai_base_url = config['openai_base_url']
        #
        #     self.models = config['models']
        #
        #     self.default_voice = config['default_voice']
        #     self.default_rate = config['default_rate']
        #     self.default_volume = config['default_volume']


        # data_route

        self.audio_directory = "audio"
        self.audio_file = "output.mp3"

        # tts Setting
        self.default_voice = 'en-US-AvaNeural'
        # self.default_voice = 'ja-JP-NanamiNeural'
        # self.default_voice = 'zh-CN-XiaoxiaoNeural'

        self.default_rate = "-5%"
        self.default_volume = "+50%"

        # llm Setting
        self.path_dir = os.path.dirname(os.path.abspath(__file__))
        self.system_prompt = open('templates/ai_setting_VTuber-Neuro sama.txt', 'r').read()

        # 我用的是阿里云的通义千问模型
        self.openai_api_key = "sk-707613869ffe4b06b165e396e580f847"
        self.openai_base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"

        self.models = "qwen-plus"

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

