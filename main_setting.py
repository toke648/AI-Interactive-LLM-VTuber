# This interface is for the Settings dataset
class MainSetting():
    def __init__(self):
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
        self.system_prompt = open('templates/ai_setting_失忆少女.txt', 'r').read()

        self.api_key = "your_api_key"
        self.base_url = "your_base_url"

        self.models = "qwen-plus"

        # STT Setting

    def get_audio_path(self):
        import os
        return os.path.join(self.audio_directory, self.audio_file)








