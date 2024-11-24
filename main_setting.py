# 不亏是我，这样就可以直接在后端设置数据集，而不用前后端多次调试了
# 此界面可用于设置数据集
class MainSetting():
    def __init__(self):
        # data_route
        self.audio_directory = "audio"
        self.audio_file = "output.mp3"

        # tts Setting
        # self.default_voice = 'en-US-AvaNeural'
        # self.default_voice = 'ja-JP-NanamiNeural'
        self.default_voice = 'zh-CN-XiaoxiaoNeural'

        self.default_rate = "-5%"
        self.default_volume = "+50%"

        # llm Setting
        self.system_prompt = open('templates/ai_setting_失忆少女.txt', 'r').read()

        self.api_key = "sk-707613869ffe4b06b165e396e580f847"
        self.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"

        self.models = "qwen-plus"

        # STT Setting

    def get_audio_path(self):
        import os
        return os.path.join(self.audio_directory, self.audio_file)

    # def get_content(self):
    #     content_history = [{'role': 'system', 'content': f'{self.system_prompt}'}]
    #     return content_history







